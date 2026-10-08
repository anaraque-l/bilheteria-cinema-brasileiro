# -*- coding: utf-8 -*-
"""Etapa 4 da grade: reducao de dimensionalidade. Duas opcoes e a referencia.

Vem depois da normalizacao e antes do balanceamento, para que PCA e selecao sejam
ajustados so com filmes reais. Com one-hot chegam perto de 80 colunas ao kNN, e
em dimensao alta as distancias se parecem: o vizinho mais proximo deixa de ser
muito mais proximo que o mais distante.
"""

from functools import partial

from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, mutual_info_classif

from e2.base import SEMENTE

# o mesmo numero de colunas nos dois encodings, para que as 10 melhores signifiquem a
# mesma coisa para o kNN; o encoding pelo alvo entrega 18, o menor caso da grade
K_MELHORES = 10

OPCOES = {
    "sem": lambda: "passthrough",
    # o svd completo e deterministico, entao nao precisa de semente
    "pca": lambda: PCA(n_components=0.95, svd_solver="full"),
    # a informacao mutua sorteia vizinhos ao estimar, por isso a semente
    "kbest": lambda: SelectKBest(partial(mutual_info_classif, random_state=SEMENTE),
                                 k=K_MELHORES),
}

JUSTIFICATIVA = {
    "sem": (
        "Testa a H13 da Entrega 1, não aplicar PCA, agora com um modelo sensível à "
        "dimensão; a H13 foi medida com floresta, que não é."),
    "pca": (
        "Com one-hot a matriz chega a cerca de 80 colunas, muitas quase vazias. Guardar "
        "95% da variância é o corte usual e dispensa escolher um número de componentes "
        "por combinação."),
    "kbest": (
        "A Entrega 1 achou atributos que dizem quase o mesmo, como filmes_diretor_antes e "
        "experiencia_da_direcao, e no kNN um atributo ruidoso pesa tanto quanto um útil. "
        "Informação mútua e não teste F porque a relação que importa ao kNN não precisa "
        "ser linear."),
}
