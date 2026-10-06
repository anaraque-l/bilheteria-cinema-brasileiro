# -*- coding: utf-8 -*-
"""Roda as tres checagens de robustez e salva tabelas e figuras.

Como executar: python src/robustez_e2.py

O que sai em reports/e2: uma tabela para cada checagem e uma com a
correlacao entre os rankings. Em reports/figuras/e2 saem dois graficos.

Enquanto os modulos da base e do pipeline ainda nao existem, o script usa
versoes simplificadas e avisa no final. Os numeros dessas rodadas servem
so para testar o codigo e nao entram no relatorio.
"""

import sys
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e2 import robustez as rb
from e2.metricas import PRINCIPAL

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "reports" / "e2"
FIGURAS = RAIZ / "reports" / "figuras" / "e2"
QUANTIS = [0.50, 0.75, 0.90]

PROVISORIO = False
try:
    from e2.base import carregar_xy, folds
    from e2.espaco import construir_pipeline
except ImportError:
    PROVISORIO = True
    from e2._provisorio import carregar_xy, construir_pipeline, folds


def carregar_resultados():
    """Le os resultados da grade, ou usa numeros de teste se eles ainda nao existem."""
    caminho = SAIDA / "resultados.csv"
    if caminho.exists():
        return pd.read_csv(caminho)
    global PROVISORIO
    PROVISORIO = True
    from e2._provisorio import resultados_sinteticos
    return resultados_sinteticos()


def main():
    """Roda as tres checagens para cada combinacao escolhida e grava tudo."""
    warnings.filterwarnings("ignore")
    SAIDA.mkdir(parents=True, exist_ok=True)
    FIGURAS.mkdir(parents=True, exist_ok=True)
    escolhidas = rb.selecionar(carregar_resultados())
    pares = folds()
    base = {q: carregar_xy(quantil=q) for q in QUANTIS}

    temp, lim, gen = [], [], []
    for _, linha in escolhidas.iterrows():
        config = {e: linha[e] for e in rb.ETAPAS}
        cid = int(linha["id"])
        pipe = construir_pipeline(config)
        X, y, ano = base[0.75]
        temp.append({"id": cid, **rb.temporal(pipe, X, y, ano)})
        gen += [{"id": cid, **g} for g in rb.por_genero(pipe, X, y, pares)]
        for q in QUANTIS:
            Xq, yq, _ = base[q]
            lim += [{"id": cid, "quantil": q, **f} for f in rb.por_fold(pipe, Xq, yq, pares)]
        print(f"combinacao {cid} ok")

    lim = pd.DataFrame(lim)
    temp = pd.DataFrame(temp)
    cv = lim[lim["quantil"] == 0.75].groupby("id")[PRINCIPAL].mean().rename("roc_auc_5fold")
    temp = temp.merge(cv, on="id")
    temp["otimismo_5fold"] = temp["roc_auc_5fold"] - temp["roc_auc"]

    meta = escolhidas.assign(codigo=escolhidas[rb.ETAPAS].astype(str).agg("|".join, axis=1))
    temp = meta.merge(temp, on="id")
    temp.to_csv(SAIDA / "robustez_temporal.csv", index=False)
    meta.merge(lim, on="id").to_csv(SAIDA / "robustez_limiar.csv", index=False)
    meta.merge(pd.DataFrame(gen), on="id").to_csv(SAIDA / "robustez_genero.csv", index=False)
    rb.correlacao_rankings(lim).to_csv(SAIDA / "robustez_limiar_spearman.csv", index=False)

    figura_limiar(lim)
    figura_temporal(temp)
    if PROVISORIO:
        print("ATENCAO: rodada provisoria, com substitutos locais. Nao cite estes numeros.")


def figura_limiar(lim):
    """Uma linha por combinacao mostrando sua posicao no ranking em P50, P75 e P90.

    Linhas retas indicam que a posicao nao muda com o corte.
    """
    rank = (lim.groupby(["quantil", "id"])[PRINCIPAL].mean()
               .groupby(level=0).rank(ascending=False).unstack(0))
    fig, ax = plt.subplots(figsize=(6, 4.5))
    for _, r in rank.iterrows():
        ax.plot(range(len(QUANTIS)), r.values, marker="o", color="0.4", lw=1)
        ax.annotate(str(r.name), (len(QUANTIS) - 1, r.values[-1]), xytext=(4, 0),
                    textcoords="offset points", va="center", fontsize=7)
    ax.set_xticks(range(len(QUANTIS)), [f"P{int(q * 100)}" for q in QUANTIS])
    ax.invert_yaxis()
    ax.set_ylabel("posição no ranking por AUC")
    ax.set_title("O ranking muda com o corte do alvo?")
    fig.tight_layout()
    fig.savefig(FIGURAS / "fig-lf-ranking-limiar.png", dpi=150)
    plt.close(fig)


def figura_temporal(temp):
    """Compara a AUC do 5-fold com a AUC da validacao temporal.

    Pontos abaixo da diagonal indicam que o 5-fold mostrou um resultado
    melhor do que o modelo teria prevendo o futuro.
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(temp["roc_auc_5fold"], temp["roc_auc"], color="0.2")
    for _, r in temp.iterrows():
        ax.annotate(str(r["id"]), (r["roc_auc_5fold"], r["roc_auc"]),
                    xytext=(3, 3), textcoords="offset points", fontsize=7)
    lo = min(temp["roc_auc_5fold"].min(), temp["roc_auc"].min()) - 0.01
    hi = max(temp["roc_auc_5fold"].max(), temp["roc_auc"].max()) + 0.01
    ax.plot([lo, hi], [lo, hi], ls="--", color="0.6")
    ax.set_xlim(lo, hi), ax.set_ylim(lo, hi)
    ax.set_xlabel("AUC no 5-fold aleatório")
    ax.set_ylabel(f"AUC temporal, teste ≥ {rb.ULTIMO_ANO_TREINO + 1}")
    ax.set_title("Abaixo da diagonal, o 5-fold é otimista")
    fig.tight_layout()
    fig.savefig(FIGURAS / "fig-lf-auc-5fold-temporal.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
