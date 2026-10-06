# -*- coding: utf-8 -*-
"""O X e o y da Entrega 2, e os folds que todas as combinacoes compartilham.

O QUE MUDA EM RELACAO A E1
  - o alvo passa a ser o P75 do ano anterior, recomendacao M8 da auditoria
    do alvo: limiar conhecido antes da estreia e na fronteira entre as duas
    populacoes de publico;
  - entram tres atributos de historico de sucesso, a melhoria M2 da E1.

build_dataset.py nao e alterado: ele e o entregavel congelado da E1.
"""

import json
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build_dataset as bd  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent.parent
SAIDA = RAIZ / "reports" / "e2"
SEMENTE = 42

NUMERICAS = [
    "ano", "filmes_diretor_antes", "filmes_distribuidora_antes",
    "filmes_produtora_antes", "coproducao", "recebeu_fsa", "recebeu_incentivo",
    "contratos_fsa", "projetos_incentivo",
    "hist_diretor", "hist_distribuidora", "hist_produtora",
]
NOMINAIS = ["genero", "uf_maj", "distribuidora", "origem_do_fomento"]
ORDINAIS = ["experiencia_da_direcao", "porte_da_distribuidora"]
ATRIBUTOS = NUMERICAS + NOMINAIS + ORDINAIS

# entidade de origem de cada atributo de historico
HISTORICOS = {
    "hist_diretor": "direcao",
    "hist_distribuidora": "distribuidora",
    "hist_produtora": "produtora_maj",
}


def historico_de_sucesso(d, entidade):
    """log10 da mediana do publico dos filmes da entidade em anos anteriores.

    So entram anos estritamente anteriores, pelo mesmo motivo da decisao D8 da
    E1: filmes do mesmo ano nao contam entre si porque a base so tem o ano.
    Mediana e log porque o publico e lei de potencia, e a media de tres filmes
    de um diretor seria praticamente o maior deles. Sem historico fica NaN:
    a ausencia e estrutural e quem decide o que fazer com ela e a etapa de
    ausentes da grade.
    """
    log_publico = np.log10(d["publico"])
    saida = pd.Series(np.nan, index=d.index)
    com_publico = d["publico"].notna()
    for _, grupo in d[d[entidade].notna()].groupby(entidade):
        anos = grupo["ano"].to_numpy()
        validos = com_publico[grupo.index].to_numpy()
        valores = log_publico[grupo.index].to_numpy()
        for indice, ano in zip(grupo.index, anos):
            anteriores = valores[(anos < ano) & validos]
            if len(anteriores):
                saida[indice] = np.median(anteriores)
    return saida


def limiar_do_ano_anterior(d, quantil):
    """Quantil do publico do ano anterior, mapeado para cada filme."""
    por_ano = d.groupby("ano")["publico"].quantile(quantil)
    # o deslocamento abaixo so significa ano anterior se nao faltar ano na serie
    assert (np.diff(por_ano.index) == 1).all(), "serie de anos com buraco"
    return d["ano"].map(por_ano.shift(1))


def montar(quantil=0.75):
    """Base da E2 completa, com alvo, antes de separar X e y."""
    return _montar(quantil).copy()


# o historico percorre a base filme a filme; a grade chama isto muitas vezes
@lru_cache(maxsize=None)
def _montar(quantil):
    d = bd.carregar()
    for coluna, entidade in HISTORICOS.items():
        d[coluna] = historico_de_sucesso(d, entidade)

    limiar = limiar_do_ano_anterior(d, quantil)
    d["sucesso"] = (d["publico"] > limiar).astype(float)
    # sem publico nao ha rotulo, e o primeiro ano nao tem ano anterior
    d.loc[d["publico"].isna() | limiar.isna(), "sucesso"] = np.nan
    return d[d["sucesso"].notna()].reset_index(drop=True)


def carregar_xy(quantil=0.75):
    """Devolve X com ATRIBUTOS, y em 0 e 1, e o ano de cada filme.

    O quantil 0.75 e o alvo principal; 0.50 e 0.90 servem a robustez.
    """
    proibidas = set(bd.COLUNAS_PROIBIDAS) & set(ATRIBUTOS)
    assert not proibidas, "coluna proibida entre os atributos: %s" % proibidas
    d = montar(quantil)
    return d[ATRIBUTOS].copy(), d["sucesso"].astype(int), d["ano"].copy()


def folds(gravar=False):
    """Os cinco pares treino e teste, sempre os mesmos.

    Estratificados pelo alvo principal. Todas as combinacoes e a robustez usam
    exatamente estes indices, para que a diferenca entre dois pipelines venha
    so do pre-processamento.
    """
    X, y, _ = carregar_xy()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMENTE)
    pares = list(cv.split(X, y))
    if gravar:
        SAIDA.mkdir(parents=True, exist_ok=True)
        fold = np.empty(len(y), dtype=int)
        for i, (_, teste) in enumerate(pares):
            fold[teste] = i
        pd.DataFrame({"indice": np.arange(len(y)), "fold": fold}).to_csv(
            SAIDA / "folds.csv", index=False)
    return pares


def checar_nao_vazamento(anos=(2005, 2012, 2019)):
    """Prova de que o historico so olha para tras.

    Multiplica por mil o publico de todos os filmes de um ano e confere que
    nenhum historico de filme daquele ano ou anterior muda, e que algum
    historico de ano posterior muda. Se o historico olhasse para o proprio ano,
    a primeira condicao falharia.
    """
    original = bd.carregar()
    antes = {c: historico_de_sucesso(original, e) for c, e in HISTORICOS.items()}
    for t in anos:
        mexida = original.copy()
        mexida.loc[mexida["ano"] == t, "publico"] *= 1000
        ate_t, depois = original["ano"] <= t, original["ano"] > t
        for coluna, entidade in HISTORICOS.items():
            depois_da_mudanca = historico_de_sucesso(mexida, entidade)
            igual = np.isclose(antes[coluna], depois_da_mudanca, equal_nan=True)
            assert igual[ate_t].all(), "%s vaza no ano %d" % (coluna, t)
            assert not igual[depois].all(), "%s nao reage ao ano %d" % (coluna, t)
    return True


def coincidencia_da_ausencia():
    """Quanto a falta de historico coincide com nenhum filme anterior.

    Se coincide quase sempre, a ausencia ja esta dita em outras colunas, e a
    indicadora de ausencia tem pouco a acrescentar ao kNN.
    """
    d = montar()
    contagem = {"hist_diretor": "filmes_diretor_antes",
                "hist_distribuidora": "filmes_distribuidora_antes",
                "hist_produtora": "filmes_produtora_antes"}
    linhas = []
    for coluna, anterior in contagem.items():
        falta, zero = d[coluna].isna(), d[anterior] == 0
        linhas.append({"atributo": coluna,
                       "ausente_%": falta.mean() * 100,
                       "coincide_com_zero_%": (falta == zero).mean() * 100,
                       "ausente_com_filme_antes": int((falta & ~zero).sum())})
    return pd.DataFrame(linhas)


def descrever(gravar=False):
    """Os numeros que a secao 2 do relatorio cita, em arquivo.

    A regra do grupo e que nenhum numero do relatorio seja digitado a mao.
    Entao o que a secao afirma sobre tamanho da base, prevalencia e ausencia
    sai daqui, e nao da tela.
    """
    X, y, ano = carregar_xy()
    por_decada = y.groupby(ano // 10 * 10).mean().round(3)
    falta = (X.isna().mean() * 100).round(2)
    ausencia = coincidencia_da_ausencia().round(2)

    descricao = {
        "filmes_com_alvo": int(len(y)),
        "filmes_sem_alvo": int(len(bd.carregar()) - len(y)),
        "prevalencia_sucesso": round(float(y.mean()), 4),
        "prevalencia_por_decada": {str(k): float(v) for k, v in por_decada.items()},
        "quantil_do_alvo": 0.75,
        "n_atributos": len(ATRIBUTOS),
        "n_numericas": len(NUMERICAS),
        "n_nominais": len(NOMINAIS),
        "n_ordinais": len(ORDINAIS),
        "maior_ausencia_fora_do_historico_%": float(
            falta.drop(index=list(HISTORICOS), errors="ignore").max()),
        "historico_nao_vaza": checar_nao_vazamento(),
    }
    if gravar:
        SAIDA.mkdir(parents=True, exist_ok=True)
        (SAIDA / "base_descricao.json").write_text(
            json.dumps(descricao, indent=2, ensure_ascii=False), encoding="utf-8")
        falta[falta > 0].rename("ausente_%").to_csv(SAIDA / "base_ausencia.csv")
        ausencia.to_csv(SAIDA / "base_ausencia_estrutural.csv", index=False)
    return descricao, falta, ausencia


def resumo():
    descricao, falta, ausencia = descrever(gravar=True)
    print("filmes com alvo: %d" % descricao["filmes_com_alvo"])
    print("prevalencia de sucesso: %.3f" % descricao["prevalencia_sucesso"])
    print("por decada: %s" % descricao["prevalencia_por_decada"])
    print("ausencia por atributo, em %:")
    print(falta[falta > 0].to_string())
    print(ausencia.to_string(index=False))
    print("teste de nao vazamento do historico: %s" % descricao["historico_nao_vaza"])
    folds(gravar=True)
    for nome in ("base_descricao.json", "base_ausencia.csv",
                 "base_ausencia_estrutural.csv", "folds.csv"):
        print("gravado: %s" % (SAIDA / nome).relative_to(RAIZ).as_posix())


if __name__ == "__main__":
    resumo()
