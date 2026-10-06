# -*- coding: utf-8 -*-
"""Etapa de balanceamento, a ultima antes do kNN.

Os samplers do imbalanced-learn so agem no fit do Pipeline, entao o fold de
teste nunca e reamostrado. E por isso que a dependencia existe.

Considerados e descartados:
  RandomOverSampler duplica sucessos, e uma copia repetida pode ocupar varios
  dos 7 vizinhos de um filme de teste, viciando o voto.
  SMOTENC exige as colunas antes do encoding, e a ordem do grupo poe o
  balanceamento depois da reducao, para que PCA e selecao vejam so filmes reais.
  ADASYN e Tomek ficaram fora do que foi visto em sala, sem ganho de argumento.
"""

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

try:
    from e2.base import SEMENTE
except ImportError:
    # Enquanto base.py nao chega a main; o valor e o mesmo do contrato.
    SEMENTE = 42

OPCOES = {
    "sem": lambda: "passthrough",
    "subamostragem": lambda: RandomUnderSampler(random_state=SEMENTE),
    # Cinco vizinhos e o padrao da biblioteca e cabe folgado nos ~520 sucessos de cada fold de treino.
    "smote": lambda: SMOTE(k_neighbors=5, random_state=SEMENTE),
}

JUSTIFICATIVA = {
    "sem": (
        "Referencia: e a H10 da Entrega 1, que valia para o alvo na mediana, "
        "agora testada num alvo P75 em que ela pode falhar."
    ),
    "subamostragem": (
        "Com 25,3% de positivos e sem class_weight no kNN, mudar a proporcao do "
        "treino e o unico jeito de mudar a votacao; o custo e descartar cerca de "
        "metade dos filmes, e o kNN depende de densidade."
    ),
    "smote": (
        "Cria sucessos sinteticos interpolando entre sucessos vizinhos sem jogar "
        "dado fora; o custo e que em espaco one-hot a interpolacao gera dummies "
        "fracionarias de filmes que nao existem."
    ),
}
