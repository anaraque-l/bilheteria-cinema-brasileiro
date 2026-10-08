# -*- coding: utf-8 -*-
"""Roda todas as combinacoes da Entrega 2 com o kNN e grava os resultados.

Executar:
  python src/executar_e2.py              todas, retomando de onde parou
  python src/executar_e2.py --rapido     o baseline e uma variacao por opcao
  python src/executar_e2.py --so 17      uma combinacao
  python src/executar_e2.py --refazer    apaga os resultados e recomeca

Saidas em reports/e2/:
  resultados.csv           uma linha por combinacao, media e desvio por metrica
  resultados_por_fold.csv  uma linha por combinacao e fold
  folds.csv                o fold de cada filme
  ambiente.json            versoes, semente e data da rodada
"""

import argparse
import json
import platform
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import get_scorer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e2 import base, espaco  # noqa: E402
from e2.metricas import SCORING  # noqa: E402

warnings.filterwarnings("ignore")


def dimensao_no_knn(pipe, X):
    """Quantas colunas chegam ao kNN. O sampler nao transforma, so reamostra."""
    for _, passo in pipe.steps[:-1]:
        if passo != "passthrough" and not hasattr(passo, "fit_resample"):
            X = passo.transform(X)
    return X.shape[1]


def avaliar(config, X, y, pares):
    """Ajusta e mede a combinacao em cada fold. Devolve as linhas por fold."""
    linhas = []
    for fold, (treino, teste) in enumerate(pares):
        pipe = espaco.construir_pipeline(config)
        Xtr, ytr = X.iloc[treino], y.iloc[treino]
        Xte, yte = X.iloc[teste], y.iloc[teste]

        inicio = time.perf_counter()
        pipe.fit(Xtr, ytr)
        ajuste = time.perf_counter() - inicio

        inicio = time.perf_counter()
        linha = {nome: get_scorer(s)(pipe, Xte, yte) for nome, s in SCORING.items()}
        predicao = time.perf_counter() - inicio

        linha["n_atributos"] = dimensao_no_knn(pipe, Xte)
        linha.update(id=config["id"], fold=fold,
                     tempo_ajuste_s=ajuste, tempo_predicao_s=predicao)
        linhas.append(linha)
    return linhas


def resumir(config, por_fold, erro=""):
    linha = {"id": config["id"], "codigo": espaco.codigo(config)}
    linha.update({etapa: config[etapa] for etapa in espaco.ETAPAS})
    linha["eh_baseline"] = int(espaco.eh_baseline(config))
    f = pd.DataFrame(por_fold)
    for nome in SCORING:
        valores = f[nome] if len(f) else pd.Series(dtype=float)
        linha[nome + "_media"] = valores.mean()
        # desvio amostral: com cinco folds e o mais conservador, e gera mais empates
        linha[nome + "_dp"] = valores.std(ddof=1)
    if len(f):
        linha["n_atributos"] = f["n_atributos"].mean()
        linha["tempo_total_s"] = (f["tempo_ajuste_s"] + f["tempo_predicao_s"]).sum()
        linha["tempo_ajuste_medio_s"] = f["tempo_ajuste_s"].mean()
    else:
        linha.update(n_atributos=np.nan, tempo_total_s=np.nan,
                     tempo_ajuste_medio_s=np.nan)
    linha["erro"] = erro
    return linha


def selecao_rapida(todas):
    """O baseline e, para cada opcao das cinco etapas, a variacao dele so nela."""
    escolhidas = []
    for config in todas:
        diferentes = [e for e in espaco.ETAPAS if config[e] != espaco.BASELINE[e]]
        if len(diferentes) <= 1:
            escolhidas.append(config)
    return escolhidas


def _anexar(caminho, linhas):
    pd.DataFrame(linhas).to_csv(caminho, mode="a", index=False,
                                header=not caminho.exists(), encoding="utf-8")


def gravar_ambiente(destino):
    import imblearn
    import sklearn
    info = {
        "python": platform.python_version(),
        "scikit-learn": sklearn.__version__,
        "imbalanced-learn": imblearn.__version__,
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "sistema": platform.platform(terse=True),
        "semente": base.SEMENTE,
        "validacao": "StratifiedKFold de 5 folds, embaralhado, semente %d" % base.SEMENTE,
        "ordem_das_etapas": espaco.ETAPAS + ["knn"],
        "k_vizinhos": espaco.K_VIZINHOS,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    (destino / "ambiente.json").write_text(
        json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--rapido", action="store_true")
    p.add_argument("--so", type=int)
    p.add_argument("--refazer", action="store_true")
    args = p.parse_args()

    # a rodada rapida e de teste e nao pode se misturar com a oficial
    destino = base.SAIDA / "rapido" if args.rapido else base.SAIDA
    destino.mkdir(parents=True, exist_ok=True)
    resumo_csv = destino / "resultados.csv"
    fold_csv = destino / "resultados_por_fold.csv"
    if args.refazer:
        resumo_csv.unlink(missing_ok=True)
        fold_csv.unlink(missing_ok=True)

    X, y, _ = base.carregar_xy()
    # a rodada rapida e de teste, entao nao pode reescrever o folds.csv oficial
    pares = base.folds(gravar=not args.rapido)
    todas = espaco.combinacoes()
    if args.rapido:
        todas = selecao_rapida(todas)
    if args.so:
        todas = [c for c in todas if c["id"] == args.so]

    # retomada: uma queda na combinacao 130 nao pode custar as 129 anteriores; quem
    # falhou volta para a fila, porque a falha pode ter sido da maquina e nao da combinacao
    feitas = set()
    if resumo_csv.exists():
        anteriores = pd.read_csv(resumo_csv)
        sem_erro = anteriores["erro"].isna()
        feitas = set(anteriores.loc[sem_erro, "id"])
        anteriores[sem_erro].to_csv(resumo_csv, index=False, encoding="utf-8")
    pendentes = [c for c in todas if c["id"] not in feitas]
    print("%d filmes, %d combinacoes, %d ja feitas, %d a rodar"
          % (len(y), len(todas), len(todas) - len(pendentes), len(pendentes)))

    for config in pendentes:
        inicio = time.perf_counter()
        try:
            por_fold, erro = avaliar(config, X, y, pares), ""
        except Exception as e:
            # combinacao que falha e resultado: vai para a tabela com a mensagem
            por_fold, erro = [], "%s: %s" % (type(e).__name__, str(e).splitlines()[0])
        linha = resumir(config, por_fold, erro)
        _anexar(resumo_csv, [linha])
        if por_fold:
            _anexar(fold_csv, por_fold)
        print("  %3d  %-55s AUC %.3f +- %.3f  F1 %.3f  %5.1fs  %s"
              % (config["id"], linha["codigo"], linha["roc_auc_media"],
                 linha["roc_auc_dp"], linha["f1_media"],
                 time.perf_counter() - inicio, erro))

    gravar_ambiente(destino)
    print("gravado em %s" % destino.relative_to(base.RAIZ).as_posix())


if __name__ == "__main__":
    main()
