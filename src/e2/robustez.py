# -*- coding: utf-8 -*-
"""Robustez: o resultado da grade continua valendo se mudarmos as condicoes?

A grade compara 144 combinacoes num unico cenario. Aqui pegamos cerca de 13
delas e testamos em tres cenarios diferentes:

  - temporal: treina com filmes ate 2017 e testa com filmes de 2018 em
    diante. E assim que o modelo seria usado na pratica, prevendo o futuro.
    Tambem confere se o historico de sucesso das entidades vazou entre
    treino e teste, porque aqui nenhum filme do treino e mais novo que os
    filmes do teste;
  - limiar: troca a definicao de sucesso de P75 para P50 e P90, mantendo
    exatamente os mesmos folds. Se o ranking das combinacoes mudar muito,
    a conclusao depende do corte escolhido;
  - genero: separa os acertos de ficcao e de documentario. Como quase
    nenhum documentario e sucesso, o modelo pode estar so aprendendo a
    reconhecer o genero.
"""

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.base import clone
from sklearn.metrics import get_scorer
from sklearn.model_selection import cross_val_predict

from e2.espaco import ETAPAS
from e2.metricas import PRINCIPAL, SCORING

# Mesmo corte da Entrega 1. Os anos de pandemia ficam todos no teste,
# que e o futuro que o modelo nao viu.
ULTIMO_ANO_TREINO = 2017
GENEROS = ["Ficção", "Documentário"]


def selecionar(resultados, n=5):
    """Escolhe as combinacoes que vao para a robustez.

    Entram o baseline, as 5 melhores e as 5 piores pela AUC, e a melhor de cada
    opcao de balanceamento. Uma combinacao que aparece em dois grupos entra uma vez.
    """
    ok = resultados[resultados["erro"].isna() | (resultados["erro"] == "")]
    ordem = ok.sort_values(f"{PRINCIPAL}_media", ascending=False)
    ids = list(ok.loc[ok["eh_baseline"] == 1, "id"])
    ids += list(ordem["id"].head(n)) + list(ordem["id"].tail(n))
    ids += list(ordem.groupby("balanceamento", sort=False)["id"].first())
    unicos = list(dict.fromkeys(int(i) for i in ids))
    return resultados.set_index("id").loc[unicos, ETAPAS].reset_index()


def _pontua(modelo, X, y):
    """Calcula as seis metricas de um modelo ja treinado."""
    return {m: get_scorer(s)(modelo, X, y) for m, s in SCORING.items()}


def temporal(pipeline, X, y, ano):
    """Treina no passado, testa no futuro e devolve as metricas do teste."""
    treino, teste = ano <= ULTIMO_ANO_TREINO, ano > ULTIMO_ANO_TREINO
    modelo = clone(pipeline).fit(X[treino], y[treino])
    linha = _pontua(modelo, X[teste], y[teste])
    linha.update(n_treino=int(treino.sum()), n_teste=int(teste.sum()),
                 prevalencia_teste=float(y[teste].mean()))
    return linha


def por_fold(pipeline, X, y, folds):
    """Avalia a combinacao em cada um dos 5 folds.

    Guarda tambem a proporcao de sucessos de cada fold. Os folds foram
    montados para ter a mesma proporcao no corte P75. Em P50 e P90 ela pode
    variar um pouco de um fold para outro, e e bom registrar isso.
    """
    linhas = []
    for f, (tr, te) in enumerate(folds):
        modelo = clone(pipeline).fit(X.iloc[tr], y.iloc[tr])
        linha = _pontua(modelo, X.iloc[te], y.iloc[te])
        linha.update(fold=f, prevalencia_teste=float(y.iloc[te].mean()))
        linhas.append(linha)
    return linhas


def por_genero(pipeline, X, y, folds):
    """Preve cada filme pelo modelo que nao o viu no treino e mede por genero."""
    proba = cross_val_predict(clone(pipeline), X, y, cv=folds,
                              method="predict_proba")[:, 1]
    pred = (proba >= 0.5).astype(int)
    linhas = []
    for g in GENEROS:
        m = (X["genero"] == g).to_numpy()
        linhas.append({"genero": g, "n": int(m.sum()),
                       "prevalencia": float(y[m].mean()),
                       **_metricas_de_predicao(y[m], pred[m], proba[m])})
    return linhas


def _metricas_de_predicao(y, pred, proba):
    from sklearn import metrics as sk
    # Se um genero nao tiver nenhum sucesso, nao da para calcular a AUC.
    # Nesse caso a celula fica vazia em vez de interromper a rodada.
    uma_classe = len(np.unique(y)) < 2
    return {
        "accuracy": sk.accuracy_score(y, pred),
        "f1": sk.f1_score(y, pred, zero_division=0),
        "precision": sk.precision_score(y, pred, zero_division=0),
        "recall": sk.recall_score(y, pred, zero_division=0),
        "roc_auc": np.nan if uma_classe else sk.roc_auc_score(y, proba),
        "average_precision": np.nan if uma_classe else sk.average_precision_score(y, proba),
        "taxa_prevista_positiva": float(pred.mean()),
    }


def correlacao_rankings(limiar_df):
    """Compara o ranking das combinacoes entre os cortes P50, P75 e P90.

    Usa a correlacao de Spearman. Perto de 1 quer dizer que a ordem quase nao
    muda com o corte. Perto de 0 quer dizer que muda bastante.
    """
    medias = limiar_df.groupby(["quantil", "id"])[PRINCIPAL].mean().unstack(0)
    cortes = list(medias.columns)
    linhas = []
    for i, a in enumerate(cortes):
        for b in cortes[i + 1:]:
            rho, p = spearmanr(medias[a], medias[b])
            linhas.append({"corte_a": a, "corte_b": b, "spearman": rho, "p": p})
    return pd.DataFrame(linhas)
