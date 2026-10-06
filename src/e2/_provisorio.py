# -*- coding: utf-8 -*-
"""Substitutos locais de base.py, espaco.py e resultados.csv.

Existem so para a robustez e o anexo andarem antes do motor da Ana Raquel.
Apagar quando base.py, espaco.py e resultados.csv estiverem em main.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from imblearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from e2.etapas.balanceamento import OPCOES as BALANCEAMENTO

SEMENTE = 42
ARQUIVO = Path(__file__).resolve().parents[2] / "data" / "processed" / "filmes.csv"

# Sem os hist_*, que sao calculados em base.py.
NUMERICAS = ["ano", "filmes_diretor_antes", "filmes_distribuidora_antes",
             "filmes_produtora_antes", "coproducao", "recebeu_fsa",
             "recebeu_incentivo", "contratos_fsa", "projetos_incentivo"]
CATEGORICAS = ["genero", "uf_maj", "distribuidora", "origem_do_fomento",
               "experiencia_da_direcao", "porte_da_distribuidora"]


def carregar_xy(quantil=0.75):
    """Alvo de D-E2-1: publico acima do quantil dos filmes do ano anterior."""
    d = pd.read_csv(ARQUIVO)
    d = d[d["publico"].notna()]
    corte = d.groupby("ano")["publico"].quantile(quantil)
    d = d.assign(corte=d["ano"].map(lambda a: corte.get(a - 1, np.nan)))
    d = d[d["corte"].notna()].reset_index(drop=True)
    y = (d["publico"] > d["corte"]).astype(int)
    return d[NUMERICAS + CATEGORICAS], y, d["ano"]


def folds():
    X, y, _ = carregar_xy()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMENTE)
    return list(cv.split(X, y))


def construir_pipeline(config):
    """Pipeline minimo: so a etapa de balanceamento segue a configuracao."""
    pre = ColumnTransformer([
        ("num", SimpleImputer(strategy="median"), NUMERICAS),
        ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"),
                              OneHotEncoder(handle_unknown="ignore")), CATEGORICAS),
    ], sparse_threshold=0)
    return Pipeline([("pre", pre), ("normalizacao", StandardScaler()),
                     ("balanceamento", BALANCEAMENTO[config["balanceamento"]]()),
                     ("knn", KNeighborsClassifier(n_neighbors=7))])


def resultados_sinteticos():
    """CSV no formato A.6 com numeros aleatorios, so para testar o encanamento."""
    import itertools
    opcoes = [["mediana_moda", "mediana_indicadora"], ["onehot", "alvo"],
              ["sem", "padrao", "minmax", "robusto"], ["sem", "pca", "kbest"],
              ["sem", "subamostragem", "smote"]]
    etapas = ["ausentes", "encoding", "normalizacao", "reducao", "balanceamento"]
    rng = np.random.default_rng(SEMENTE)
    linhas = []
    for i, combo in enumerate(itertools.product(*opcoes), start=1):
        linha = {"id": i, "codigo": "|".join(combo), **dict(zip(etapas, combo)),
                 "eh_baseline": int(i == 1)}
        for m in ["accuracy", "f1", "precision", "recall", "roc_auc", "average_precision"]:
            linha[f"{m}_media"] = rng.uniform(0.3, 0.85)
            linha[f"{m}_dp"] = rng.uniform(0.005, 0.03)
        linha.update(n_atributos=rng.integers(10, 500), tempo_total_s=rng.uniform(0.5, 10),
                     tempo_ajuste_medio_s=rng.uniform(0.05, 2), erro="")
        linhas.append(linha)
    return pd.DataFrame(linhas)
