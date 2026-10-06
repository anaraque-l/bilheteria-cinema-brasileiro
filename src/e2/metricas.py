# -*- coding: utf-8 -*-
"""Metricas da Entrega 2, iguais para as 144 combinacoes.

Classe positiva e sucesso igual a 1. Com 25,3% de positivos, quem responde
sempre fracasso acerta 0,747 e tem F1 zero, entao a acuracia nao ranqueia
nada. A AUC mede se o modelo ordena bem os filmes, sem depender de limiar.
F1, precisao e revocacao medem o que acontece no limiar padrao de 0,5, que
num kNN com k igual a 7 quer dizer pelo menos 4 dos 7 vizinhos de sucesso.
A average_precision entra como complemento por ser sensivel a prevalencia.
"""

SCORING = {
    "accuracy": "accuracy",
    "f1": "f1",
    "precision": "precision",
    "recall": "recall",
    "roc_auc": "roc_auc",
    "average_precision": "average_precision",
}

# Desempate de ranking: a AUC nao depende de limiar e e a mesma da Entrega 1.
PRINCIPAL = "roc_auc"
CO_PRINCIPAL = "f1"
