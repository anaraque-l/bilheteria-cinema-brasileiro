# -*- coding: utf-8 -*-
"""Monta a tabela do anexo com as 144 combinacoes.

Como executar: python src/e2/anexo.py

Cada linha e uma combinacao, em ordem de id, com as opcoes de cada etapa,
media e desvio de cada metrica, numero de atributos, tempo e erro. Sai em
Markdown para o relatorio e em CSV para importar no Word sem digitar nada.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from e2.espaco import ETAPAS
from e2.metricas import SCORING

RAIZ = Path(__file__).resolve().parents[2]
SAIDA = RAIZ / "reports" / "e2"
ROTULO = {"accuracy": "acurácia", "f1": "F1", "precision": "precisão",
          "recall": "revocação", "roc_auc": "AUC", "average_precision": "AP"}


def tabela(resultados):
    """Formata os resultados da grade como texto pronto para o anexo.

    Os numeros saem com virgula decimal, como no resto do relatorio.
    """
    r = resultados.sort_values("id")
    t = pd.DataFrame({"id": r["id"].astype(int).astype(str)})
    # O baseline e marcado ao lado do id, assim a tabela nao ganha uma coluna so para isso.
    t.loc[r["eh_baseline"].to_numpy() == 1, "id"] += " (base)"
    for e in ETAPAS:
        t[e] = r[e].to_numpy()
    for m in SCORING:
        media, dp = r[f"{m}_media"], r[f"{m}_dp"]
        t[ROTULO[m]] = [("—" if pd.isna(a) else f"{a:.3f} ± {b:.3f}".replace(".", ","))
                        for a, b in zip(media, dp)]
    t["atributos"] = r["n_atributos"].map(lambda v: "—" if pd.isna(v) else f"{v:.0f}").to_numpy()
    t["tempo (s)"] = r["tempo_total_s"].map(lambda v: "—" if pd.isna(v) else f"{v:.1f}".replace(".", ",")).to_numpy()
    t["erro"] = r["erro"].fillna("").to_numpy()
    return t


def para_markdown(t):
    """Converte a tabela em texto Markdown."""
    linhas = ["| " + " | ".join(t.columns) + " |",
              "|" + "---|" * len(t.columns)]
    linhas += ["| " + " | ".join(str(v).replace("|", "\\|") for v in row) + " |"
               for row in t.itertuples(index=False)]
    return "\n".join(linhas) + "\n"


def main(caminho=SAIDA / "resultados.csv"):
    """Le os resultados, monta a tabela e grava as duas versoes."""
    resultados = pd.read_csv(caminho, keep_default_na=True)
    t = tabela(resultados)
    SAIDA.mkdir(parents=True, exist_ok=True)
    if len(t) != 144:
        print(f"ATENCAO: {len(t)} linhas, o esperado e 144.")
    t.to_csv(SAIDA / "anexo_144.csv", index=False, sep=";")
    (SAIDA / "anexo_144.md").write_text(para_markdown(t), encoding="utf-8")
    print(f"anexo com {len(t)} linhas em {SAIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
