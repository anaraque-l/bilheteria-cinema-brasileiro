# -*- coding: utf-8 -*-
"""Etapa 3 da grade: normalizacao. Tres opcoes e a referencia sem normalizar.

Age na matriz inteira que sai do encoding: numericas, ordinais codificadas,
dummies do one-hot ou colunas do encoding pelo alvo, e indicadoras de ausencia.
O kNN mede distancia euclidiana nessa matriz, entao a coluna de maior amplitude
decide quem e vizinho: ano vai de 1996 a 2024, filmes_distribuidora_antes de 0 a
179, e as binarias de 0 a 1.
"""

from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

OPCOES = {
    "sem": lambda: "passthrough",
    "padrao": lambda: StandardScaler(),
    "minmax": lambda: MinMaxScaler(),
    "robusto": lambda: RobustScaler(),
}

JUSTIFICATIVA = {
    "sem": (
        "Referência: mede se as escalas cruas já servem ao kNN, em que ano vai de "
        "1996 a 2024 e as binárias de 0 a 1."),
    "padrao": (
        "Põe todas as colunas na mesma escala de desvio. O custo aparece no one-hot: "
        "uma dummy presente em 1% dos filmes passa a valer 9,9 quando é 1, e a "
        "categoria rara domina a distância."),
    "minmax": (
        "Leva tudo a [0, 1] sem mexer nas dummies, que continuam 0 e 1. É sensível ao "
        "máximo: com filmes_distribuidora_antes indo a 179 e mediana 10, a maioria dos "
        "filmes fica perto de 0 nessa coluna."),
    "robusto": (
        "Centra na mediana e divide pelo intervalo interquartil, pensado para as "
        "contagens de filmes anteriores, com assimetria de 2,0 a 3,8. Numa dummy rara o "
        "intervalo é 0, o scikit-learn usa escala 1 e a dummy fica como está."),
}
