# -*- coding: utf-8 -*-
"""Leitura das 144 combinacoes: empate, ranking, efeito de cada etapa, interacoes e custo.

Toda funcao recebe o DataFrame de reports/e2/resultados.csv. A regra de empate do
enunciado mora aqui e so aqui: duas combinacoes empatam numa metrica quando a
diferenca das medias e menor que o maior dos dois desvios entre folds.

O efeito de uma etapa e lido de dois jeitos. A media por opcao e o que o enunciado
pede, mas mistura contextos bons e ruins. A leitura pareada fixa as outras quatro
etapas, compara a opcao com a de referencia dentro de cada contexto e conta
vitorias, empates e derrotas pela regra de empate.
"""

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from e2.espaco import BASELINE, ETAPAS

# mesma paleta das figuras da Entrega 1, definida no script da auditoria do alvo
COR, COR2, CINZA = "#2b6cb0", "#c05621", "#4a5568"


def empata(a, b, m):
    """Regra de empate na metrica m.

    a e b sao duas linhas de resultados, ou duas tabelas alinhadas linha a linha;
    no segundo caso a resposta vem linha a linha.
    """
    return np.abs(a[m + "_media"] - b[m + "_media"]) < np.maximum(a[m + "_dp"], b[m + "_dp"])


def validas(res):
    """So as combinacoes que rodaram. As que falharam continuam no anexo."""
    return res[res["erro"].isna()]


def ranking(res, m="roc_auc"):
    """As combinacoes da melhor para a pior, com quem empata com a melhor e com o baseline."""
    r = validas(res).sort_values(m + "_media", ascending=False).reset_index(drop=True)
    melhor = r.iloc[0]
    baseline = r[r["eh_baseline"] == 1].iloc[0]
    r.insert(0, "posicao", range(1, len(r) + 1))
    r["empata_com_a_melhor"] = r.apply(lambda linha: bool(empata(linha, melhor, m)), axis=1)
    r["empata_com_o_baseline"] = r.apply(lambda linha: bool(empata(linha, baseline, m)), axis=1)
    return r[["posicao", "id", "codigo", m + "_media", m + "_dp",
              "empata_com_a_melhor", "empata_com_o_baseline"]]


def melhores_piores(res, m="roc_auc", n=10):
    """As n primeiras e as n ultimas do ranking."""
    r = ranking(res, m)
    return pd.concat([r.head(n).assign(grupo="melhores"), r.tail(n).assign(grupo="piores")])


def _compara(com, contra, m):
    """Compara duas tabelas alinhadas por contexto e conta o resultado de cada par."""
    iguais = empata(com, contra, m)
    ganho = com[m + "_media"] - contra[m + "_media"]
    return {"vitorias": int(((ganho > 0) & ~iguais).sum()),
            "empates": int(iguais.sum()),
            "derrotas": int(((ganho < 0) & ~iguais).sum()),
            "ganho_medio": float(ganho.mean())}


def efeito_por_etapa(res, etapa, m="roc_auc"):
    """Media por opcao e comparacao pareada de cada opcao contra a de referencia.

    A referencia e a opcao do baseline: sem normalizar, sem reduzir, sem balancear,
    mediana e moda, e one-hot.
    """
    referencia = BASELINE[etapa]
    contexto = [e for e in ETAPAS if e != etapa]
    tabela = validas(res).set_index(contexto)
    contra = tabela[tabela[etapa] == referencia]
    linhas = []
    for opcao, com in tabela.groupby(etapa):
        linha = {"etapa": etapa, "opcao": opcao, "referencia": opcao == referencia,
                 "media": com[m + "_media"].mean(), "combinacoes": len(com)}
        if opcao != referencia:
            pares = com.index.intersection(contra.index)
            linha.update(_compara(com.loc[pares], contra.loc[pares], m))
        linhas.append(linha)
    return pd.DataFrame(linhas)


def interacoes(res, etapa_a, etapa_b, m="roc_auc"):
    """Efeito de cada opcao de etapa_a contra a referencia, separado por opcao de etapa_b.

    O veredito de cada linha e o resultado mais frequente nos pares; numa igualdade
    vale empate, que e o lado conservador. Ha interacao quando o veredito de uma opcao
    de etapa_a muda conforme a opcao de etapa_b.
    """
    referencia = BASELINE[etapa_a]
    resto = [e for e in ETAPAS if e not in (etapa_a, etapa_b)]
    linhas = []
    for opcao_b, sub in validas(res).groupby(etapa_b):
        tabela = sub.set_index(resto)
        contra = tabela[tabela[etapa_a] == referencia]
        for opcao_a, com in tabela[tabela[etapa_a] != referencia].groupby(etapa_a):
            pares = com.index.intersection(contra.index)
            linhas.append({"etapa_a": etapa_a, "opcao_a": opcao_a,
                           "etapa_b": etapa_b, "opcao_b": opcao_b,
                           **_compara(com.loc[pares], contra.loc[pares], m)})
    tabela = pd.DataFrame(linhas)
    contagens = tabela[["empates", "vitorias", "derrotas"]]
    tabela["veredito"] = contagens.idxmax(axis=1).map(
        {"empates": "empata", "vitorias": "vence", "derrotas": "perde"})
    muda = tabela.groupby("opcao_a")["veredito"].nunique() > 1
    tabela["interacao"] = tabela["opcao_a"].map(muda)
    return tabela


def custo(res):
    """Tempo medio por opcao de cada etapa, as 10 mais caras e a relacao com a dimensao."""
    r = validas(res)
    por_opcao = pd.concat([
        r.groupby(e)["tempo_total_s"].mean().rename("tempo_medio_s")
         .rename_axis("opcao").reset_index().assign(etapa=e)
        for e in ETAPAS])[["etapa", "opcao", "tempo_medio_s"]]
    mais_caras = r.nlargest(10, "tempo_total_s")[["id", "codigo", "n_atributos", "tempo_total_s"]]
    rho = spearmanr(r["n_atributos"], r["tempo_total_s"])[0]
    return por_opcao, mais_caras, float(rho)


# ---------------------------------------------------------------------------
# Figuras
# ---------------------------------------------------------------------------

def figuras(res, destino, m="roc_auc"):
    """Grava as quatro figuras fig-al-* em destino e devolve os caminhos."""
    import matplotlib.pyplot as plt

    plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 160, "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.grid": True, "grid.alpha": .25, "grid.linewidth": .6})
    destino.mkdir(parents=True, exist_ok=True)
    caminhos = []

    # 1. as combinacoes em ordem, com o desvio e quem empata com a melhor
    r = ranking(res, m)
    fig, ax = plt.subplots(figsize=(11, 4))
    cores = np.where(r["empata_com_a_melhor"], COR, CINZA)
    ax.errorbar(r["posicao"], r[m + "_media"], yerr=r[m + "_dp"], fmt="none",
                ecolor="#cbd5e0", lw=.8)
    ax.scatter(r["posicao"], r[m + "_media"], c=cores, s=14, zorder=3)
    base = r[r["id"] == res.loc[res["eh_baseline"] == 1, "id"].iloc[0]]
    ax.scatter(base["posicao"], base[m + "_media"], color=COR2, s=60, zorder=4,
               label="baseline, posição %d" % base["posicao"].iloc[0])
    ax.scatter([], [], color=COR, s=14, label="empata com a melhor")
    ax.set_xlabel("posição no ranking")
    ax.set_ylabel("AUC média nos 5 folds")
    ax.set_title("As combinações da melhor para a pior", loc="left", fontweight="bold")
    ax.legend(frameon=False, loc="lower left")
    caminhos.append(_salva(fig, destino / "fig-al-ranking.png"))

    # 2. ganho pareado de cada opcao contra a referencia da sua etapa
    efeitos = pd.concat([efeito_por_etapa(res, e, m) for e in ETAPAS])
    efeitos = efeitos[~efeitos["referencia"]].iloc[::-1]
    rotulos = efeitos["etapa"] + ": " + efeitos["opcao"]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(rotulos, efeitos["ganho_medio"],
            color=np.where(efeitos["ganho_medio"] >= 0, COR, COR2))
    for y, (_, e) in enumerate(efeitos.iterrows()):
        ax.annotate("%dV %dE %dD" % (e["vitorias"], e["empates"], e["derrotas"]),
                    (0, y), xytext=(4 if e["ganho_medio"] < 0 else -4, 0),
                    textcoords="offset points", va="center", fontsize=8, color=CINZA,
                    ha="left" if e["ganho_medio"] < 0 else "right")
    ax.axvline(0, color=CINZA, lw=1)
    ax.set_xlabel("ganho médio de AUC contra a opção de referência, nos mesmos contextos")
    ax.set_title("Efeito de cada opção, comparado par a par", loc="left", fontweight="bold")
    caminhos.append(_salva(fig, destino / "fig-al-efeitos.png"))

    # 3. tres interacoes em mapa de calor, com a AUC media de cada cruzamento
    pares = [("normalizacao", "encoding"), ("reducao", "normalizacao"),
             ("balanceamento", "encoding")]
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
    for ax, (a, b) in zip(axes, pares):
        tabela = validas(res).pivot_table(values=m + "_media", index=a, columns=b, aggfunc="mean")
        im = ax.imshow(tabela.to_numpy(), cmap="Blues", aspect="auto")
        ax.set_xticks(range(tabela.shape[1]), tabela.columns)
        ax.set_yticks(range(tabela.shape[0]), tabela.index)
        for i in range(tabela.shape[0]):
            for j in range(tabela.shape[1]):
                ax.text(j, i, "%.3f" % tabela.iat[i, j], ha="center", va="center", fontsize=8)
        ax.set_xlabel(b)
        ax.set_ylabel(a)
        ax.grid(False)
        fig.colorbar(im, ax=ax, shrink=.8)
    fig.suptitle("AUC média em cada cruzamento de duas etapas", x=.01, ha="left",
                 fontweight="bold")
    caminhos.append(_salva(fig, destino / "fig-al-interacoes.png"))

    # 4. tempo contra numero de colunas que chegam ao kNN, por opcao de reducao
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for opcao, cor in zip(["sem", "pca", "kbest"], [CINZA, COR, COR2]):
        sub = validas(res)[validas(res)["reducao"] == opcao]
        ax.scatter(sub["n_atributos"], sub["tempo_total_s"], color=cor, s=16, label=opcao)
    ax.set_xlabel("colunas que chegam ao kNN, média dos folds")
    ax.set_ylabel("tempo total nos 5 folds, em segundos")
    ax.set_title("Custo de cada combinação", loc="left", fontweight="bold")
    ax.legend(title="redução", frameon=False)
    caminhos.append(_salva(fig, destino / "fig-al-custo.png"))
    return caminhos


def _salva(fig, caminho):
    import matplotlib.pyplot as plt
    fig.tight_layout()
    fig.savefig(caminho, bbox_inches="tight")
    plt.close(fig)
    return caminho
