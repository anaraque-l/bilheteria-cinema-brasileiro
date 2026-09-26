# -*- coding: utf-8 -*-
"""Monta a base analitica a partir do bruto em data/raw/.

Executar: python src/build_dataset.py

O QUE ESTE MODULO FAZ
  - separa as linhas de filme do bloco de notas de rodape;
  - tipa: numero pt-BR ("1.286.000", "6.430.000,00") vira float;
  - torna a falta EXPLICITA: "ND" e "-" viram NaN, para o pandas contar;
  - deriva atributos que so dependem do passado (historico do diretor, da
    distribuidora, da produtora) e do proprio registro (coproducao, decada);
  - junta deflator do IPCA e populacao do IBGE;
  - define os dois alvos candidatos.

O QUE ESTE MODULO NAO FAZ - e nao deve fazer na Entrega 1
  Nao imputa. Nao remove outlier. Nao padroniza. Nao codifica categorica.
  Nao balanceia. Nao seleciona atributo. O enunciado e explicito: esta entrega
  descreve e diagnostica; a correcao e a Entrega 2. As hipoteses de
  pre-processamento sao ESCRITAS em docs/03-melhorias-e-tradeoffs.md, e la sao
  MEDIDAS por analise de
  sensibilidade - medir o impacto de uma decisao nao e o mesmo que aplica-la.
"""

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
BRUTO = RAIZ / "data" / "raw"
PRONTO = RAIZ / "data" / "processed"

# Marcadores de falta usados pela ANCINE. Nao sao NaN no arquivo: sao texto.
# Se nao traduzirmos, "ND" vira uma categoria legitima e a coluna numerica
# vira object. Este e o erro mais facil de cometer nesta base.
AUSENTES = {"ND", "-", "", "nd", "n/d", "N/D"}

COLUNAS = [
    "ano", "cpb", "titulo", "direcao", "genero", "produtora_maj", "uf_bruto",
    "produtora_min", "uf2_bruto", "distribuidora", "max_salas", "publico",
    "renda_corrente", "_vazia",
]


# ---------------------------------------------------------------------------
# Leitura e tipagem
# ---------------------------------------------------------------------------

def _ler_ancine():
    """Le o CSV cru e devolve (filmes, notas_de_rodape)."""
    caminho = BRUTO / "ancine_filmes_1995_2024r.csv"
    if not caminho.exists():
        raise SystemExit("Falta %s. Rode antes: python src/ingestao.py" % caminho)

    # skiprows=1 pula o titulo da planilha, que ocupa a primeira linha inteira.
    # encoding utf-8-sig porque o arquivo vem com BOM.
    df = pd.read_csv(caminho, sep=";", skiprows=1, encoding="utf-8-sig", dtype=str)
    df.columns = COLUNAS
    df = df.drop(columns="_vazia")

    # O rodape da planilha tem ~47 linhas de notas metodologicas, que o pandas
    # le como se fossem filmes. O criterio de corte e simples e robusto: linha
    # de filme tem ano com exatamente 4 digitos.
    eh_filme = df["ano"].astype("string").str.fullmatch(r"\d{4}").fillna(False)
    return df[eh_filme].copy(), df[~eh_filme].copy()


def _num_ptbr(serie, decimal=False):
    """Converte numero em formato pt-BR para float, com falta explicita.

    "1.286.000"    -> 1286000.0   (ponto e separador de milhar)
    "6.430.000,00" -> 6430000.0   (virgula e decimal)
    "ND", "-"      -> NaN
    """
    s = serie.astype("string").str.strip()
    s = s.where(~s.isin(AUSENTES), other=pd.NA)
    s = s.str.replace(".", "", regex=False)
    if decimal:
        s = s.str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")


def _texto(serie):
    """Normaliza espacos e marca falta, sem alterar o conteudo em si."""
    s = serie.astype("string").str.strip()
    return s.where(~s.isin(AUSENTES), other=pd.NA)


# ---------------------------------------------------------------------------
# Atributos derivados
# ---------------------------------------------------------------------------

def _uf_principal(uf_bruto):
    """Extrai a UF da produtora majoritaria de um campo baguncado.

    O campo tem 90 valores distintos no arquivo bruto (87 depois de normalizar
    espaco e marcar '-' como ausente) para 27 UFs possiveis, porque a ANCINE
    concatena: "RJ", "RJ/RJ", "SP/RJ", "PE/RS/RJ/SP", " -/DF", "-".
    Pegamos o PRIMEIRO codigo de duas letras, que e o da majoritaria.

    Isto e PARSING, nao correcao: nao inventamos UF onde nao ha (vira NaN) e a
    coluna original fica preservada em `uf_bruto` para auditoria.
    """
    def primeira(v):
        if pd.isna(v):
            return pd.NA
        achados = re.findall(r"[A-Z]{2}", str(v).upper())
        return achados[0] if achados else pd.NA
    return uf_bruto.map(primeira).astype("string")


def _n_ufs(uf_bruto):
    """Quantas UFs distintas aparecem no campo - proxy de dispersao regional."""
    def conta(v):
        if pd.isna(v):
            return np.nan
        achados = set(re.findall(r"[A-Z]{2}", str(v).upper()))
        return len(achados) if achados else np.nan
    return uf_bruto.map(conta)


def _historico_anterior(df, coluna):
    """Quantos filmes essa entidade ja tinha lancado ANTES do ano deste filme.

    Por que "antes" e nao "ate": se contarmos o proprio filme e os do mesmo
    ano, o atributo carrega informacao que so existe depois do lancamento - e
    vazamento temporal. Um diretor que estreou em 2024 tem historico 0 em 2024,
    nao 1.

    Implementacao: contagem acumulada por entidade e ano, menos a contagem do
    proprio ano. Filmes do MESMO ano nao contam entre si, que e o comportamento
    correto porque a base tem so o ano, nao a data exata do lancamento.
    """
    por_ano = (df.groupby([coluna, "ano"], dropna=True)
                 .size().rename("n").reset_index())
    por_ano = por_ano.sort_values([coluna, "ano"])
    por_ano["acum_ate"] = por_ano.groupby(coluna)["n"].cumsum()
    por_ano["anterior"] = por_ano["acum_ate"] - por_ano["n"]
    chave = df[[coluna, "ano"]].merge(
        por_ano[[coluna, "ano", "anterior"]], on=[coluna, "ano"], how="left")
    return chave["anterior"].to_numpy()


def _faixa_ordinal(serie, cortes, rotulos):
    """Binagem de uma contagem numa categorica ORDINAL.

    Por que ordinal e nao nominal: as faixas tem ordem natural (uma direcao
    veterana fez mais filmes que uma iniciante), e essa ordem e informacao.
    Codificar como nominal jogaria fora a ordem; como numerica, assumiria que
    a distancia entre faixas e constante, o que nao e verdade.

    Herdam a inocuidade do atributo de origem: `filmes_*_antes` conta so anos
    ESTRITAMENTE anteriores, entao a faixa tambem e anterior a estreia.
    """
    faixa = pd.cut(serie, bins=cortes, labels=rotulos, right=False,
                   include_lowest=True)
    return faixa.astype(pd.CategoricalDtype(categories=rotulos, ordered=True))


def _fomento_por_cpb(nome_arquivo, coluna_instrumento):
    """Le um arquivo de fomento e agrega por CPB.

    Uma obra aparece uma vez por contrato/projeto aprovado. Sem agregar, a
    juncao com a listagem multiplicaria linhas de filme - foi por isso que o
    registro da fonte avisa para agregar antes.
    """
    caminho = BRUTO / nome_arquivo
    if not caminho.exists():
        raise SystemExit("Falta %s. Rode antes: python src/ingestao.py" % caminho)
    f = pd.read_csv(caminho, sep=";", encoding="utf-8-sig", dtype=str)
    f["CPB"] = f["CPB"].str.strip()
    f = f[f["CPB"].notna() & (f["CPB"] != "-")]
    return f.groupby("CPB")[coluna_instrumento].size().rename("n").reset_index()


# ---------------------------------------------------------------------------
# Fontes complementares
# ---------------------------------------------------------------------------

def _deflator_anual(ano_base=2024):
    """Fator que leva reais correntes de cada ano para reais de `ano_base`.

    A serie 433 do BCB e a variacao percentual MENSAL do IPCA. Encadeamos os
    meses num indice, tiramos a media de cada ano e comparamos com o ano base.
    """
    bruto = json.loads((BRUTO / "bcb_ipca_433.json").read_text(encoding="utf-8"))
    ipca = pd.DataFrame(bruto)
    ipca["data"] = pd.to_datetime(ipca["data"], format="%d/%m/%Y")
    ipca["valor"] = pd.to_numeric(ipca["valor"])
    ipca = ipca[ipca["data"].dt.year >= 1994].sort_values("data")

    ipca["indice"] = 100 * (1 + ipca["valor"] / 100).cumprod()
    anual = ipca.groupby(ipca["data"].dt.year)["indice"].mean()
    fator = anual.loc[ano_base] / anual
    return fator.rename("deflator").rename_axis("ano").reset_index()


def _populacao():
    bruto = json.loads((BRUTO / "ibge_populacao.json").read_text(encoding="utf-8"))
    serie = bruto[0]["resultados"][0]["series"][0]["serie"]
    pop = pd.DataFrame({"ano": [int(a) for a in serie],
                        "populacao_br": [float(v) for v in serie.values()]})
    return pop.sort_values("ano")


# ---------------------------------------------------------------------------
# Montagem
# ---------------------------------------------------------------------------

def montar(verboso=True):
    filmes, notas = _ler_ancine()
    f = filmes.reset_index(drop=True)
    d = pd.DataFrame(index=range(len(f)))

    d["ano"] = f["ano"].astype(int)
    d["cpb"] = _texto(f["cpb"])
    d["titulo"] = _texto(f["titulo"])
    d["direcao"] = _texto(f["direcao"])
    d["genero"] = _texto(f["genero"])
    d["produtora_maj"] = _texto(f["produtora_maj"])
    d["produtora_min"] = _texto(f["produtora_min"])
    d["distribuidora"] = _texto(f["distribuidora"])
    d["uf_bruto"] = _texto(f["uf_bruto"])
    d["uf2_bruto"] = _texto(f["uf2_bruto"])

    d["max_salas"] = _num_ptbr(f["max_salas"])
    d["publico"] = _num_ptbr(f["publico"])
    d["renda_corrente"] = _num_ptbr(f["renda_corrente"], decimal=True)

    # --- derivados do proprio registro -------------------------------------
    d["uf_maj"] = _uf_principal(d["uf_bruto"])
    d["n_ufs"] = _n_ufs(d["uf_bruto"])
    d["coproducao"] = d["produtora_min"].notna().astype(int)
    d["decada"] = (d["ano"] // 10 * 10).astype(int)

    # --- derivados de historico (so passado) -------------------------------
    d["filmes_diretor_antes"] = _historico_anterior(d, "direcao")
    d["filmes_distribuidora_antes"] = _historico_anterior(d, "distribuidora")
    d["filmes_produtora_antes"] = _historico_anterior(d, "produtora_maj")
    d["estreia_do_diretor"] = (d["filmes_diretor_antes"] == 0).astype("Int64")

    # --- categoricas ORDINAIS ----------------------------------------------
    # O enunciado pede explicitamente que os tipos incluam categorica ordinal.
    # Estas duas sao ordinais de verdade (as faixas tem ordem) e continuam
    # anteriores a estreia, porque derivam de contagens so do passado.
    d["experiencia_da_direcao"] = _faixa_ordinal(
        d["filmes_diretor_antes"], [0, 1, 3, 6, np.inf],
        ORDEM_ORDINAIS["experiencia_da_direcao"])
    # Cortes do porte da distribuidora: a mediana do historico e 9 e o p90 e 72,
    # entao 5 / 20 / 60 separa os quatro grupos sem deixar faixa quase vazia.
    d["porte_da_distribuidora"] = _faixa_ordinal(
        d["filmes_distribuidora_antes"], [0, 5, 20, 60, np.inf],
        ORDEM_ORDINAIS["porte_da_distribuidora"])

    # --- fomento publico ----------------------------------------------------
    # Fomento e APROVADO antes de a obra existir: e informacao legitimamente
    # anterior a estreia, e e o que liga o projeto a pergunta de politica
    # publica - o dinheiro esta indo para filmes que encontram plateia?
    fsa = _fomento_por_cpb("ancine_fomento_fsa.csv", "NUMERO_CONTRATO_FSA")
    inc = _fomento_por_cpb("ancine_fomento_indireto.csv", "NUMERO_SALIC")

    d["contratos_fsa"] = d["cpb"].map(dict(zip(fsa["CPB"], fsa["n"]))).fillna(0).astype(int)
    d["projetos_incentivo"] = d["cpb"].map(dict(zip(inc["CPB"], inc["n"]))).fillna(0).astype(int)
    d["recebeu_fsa"] = (d["contratos_fsa"] > 0).astype(int)
    d["recebeu_incentivo"] = (d["projetos_incentivo"] > 0).astype(int)

    # Categorica NOMINAL que resume os dois mecanismos num atributo so.
    # Filme sem CPB nao pode ser checado: vira NaN, nao "sem fomento".
    origem = pd.Series("sem fomento", index=d.index, dtype=object)
    origem[(d["recebeu_fsa"] == 1) & (d["recebeu_incentivo"] == 0)] = "só FSA"
    origem[(d["recebeu_fsa"] == 0) & (d["recebeu_incentivo"] == 1)] = "só incentivo"
    origem[(d["recebeu_fsa"] == 1) & (d["recebeu_incentivo"] == 1)] = "FSA e incentivo"
    origem[d["cpb"].isna()] = np.nan
    d["origem_do_fomento"] = origem
    for col in ["contratos_fsa", "projetos_incentivo", "recebeu_fsa", "recebeu_incentivo"]:
        d.loc[d["cpb"].isna(), col] = np.nan

    # --- contexto de mercado ------------------------------------------------
    d = d.merge(_deflator_anual(), on="ano", how="left")
    d["renda_deflacionada_2024"] = d["renda_corrente"] * d["deflator"]
    d = d.merge(_populacao(), on="ano", how="left")

    # quantos filmes brasileiros disputaram a bilheteria no mesmo ano
    d["filmes_no_ano"] = d.groupby("ano")["titulo"].transform("size")

    # --- alvos candidatos ---------------------------------------------------
    # (a) mediana global: definicao literal do enunciado
    mediana_global = d["publico"].median()
    d["sucesso_global"] = (d["publico"] > mediana_global).astype("Int64")
    d.loc[d["publico"].isna(), "sucesso_global"] = pd.NA

    # (b) mediana do ano: controla o tamanho do mercado, que mudou muito entre
    # 1995 e 2024. Qual dos dois usar e a decisao D4 de docs/02 - a EDA e que
    # da o argumento. Deixamos os dois na base de proposito.
    mediana_ano = d.groupby("ano")["publico"].transform("median")
    d["mediana_publico_do_ano"] = mediana_ano
    d["sucesso_no_ano"] = (d["publico"] > mediana_ano).astype("Int64")
    d.loc[d["publico"].isna(), "sucesso_no_ano"] = pd.NA

    PRONTO.mkdir(parents=True, exist_ok=True)
    d.to_csv(PRONTO / "filmes.csv", index=False, encoding="utf-8")
    notas.to_csv(PRONTO / "notas_de_rodape.csv", index=False, encoding="utf-8")

    if verboso:
        print("Base montada: %d filmes, %d atributos" % d.shape)
        print("  mediana global de publico: %s" % format(mediana_global, ",.0f"))
        print("  linhas de rodape separadas: %d" % len(notas))
        print("  gravado em data/processed/filmes.csv")
    return d


# Colunas que NUNCA podem entrar como atributo num modelo desta base. Esta lista
# vive aqui, e nao no notebook, porque e a mesma para qualquer experimento: quem
# montar o X da Entrega 2 elimina estas colunas primeiro e discute depois.
#   publico, renda_*        - sao o alvo, ou o alvo em outra unidade (rho = 0,985)
#   max_salas               - maximo da CARREIRA: contaminado pelo desempenho (D6)
#   mediana_publico_do_ano  - e o proprio limiar do alvo relativo
#   filmes_no_ano           - contagem que so fecha em 31/12: nao existe na estreia
#   sucesso_*               - os alvos
COLUNAS_PROIBIDAS = [
    "publico", "renda_corrente", "renda_deflacionada_2024", "max_salas",
    "mediana_publico_do_ano", "filmes_no_ano", "sucesso_global", "sucesso_no_ano",
]


def atributos_legitimos(d):
    """Devolve as colunas de `d` que podem entrar num modelo pre-estreia.

    Uso: `X = d[build_dataset.atributos_legitimos(d)]`. Tambem exclui `cpb` e
    `titulo`, que sao identificadores, nao atributos.
    """
    fora = set(COLUNAS_PROIBIDAS) | {"cpb", "titulo"}
    return [c for c in d.columns if c not in fora]


# Ordem das categoricas ORDINAIS. Precisa viver aqui porque o CSV nao guarda
# tipo: sem restaurar isso na leitura, um groupby ordena alfabeticamente e
# "estabelecida" vem antes de "estreante" - o que destroi justamente a ordem
# que torna o atributo ordinal.
ORDEM_ORDINAIS = {
    "experiencia_da_direcao": ["estreante", "iniciante", "estabelecida", "veterana"],
    "porte_da_distribuidora": ["nova", "pequena", "media", "grande"],
}


def _restaurar_ordinais(d):
    for col, ordem in ORDEM_ORDINAIS.items():
        if col in d.columns:
            d[col] = d[col].astype(pd.CategoricalDtype(categories=ordem, ordered=True))
    return d


def carregar():
    """Le a base pronta. Usado pelo notebook e por sensibilidades.py."""
    caminho = PRONTO / "filmes.csv"
    if not caminho.exists():
        return montar(verboso=False)
    return _restaurar_ordinais(pd.read_csv(caminho, encoding="utf-8"))


if __name__ == "__main__":
    montar()
