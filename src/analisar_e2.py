# -*- coding: utf-8 -*-
"""Gera as tabelas e as figuras da analise das 144 combinacoes.

Executar: python src/analisar_e2.py

Le reports/e2/resultados.csv, gravado por executar_e2.py, e grava em reports/e2 os
arquivos analise_*.csv e em reports/figuras/e2 as figuras fig-al-*.png. A AUC
ordena as combinacoes; o F1 entra nas tabelas de efeito porque e onde o
balanceamento aparece.
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e2 import analise  # noqa: E402
from e2.espaco import ETAPAS  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "reports" / "e2"
FIGURAS = RAIZ / "reports" / "figuras" / "e2"
METRICAS = ["roc_auc", "f1"]

# os cruzamentos que a secao 5.3 discute
PARES = [("normalizacao", "encoding"), ("reducao", "normalizacao"),
         ("balanceamento", "encoding"), ("balanceamento", "normalizacao"),
         ("ausentes", "encoding")]


def main():
    res = pd.read_csv(SAIDA / "resultados.csv")
    rodaram = analise.validas(res)
    print("%d combinacoes, %d com erro" % (len(res), len(res) - len(rodaram)))

    ranking = analise.ranking(res)
    ranking.to_csv(SAIDA / "analise_ranking.csv", index=False)
    analise.melhores_piores(res).to_csv(SAIDA / "analise_melhores_piores.csv", index=False)

    efeitos = pd.concat([analise.efeito_por_etapa(res, e, m).assign(metrica=m)
                         for m in METRICAS for e in ETAPAS])
    efeitos.to_csv(SAIDA / "analise_efeitos.csv", index=False)

    interacoes = pd.concat([analise.interacoes(res, a, b, m).assign(metrica=m)
                            for m in METRICAS for a, b in PARES])
    interacoes.to_csv(SAIDA / "analise_interacoes.csv", index=False)

    por_opcao, mais_caras, rho = analise.custo(res)
    por_opcao.to_csv(SAIDA / "analise_custo_por_opcao.csv", index=False)
    mais_caras.to_csv(SAIDA / "analise_custo_mais_caras.csv", index=False)

    for caminho in analise.figuras(res, FIGURAS):
        print("gravado: %s" % caminho.relative_to(RAIZ).as_posix())

    melhor = ranking.iloc[0]
    base = ranking[ranking["id"] == res.loc[res["eh_baseline"] == 1, "id"].iloc[0]].iloc[0]
    print("\nmelhor: %s, AUC %.3f +- %.3f" % (melhor["codigo"], melhor["roc_auc_media"],
                                             melhor["roc_auc_dp"]))
    print("baseline: posicao %d, AUC %.3f +- %.3f" % (base["posicao"], base["roc_auc_media"],
                                                    base["roc_auc_dp"]))
    print("empatam com a melhor: %d" % ranking["empata_com_a_melhor"].sum())
    print("tempo x colunas que chegam ao kNN, Spearman: %.2f" % rho)
    print("\nefeito pareado na AUC, contra a opcao de referencia:")
    auc = efeitos[(efeitos["metrica"] == "roc_auc") & ~efeitos["referencia"]]
    for _, e in auc.iterrows():
        print("  %-14s %-19s ganho %+.3f  %2dV %2dE %2dD"
              % (e["etapa"], e["opcao"], e["ganho_medio"], e["vitorias"], e["empates"],
                 e["derrotas"]))
    print("\ninteracoes na AUC, onde o veredito muda conforme a outra etapa:")
    marcadas = interacoes[(interacoes["metrica"] == "roc_auc") & interacoes["interacao"]]
    for (a, b, opcao), grupo in marcadas.groupby(["etapa_a", "etapa_b", "opcao_a"]):
        vereditos = ", ".join("%s: %s" % (o, v) for o, v in zip(grupo["opcao_b"], grupo["veredito"]))
        print("  %s %s, por %s -> %s" % (a, opcao, b, vereditos))


if __name__ == "__main__":
    main()
