# -*- coding: utf-8 -*-
"""Robustez da Entrega 2: o ranking da grade se aguenta de pe?

Tres checagens sobre um punhado de combinacoes escolhidas da grade:
  temporal  treina no passado e testa no futuro, como a Entrega 1 recomendou;
            e tambem a checagem honesta do vazamento cruzado dos hist_*,
            porque nenhum filme do treino e posterior a um filme do teste.
  limiar    refaz o 5-fold com o alvo em P50 e P90 sobre os mesmos folds,
            entao a unica coisa que muda e o corte.
  genero    predicao fora do fold separada por Ficcao e Documentario, para
            saber se o modelo preve sucesso ou preve genero.

Nada aqui depende de como o pipeline e montado: tudo recebe uma funcao que
devolve o pipeline de uma configuracao.
"""

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.base import clone
from sklearn.metrics import get_scorer
from sklearn.model_selection import cross_val_predict

from e2.metricas import PRINCIPAL, SCORING

ETAPAS = ["ausentes", "encoding", "normalizacao", "reducao", "balanceamento"]

# Ultimo ano do treino na temporal: deixa 2018 em diante como teste, o mesmo
# corte da Entrega 1, que ja inclui os anos de pandemia no futuro.
ULTIMO_ANO_TREINO = 2017
GENEROS = ["Ficção", "Documentário"]


def selecionar(resultados, n=5):
    """Baseline, n melhores, n piores e a melhor de cada balanceamento, sem repetir."""
    ok = resultados[resultados["erro"].isna() | (resultados["erro"] == "")]
    ordem = ok.sort_values(f"{PRINCIPAL}_media", ascending=False)
    ids = list(ok.loc[ok["eh_baseline"] == 1, "id"])
    ids += list(ordem["id"].head(n)) + list(ordem["id"].tail(n))
    ids += list(ordem.groupby("balanceamento", sort=False)["id"].first())
    unicos = list(dict.fromkeys(int(i) for i in ids))
    return resultados.set_index("id").loc[unicos, ETAPAS].reset_index()


def _pontua(modelo, X, y):
    return {m: get_scorer(s)(modelo, X, y) for m, s in SCORING.items()}


def temporal(pipeline, X, y, ano):
    treino, teste = ano <= ULTIMO_ANO_TREINO, ano > ULTIMO_ANO_TREINO
    modelo = clone(pipeline).fit(X[treino], y[treino])
    linha = _pontua(modelo, X[teste], y[teste])
    linha.update(n_treino=int(treino.sum()), n_teste=int(teste.sum()),
                 prevalencia_teste=float(y[teste].mean()))
    return linha


def por_fold(pipeline, X, y, folds):
    """Uma linha por fold, com a prevalencia de cada um, porque os folds foram
    estratificados no P75 e nos outros cortes a proporcao pode oscilar."""
    linhas = []
    for f, (tr, te) in enumerate(folds):
        modelo = clone(pipeline).fit(X.iloc[tr], y.iloc[tr])
        linha = _pontua(modelo, X.iloc[te], y.iloc[te])
        linha.update(fold=f, prevalencia_teste=float(y.iloc[te].mean()))
        linhas.append(linha)
    return linhas


def por_genero(pipeline, X, y, folds):
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
    # Um genero sem nenhum positivo nao tem AUC; vira NaN em vez de erro.
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
    """Spearman entre os rankings por AUC media em cada par de cortes."""
    medias = limiar_df.groupby(["quantil", "id"])[PRINCIPAL].mean().unstack(0)
    cortes = list(medias.columns)
    linhas = []
    for i, a in enumerate(cortes):
        for b in cortes[i + 1:]:
            rho, p = spearmanr(medias[a], medias[b])
            linhas.append({"corte_a": a, "corte_b": b, "spearman": rho, "p": p})
    return pd.DataFrame(linhas)
