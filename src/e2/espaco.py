# -*- coding: utf-8 -*-
"""O espaco de combinacoes e a montagem de cada pipeline.

A ordem das etapas dentro do fold e uma decisao, nao um detalhe:
  ausentes -> encoding -> normalizacao -> reducao -> balanceamento -> kNN

  - ausentes antes de encoding: o encoder nao aceita NaN, e a categoria
    "ausente" precisa existir antes de virar coluna;
  - normalizacao depois de encoding: o kNN mede distancia na matriz inteira,
    dummies incluidas, e e essa matriz que precisa estar em escala;
  - reducao antes de balanceamento: PCA e selecao sao ajustados so com filmes
    reais, nunca com pontos sinteticos do SMOTE;
  - balanceamento por ultimo: o SMOTE interpola no mesmo espaco em que o kNN
    vai medir distancia.

O Pipeline e o do imbalanced-learn porque so ele aceita um sampler no meio, e
o sampler so age no ajuste: o fold de teste nunca e reamostrado.
"""

import importlib
import itertools

from imblearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier

ETAPAS = ["ausentes", "encoding", "normalizacao", "reducao", "balanceamento"]

BASELINE = {
    "ausentes": "mediana_moda",
    "encoding": "onehot",
    "normalizacao": "sem",
    "reducao": "sem",
    "balanceamento": "sem",
}

# fixo pelo enunciado, para que toda diferenca venha do pre-processamento
K_VIZINHOS = 7


def opcoes(etapa):
    """OPCOES do modulo da etapa. Importado sob demanda: cada etapa tem dona."""
    return importlib.import_module("e2.etapas.%s" % etapa).OPCOES


def combinacoes():
    """As combinacoes em ordem estavel, cada uma com id a partir de 1."""
    listas = [list(opcoes(etapa)) for etapa in ETAPAS]
    saida = []
    for i, escolha in enumerate(itertools.product(*listas), start=1):
        config = dict(zip(ETAPAS, escolha))
        config["id"] = i
        saida.append(config)
    return saida


def codigo(config):
    return "|".join(config[etapa] for etapa in ETAPAS)


def eh_baseline(config):
    return all(config[etapa] == BASELINE[etapa] for etapa in ETAPAS)


def construir_pipeline(config):
    passos = [(etapa, opcoes(etapa)[config[etapa]]()) for etapa in ETAPAS]
    return Pipeline(passos + [("knn", KNeighborsClassifier(n_neighbors=K_VIZINHOS))])
