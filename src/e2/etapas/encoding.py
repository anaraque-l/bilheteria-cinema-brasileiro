# -*- coding: utf-8 -*-
"""Etapa 2 da grade: encoding. Duas opcoes, nenhuma pode ser pulada.

As duas ordinais recebem sempre o mesmo tratamento, codigo na ordem natural
das faixas. O que varia entre as opcoes e como as quatro nominais viram
numero, e e ai que esta a decisao que importa para o kNN: distribuidora tem
455 categorias, 278 delas com um unico filme.
"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, TargetEncoder

import build_dataset as bd
from e2.base import NOMINAIS, ORDINAIS, SEMENTE

# faixa de 5 a 15 medida na S4 da E1: custa 0,009 de AUC e corta ~380 colunas
MIN_FREQUENCIA = 10


def _ordinais():
    # a categoria ausente so aparece com a imputacao por indicadora, e nao
    # tem lugar na ordem; vira um codigo abaixo de todas as faixas
    return OrdinalEncoder(
        categories=[bd.ORDEM_ORDINAIS[c] for c in ORDINAIS],
        handle_unknown="use_encoded_value", unknown_value=-1,
    )


def _encoder(nominais):
    return ColumnTransformer(
        [("nom", nominais, NOMINAIS), ("ord", _ordinais(), ORDINAIS)],
        remainder="passthrough",
    )


def onehot():
    return _encoder(OneHotEncoder(
        min_frequency=MIN_FREQUENCIA, handle_unknown="infrequent_if_exist",
        sparse_output=False))


def alvo():
    # o ajuste usa validacao cruzada interna, entao nenhum filme de treino e
    # codificado com o proprio rotulo
    return _encoder(TargetEncoder(
        target_type="binary", cv=5, shuffle=True, random_state=SEMENTE))


OPCOES = {
    "onehot": onehot,
    "alvo": alvo,
}

JUSTIFICATIVA = {
    "onehot": (
        "A técnica padrão para nominais. O agrupamento das categorias com menos de "
        "10 filmes sai da S4 da E1, em que a faixa de 5 a 15 custou 0,009 de AUC e "
        "cortou cerca de 380 colunas."),
    "alvo": (
        "Distribuidora tem 455 categorias, 278 com um único filme. Para o kNN cada "
        "coluna é uma dimensão a mais na distância; o encoding pelo alvo põe cada "
        "nominal em uma coluna só, com validação cruzada interna para não vazar o "
        "rótulo do próprio filme."),
}
