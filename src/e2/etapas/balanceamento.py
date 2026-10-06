# -*- coding: utf-8 -*-
"""Balanceamento: igualar sucessos e fracassos antes de o kNN votar.

Para que serve. Na base ha tres fracassos para cada sucesso. O kNN decide
pelo voto dos 7 vizinhos mais proximos, entao na maioria dos bairros os
fracassos ganham a votacao e o modelo quase nao preve sucesso. Mudar a
proporcao das classes no treino e a unica forma de mexer nesse voto, porque
o kNN nao aceita peso por classe.

Por que nao contamina o teste. A biblioteca imbalanced-learn so reamostra
durante o treino do pipeline. Na hora de avaliar, os filmes de teste passam
direto, sem nenhum filme removido ou inventado.

As tres opcoes:
  - sem: deixa a base como esta e serve de referencia;
  - subamostragem: sorteia e remove fracassos ate igualar as classes;
  - smote: cria sucessos novos no meio do caminho entre dois sucessos parecidos.

Opcoes que ficaram de fora:
  - duplicar sucessos: um filme copiado varias vezes pode ocupar varios dos 7
    vizinhos de um filme de teste e decidir o voto sozinho;
  - SMOTENC: precisa das colunas categoricas originais, mas aqui o
    balanceamento vem depois do encoding e da reducao;
  - ADASYN e Tomek: nao foram vistos em sala e nao mudariam o argumento.
"""

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

from e2.base import SEMENTE

OPCOES = {
    "sem": lambda: "passthrough",
    "subamostragem": lambda: RandomUnderSampler(random_state=SEMENTE),
    # O SMOTE escolhe entre os 5 sucessos mais parecidos para criar cada filme novo.
    # E o valor padrao e cabe com folga nos cerca de 520 sucessos de cada treino.
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
