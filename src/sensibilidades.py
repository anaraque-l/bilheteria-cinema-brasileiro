# -*- coding: utf-8 -*-
"""Mede o PESO de cada decisao de modelagem, sem tomar nenhuma delas.

Executar: python src/sensibilidades.py

POR QUE ISTO EXISTE NUMA ENTREGA EXPLORATORIA
  O enunciado pede "hipoteses de pre-processamento decorrentes das evidencias".
  Uma hipotese sem numero e palpite. Este modulo transforma cada hipotese numa
  medida: quanto muda o AUC se eu incluir o atributo suspeito de vazamento?
  quanto o split aleatorio infla o resultado em relacao ao split temporal?

  Isto NAO e a modelagem da Entrega 2. A diferenca importa:
    - a Entrega 2 escolhe o melhor modelo e reporta o desempenho dele;
    - aqui rodamos UM protocolo fixo e simples, e o que se compara e sempre a
      DIFERENCA entre duas versoes da base. O modelo e so o instrumento de
      medida, como um termometro. Nenhum resultado daqui vira "o desempenho do
      nosso modelo" no relatorio.

  A base entregue em data/processed/filmes.csv continua sem imputacao, sem
  remocao de outlier e sem codificacao. Toda transformacao testada aqui
  acontece DENTRO dos folds, num Pipeline, e morre no fim da funcao.
"""

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

warnings.filterwarnings("ignore")

RAIZ = Path(__file__).resolve().parent.parent
SEMENTE = 42

# O conjunto "honesto": tudo que um produtor sabe ANTES de estrear o filme.
# Nao ha publico, nao ha renda, nao ha numero de salas.
NUM_HONESTAS = ["ano", "filmes_diretor_antes", "filmes_distribuidora_antes",
                "filmes_produtora_antes", "filmes_no_ano", "coproducao", "n_ufs",
                # Fomento e APROVADO antes de a obra existir: anterior a estreia.
                "recebeu_fsa", "recebeu_incentivo",
                "contratos_fsa", "projetos_incentivo"]
CAT_HONESTAS = ["genero", "uf_maj", "distribuidora",
                # As duas ordinais derivam de contagens so do passado.
                "experiencia_da_direcao", "porte_da_distribuidora",
                "origem_do_fomento"]


def _dados():
    import build_dataset
    return build_dataset.carregar()


def _pipeline(num, cat, modelo, log_num=False, max_cat=30):
    """Pipeline com TODO o pre-processamento dentro do fold.

    Se o imputer ou o scaler fossem ajustados fora, a estatistica usada para
    preencher o fold de teste teria sido calculada com o proprio fold de teste
    dentro. Isso e vazamento de pre-processamento, e e o erro mais comum da
    disciplina.
    """
    passos_num = [("imp", SimpleImputer(strategy="median"))]
    if log_num:
        passos_num.append(("log", _Log1p()))
    passos_num.append(("esc", StandardScaler()))

    prep = ColumnTransformer([
        ("num", Pipeline(passos_num), num),
        ("cat", Pipeline([
            ("imp", SimpleImputer(strategy="constant", fill_value="AUSENTE")),
            # min_frequency agrupa categoria rara em "infrequent". Sem isso, as
            # 467 distribuidoras viram 467 colunas, quase todas com 1 filme.
            ("ohe", OneHotEncoder(handle_unknown="infrequent_if_exist",
                                  min_frequency=max_cat, sparse_output=False)),
        ]), cat),
    ], remainder="drop")

    return Pipeline([("prep", prep), ("modelo", modelo)])


class _Log1p:
    """log1p em matriz densa. Sklearn tem FunctionTransformer, mas uma classe
    nomeada aparece melhor no repr do pipeline e no relatorio."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.log1p(np.clip(np.asarray(X, dtype=float), 0, None))

    def get_params(self, deep=True):
        return {}

    def set_params(self, **kw):
        return self


def _auc(d, num, cat, alvo, modelo, log_num=False):
    """AUC media em 5-fold estratificado. Devolve (media, desvio)."""
    base = d[d[alvo].notna()].copy()
    y = base[alvo].astype(int)
    X = base[num + cat]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMENTE)
    s = cross_val_score(_pipeline(num, cat, modelo, log_num), X, y,
                        cv=cv, scoring="roc_auc")
    return s.mean(), s.std()


def _rf():
    return RandomForestClassifier(n_estimators=300, random_state=SEMENTE, n_jobs=-1)


def _lr():
    return LogisticRegression(max_iter=2000, random_state=SEMENTE)


# ---------------------------------------------------------------------------
# S1 - Vazamento: quanto vale cada atributo posterior ao lancamento
# ---------------------------------------------------------------------------

def s1_vazamento(d):
    print("\n" + "=" * 74)
    print("S1  VAZAMENTO - o que cada atributo posterior ao lancamento entrega")
    print("=" * 74)
    print("AUC de floresta aleatoria, 5-fold, alvo=sucesso_global.\n")

    cenarios = [
        ("honesto (so o que se sabe antes de estrear)", NUM_HONESTAS),
        ("+ max_salas", NUM_HONESTAS + ["max_salas"]),
        ("+ renda_deflacionada_2024", NUM_HONESTAS + ["renda_deflacionada_2024"]),
        ("+ max_salas + renda", NUM_HONESTAS + ["max_salas", "renda_deflacionada_2024"]),
    ]
    linhas = []
    base_auc = None
    for nome, num in cenarios:
        m, s = _auc(d, num, CAT_HONESTAS, "sucesso_global", _rf())
        if base_auc is None:
            base_auc = m
        linhas.append((nome, m, s, m - base_auc))
        print("  %-44s AUC %.3f (+/-%.3f)   delta %+0.3f" % (nome, m, s, m - base_auc))
    return pd.DataFrame(linhas, columns=["cenario", "auc", "desvio", "delta_vs_honesto"])


# ---------------------------------------------------------------------------
# S2 - Definicao do alvo
# ---------------------------------------------------------------------------

def s2_alvo(d):
    print("\n" + "=" * 74)
    print("S2  DEFINICAO DO ALVO - mediana global x mediana do ano")
    print("=" * 74)

    for alvo in ["sucesso_global", "sucesso_no_ano"]:
        pos = d[alvo].mean()
        por_decada = d.groupby("decada")[alvo].mean()
        m, s = _auc(d, NUM_HONESTAS, CAT_HONESTAS, alvo, _rf())
        print("\n  %s" % alvo)
        print("    taxa de positivos global: %.3f" % pos)
        print("    taxa por decada: %s" % por_decada.round(3).to_dict())
        print("    AUC (conjunto honesto): %.3f (+/-%.3f)" % (m, s))
    print("\n  Leitura: a mediana global embute o ANO no alvo - filme antigo cai")
    print("  quase sempre no lado 'sucesso'. A mediana do ano remove esse atalho.")


# ---------------------------------------------------------------------------
# S3 - Split aleatorio x split temporal
# ---------------------------------------------------------------------------

def s3_split(d):
    print("\n" + "=" * 74)
    print("S3  PARTICAO - aleatoria x temporal (treina no passado, testa no futuro)")
    print("=" * 74)

    from sklearn.metrics import roc_auc_score

    for alvo in ["sucesso_global", "sucesso_no_ano"]:
        base = d[d[alvo].notna()].copy()
        y = base[alvo].astype(int)
        X = base[NUM_HONESTAS + CAT_HONESTAS]

        aleat, _ = _auc(d, NUM_HONESTAS, CAT_HONESTAS, alvo, _rf())

        corte = 2018
        tr, te = base["ano"] < corte, base["ano"] >= corte
        p = _pipeline(NUM_HONESTAS, CAT_HONESTAS, _rf())
        p.fit(X[tr], y[tr])
        temporal = roc_auc_score(y[te], p.predict_proba(X[te])[:, 1])

        print("\n  %s" % alvo)
        print("    AUC 5-fold aleatorio : %.3f" % aleat)
        print("    AUC treino<%d / teste>=%d : %.3f  (n_teste=%d)"
              % (corte, corte, temporal, te.sum()))
        print("    otimismo do split aleatorio: %+.3f" % (aleat - temporal))


# ---------------------------------------------------------------------------
# S4 - Cardinalidade da distribuidora
# ---------------------------------------------------------------------------

def s4_cardinalidade(d):
    print("\n" + "=" * 74)
    print("S4  CARDINALIDADE - como tratar 467 distribuidoras")
    print("=" * 74)
    print("  min_frequency = quantos filmes uma distribuidora precisa ter para")
    print("  ganhar coluna propria. Abaixo disso, cai num balde 'infrequente'.\n")

    for corte in [1, 5, 15, 30, 60]:
        base = d[d["sucesso_global"].notna()]
        y = base["sucesso_global"].astype(int)
        X = base[NUM_HONESTAS + CAT_HONESTAS]
        cv = StratifiedKFold(5, shuffle=True, random_state=SEMENTE)
        p = _pipeline(NUM_HONESTAS, CAT_HONESTAS, _rf(), max_cat=corte)
        s = cross_val_score(p, X, y, cv=cv, scoring="roc_auc")
        p.fit(X, y)
        n_col = p.named_steps["prep"].transform(X).shape[1]
        print("    min_frequency=%-3d  colunas=%-4d  AUC %.3f (+/-%.3f)"
              % (corte, n_col, s.mean(), s.std()))


# ---------------------------------------------------------------------------
# S5 - Transformacao log em atributo assimetrico
# ---------------------------------------------------------------------------

def s5_log(d):
    print("\n" + "=" * 74)
    print("S5  ASSIMETRIA - o log ajuda quem? (modelo linear x arvore)")
    print("=" * 74)
    print("  Atributos com cauda longa entram aqui: max_salas e os historicos.\n")

    num = NUM_HONESTAS + ["max_salas"]
    for nome, modelo in [("regressao logistica", _lr()), ("floresta aleatoria", _rf())]:
        cru, _ = _auc(d, num, CAT_HONESTAS, "sucesso_global", modelo, log_num=False)
        log, _ = _auc(d, num, CAT_HONESTAS, "sucesso_global", modelo, log_num=True)
        print("    %-22s cru %.3f  ->  log1p %.3f   delta %+0.3f"
              % (nome, cru, log, log - cru))
    print("\n  Leitura: o log muda o modelo linear e quase nao muda a arvore.")
    print("  Arvore so olha a ORDEM dos valores, e log1p e monotonica.")


# ---------------------------------------------------------------------------
# S6 - Atributo de variancia quase nula
# ---------------------------------------------------------------------------

def s6_variancia_nula(d):
    print("\n" + "=" * 74)
    print("S6  VARIANCIA QUASE NULA - vale a pena remover n_ufs?")
    print("=" * 74)
    moda = d["n_ufs"].value_counts(normalize=True).iloc[0]
    print("    n_ufs: a moda concentra %.1f%% dos registros\n" % (moda * 100))

    com, sc = _auc(d, NUM_HONESTAS, CAT_HONESTAS, "sucesso_global", _rf())
    sem_lista = [c for c in NUM_HONESTAS if c != "n_ufs"]
    sem, ss = _auc(d, sem_lista, CAT_HONESTAS, "sucesso_global", _rf())
    print("    com n_ufs : AUC %.3f (+/-%.3f)" % (com, sc))
    print("    sem n_ufs : AUC %.3f (+/-%.3f)" % (sem, ss))
    print("    delta     : %+0.3f  (desvio entre folds e %.3f)" % (sem - com, sc))


def main():
    d = _dados()
    print("Analise de sensibilidade - %d filmes" % len(d))
    print("Protocolo fixo: 5-fold estratificado, semente %d, tudo em Pipeline." % SEMENTE)
    tabela = s1_vazamento(d)
    s2_alvo(d)
    s3_split(d)
    s4_cardinalidade(d)
    s5_log(d)
    s6_variancia_nula(d)

    destino = RAIZ / "reports" / "sensibilidades_s1.csv"
    destino.parent.mkdir(parents=True, exist_ok=True)
    tabela.to_csv(destino, index=False, encoding="utf-8")
    print("\nTabela S1 gravada em %s" % destino.relative_to(RAIZ))


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
