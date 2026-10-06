# -*- coding: utf-8 -*-
"""Tabela completa do anexo: as 144 combinacoes, uma linha cada, por id.

Executar: python src/e2/anexo.py

Gera Markdown para o relatorio e CSV ja formatado, que entra no docx sem
copiar e colar a mao, porque tabela colada e tabela quebrada.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from e2.metricas import SCORING

RAIZ = Path(__file__).resolve().parents[2]
SAIDA = RAIZ / "reports" / "e2"
ETAPAS = ["ausentes", "encoding", "normalizacao", "reducao", "balanceamento"]
# Virgula decimal, como no texto do relatorio.
ROTULO = {"accuracy": "acurácia", "f1": "F1", "precision": "precisão",
          "recall": "revocação", "roc_auc": "AUC", "average_precision": "AP"}


def tabela(resultados):
    r = resultados.sort_values("id")
    t = pd.DataFrame({"id": r["id"].astype(int).astype(str)})
    # O baseline e marcado no proprio id para nao gastar uma coluna inteira.
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
    linhas = ["| " + " | ".join(t.columns) + " |",
              "|" + "---|" * len(t.columns)]
    linhas += ["| " + " | ".join(str(v).replace("|", "\\|") for v in row) + " |"
               for row in t.itertuples(index=False)]
    return "\n".join(linhas) + "\n"


def main(caminho=SAIDA / "resultados.csv"):
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
