# -*- coding: utf-8 -*-
"""Etapa 1 da grade: valores ausentes. Duas opcoes, nenhuma pode ser pulada.

O kNN nao calcula distancia com NaN, entao nao existe a opcao de nao tratar.
A ausencia relevante nesta base e a dos historicos de sucesso, perto de 68%
para direcao: ela e estrutural, quer dizer que a entidade nunca lancou filme.
Fora deles, a maior ausencia entre os atributos fica abaixo de 0,5%.
"""

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

from e2.base import NOMINAIS, NUMERICAS, ORDINAIS


def _imputador(numericas, categoricas):
    t = ColumnTransformer(
        [("num", numericas, NUMERICAS), ("cat", categoricas, NOMINAIS + ORDINAIS)],
        verbose_feature_names_out=False,
    )
    # o encoding seguinte escolhe as colunas pelo nome
    return t.set_output(transform="pandas")


def mediana_moda():
    return _imputador(SimpleImputer(strategy="median"),
                      SimpleImputer(strategy="most_frequent"))


def mediana_indicadora():
    return _imputador(SimpleImputer(strategy="median", add_indicator=True),
                      SimpleImputer(strategy="constant", fill_value="ausente"))


OPCOES = {
    "mediana_moda": mediana_moda,
    "mediana_indicadora": mediana_indicadora,
}

JUSTIFICATIVA = {
    "mediana_moda": (
        "A imputação mais elementar. Mediana e não média porque é robusta à cauda "
        "das contagens de fomento; nos históricos, que já estão em log e são quase "
        "simétricos, as duas praticamente coincidem."),
    "mediana_indicadora": (
        "A E1 separou a ausência em quatro naturezas e mostrou que ausência pode "
        "ser informação, como em max_salas e em coproducao. Nos históricos ela é "
        "estrutural, nenhum filme anterior, e a indicadora deixa o kNN ver isso em "
        "vez de tratar o estreante como alguém de reputação mediana."),
}
