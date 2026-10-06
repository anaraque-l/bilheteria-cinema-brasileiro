# -*- coding: utf-8 -*-
"""Como medimos o acerto das 144 combinacoes.

O filme de sucesso e a classe positiva. Como so um em cada quatro filmes e
sucesso, um modelo que chuta sempre fracasso ja acerta 74,7% das vezes sem
ter aprendido nada. Por isso a acuracia sozinha engana neste problema.

As metricas se dividem em duas familias:
  - a AUC olha se o modelo coloca os sucessos acima dos fracassos quando
    ordena os filmes, sem precisar escolher um ponto de corte;
  - F1, precisao e revocacao olham a decisao final do modelo. No kNN com
    7 vizinhos, o filme e previsto como sucesso quando pelo menos 4 dos 7
    vizinhos sao sucesso.

A precisao media completa o quadro porque leva em conta quantos positivos
existem na base.
"""

SCORING = {
    "accuracy": "accuracy",
    "f1": "f1",
    "precision": "precision",
    "recall": "recall",
    "roc_auc": "roc_auc",
    "average_precision": "average_precision",
}

# A AUC ordena as combinacoes porque nao depende do ponto de corte e e a mesma
# metrica da Entrega 1. O F1 vem logo atras porque e onde o balanceamento aparece.
PRINCIPAL = "roc_auc"
CO_PRINCIPAL = "f1"
