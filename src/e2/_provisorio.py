# -*- coding: utf-8 -*-
"""Versoes simplificadas do pipeline e dos resultados da grade.

Servem para testar a robustez e o anexo enquanto as etapas de normalizacao e
reducao e o arquivo de resultados ainda nao existem. Este arquivo deve ser
apagado quando a grade completa rodar.
"""

import numpy as np
import pandas as pd
from imblearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from e2.base import NOMINAIS, NUMERICAS, ORDINAIS, SEMENTE
from e2.etapas.balanceamento import OPCOES as BALANCEAMENTO

# O pipeline simplificado trata as ordinais como nominais, o que basta para testar.
CATEGORICAS = NOMINAIS + ORDINAIS


def construir_pipeline(config):
    """Monta um pipeline simples em que so o balanceamento varia."""
    pre = ColumnTransformer([
        ("num", SimpleImputer(strategy="median"), NUMERICAS),
        ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"),
                              OneHotEncoder(handle_unknown="ignore")), CATEGORICAS),
    ], sparse_threshold=0)
    return Pipeline([("pre", pre), ("normalizacao", StandardScaler()),
                     ("balanceamento", BALANCEAMENTO[config["balanceamento"]]()),
                     ("knn", KNeighborsClassifier(n_neighbors=7))])


def resultados_sinteticos():
    """Gera resultados aleatorios no mesmo formato da grade, so para testar o codigo."""
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
