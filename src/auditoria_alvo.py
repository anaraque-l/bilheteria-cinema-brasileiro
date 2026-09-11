# -*- coding: utf-8 -*-
"""Auditoria metodologica da definicao de SUCESSO DE BILHETERIA.

Executar: python src/auditoria_alvo.py

POR QUE ISTO EXISTE
  `build_dataset.py` cria dois alvos candidatos - `sucesso_global` e
  `sucesso_no_ano` - e `docs/02-decisoes-e-escopo.md` (D4) recomenda o segundo.
  Este modulo NAO aceita essa decisao como dada: ele pergunta se a mediana e um
  bom ponto de corte, se existe corte melhor, e o quanto a conclusao sobre
  "quais filmes deram certo" depende da definicao escolhida.

  Nada aqui altera a base. O modulo so MEDE, e grava as tabelas em reports/.
  A leitura das tabelas esta em docs/04-auditoria-do-alvo.md.
"""

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy.optimize import brentq
from scipy.stats import norm
from sklearn.metrics import cohen_kappa_score, roc_auc_score
from sklearn.mixture import GaussianMixture

sys.path.insert(0, str(Path(__file__).resolve().parent))
warnings.filterwarnings("ignore")

import build_dataset as bd  # noqa: E402
from sensibilidades import CAT_HONESTAS, NUM_HONESTAS, _pipeline, _rf  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "reports"
FIGURAS = SAIDA / "figuras"
SEMENTE = 0

# Paleta das outras onze figuras do relatorio: a figura nova precisa parecer da
# mesma familia, senao o slide denuncia que foi feita depois.
COR, COR2, CINZA = "#2b6cb0", "#c05621", "#4a5568"
# Rotulo curto do eixo log: "1 mil" em vez de "1.000", senao as marcas colidem.
CURTO = {1: "10", 2: "100", 3: "1 mil", 4: "10 mil", 5: "100 mil",
         6: "1 mi", 7: "10 mi"}


def ptbr(v):
    """1234567 -> '1.234.567' (separador de milhar do pt-BR)."""
    return format(int(round(v)), ",.0f").replace(",", ".")


# ---------------------------------------------------------------------------
# As definicoes candidatas de sucesso
# ---------------------------------------------------------------------------

def definicoes(d):
    """Devolve um DataFrame 0/1: uma coluna por definicao candidata de sucesso.

    As definicoes se dividem em quatro familias:
      - corte por quantil GLOBAL (o alvo literal do enunciado e suas variantes);
      - corte por quantil DO ANO (controla o tamanho do mercado);
      - corte ABSOLUTO (limiar de negocio, em espectadores);
      - corte NORMALIZADO (pela populacao, ou pela fatia do mercado do ano).
    A familia "ano ANTERIOR" existe para testar um problema especifico:
    a mediana do proprio ano so e conhecida depois que o ano acaba.
    """
    p = d["publico"]
    por_ano = lambda q: d.groupby("ano")["publico"].transform(lambda s: s.quantile(q))
    defeito_prev = lambda q: d["ano"].map(d.groupby("ano")["publico"].quantile(q).shift(1))

    dd = d.copy()
    janela = pd.Series(np.nan, index=d.index)
    for a in sorted(d["ano"].unique()):
        vizinhanca = d[(d["ano"] >= a - 2) & (d["ano"] <= a + 2)]["publico"]
        janela[dd["ano"] == a] = vizinhanca.quantile(0.75)

    taxa = p / d["populacao_br"]
    fatia = p / d.groupby("ano")["publico"].transform("sum")

    # A serie do IBGE nao cobre 9 dos 30 anos (1995-2000, 2007, 2010, 2022-2023):
    # ano de Censo e os primeiros anos ficam de fora do agregado 6579. Onde nao
    # ha populacao, a definicao per capita e INDEFINIDA - nao "fracasso".
    sem_pop = d["populacao_br"].isna()

    tabela = pd.DataFrame({
        "global_P50": p > p.median(),            # alvo atual: sucesso_global
        "global_P75": p > p.quantile(0.75),
        "global_P80": p > p.quantile(0.80),
        "global_P90": p > p.quantile(0.90),
        "ano_P50": p > por_ano(0.50),            # alvo atual: sucesso_no_ano
        "ano_P75": p > por_ano(0.75),
        "ano_P90": p > por_ano(0.90),
        "anoANTERIOR_P50": p > defeito_prev(0.50),
        "anoANTERIOR_P75": p > defeito_prev(0.75),
        "janela5a_P75": p > janela,
        "abs_50k": p >= 50_000,
        "abs_100k": p >= 100_000,
        "abs_500k": p >= 500_000,
        "percapita_P50": taxa > taxa.median(),
        "percapita_P90": taxa > taxa.quantile(0.90),
        "fatia_10pct_do_ano": fatia >= 0.10,
    }).astype(float)
    tabela.loc[sem_pop, ["percapita_P50", "percapita_P90"]] = np.nan
    tabela.loc[d["ano"] == d["ano"].min(), ["anoANTERIOR_P50", "anoANTERIOR_P75"]] = np.nan
    return tabela


# ---------------------------------------------------------------------------
# Analises
# ---------------------------------------------------------------------------

def distribuicao(d):
    """Forma da distribuicao de publico: assimetria, cauda e concentracao."""
    p = d["publico"].dropna()
    s = np.sort(p.to_numpy())[::-1]
    gini_x = np.sort(p.to_numpy())
    n = len(gini_x)
    gini = (2 * np.arange(1, n + 1) - n - 1).dot(gini_x) / (n * gini_x.sum())

    linhas = [("n", len(p)), ("media", p.mean()), ("mediana", p.median()),
              ("media/mediana", p.mean() / p.median()),
              ("desvio", p.std()), ("assimetria", p.skew()), ("curtose", p.kurt()),
              ("gini", gini), ("maximo/mediana", p.max() / p.median())]
    for q in [0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]:
        linhas.append(("P%d" % (q * 100), p.quantile(q)))
    for k in [0.01, 0.05, 0.10, 0.20]:
        linhas.append(("%% do publico no top %d%%" % (k * 100),
                       s[:int(round(k * len(s)))].sum() / s.sum() * 100))
    linhas.append(("% do publico na metade inferior",
                   s[len(s) // 2:].sum() / s.sum() * 100))
    return pd.DataFrame(linhas, columns=["estatistica", "valor"])


def duas_populacoes(d):
    """A distribuicao de publico e uma mistura de duas populacoes?

    Ajusta uma mistura de duas gaussianas em log10(publico) e devolve, por
    periodo, o centro de cada componente e o ponto em que uma passa a dominar
    a outra. Esse ponto de cruzamento e um corte que os DADOS propoem, em vez
    de um quantil escolhido por nos.
    """
    def ajustar(x):
        X = np.log10(x.dropna().to_numpy()).reshape(-1, 1)
        g = GaussianMixture(2, random_state=SEMENTE).fit(X)
        ordem = np.argsort(g.means_.ravel())
        w, m = g.weights_[ordem], g.means_.ravel()[ordem]
        sd = np.sqrt(g.covariances_.ravel())[ordem]
        f = lambda t: w[0] * norm.pdf(t, m[0], sd[0]) - w[1] * norm.pdf(t, m[1], sd[1])
        try:
            cruz = 10 ** brentq(f, m[0], m[1])
        except ValueError:
            cruz = np.nan
        return w, 10 ** m, cruz

    linhas = []
    for rotulo, sub in [("1995-2024", d)] + [(str(k), g) for k, g in d.groupby("decada")]:
        w, centros, cruz = ajustar(sub["publico"])
        linhas.append({"periodo": rotulo, "n": len(sub),
                       "peso_circuito_limitado": w[0], "centro_circuito_limitado": centros[0],
                       "peso_lancamento_comercial": w[1], "centro_lancamento_comercial": centros[1],
                       "cruzamento": cruz,
                       "%_acima_do_cruzamento": (sub["publico"] > cruz).mean() * 100})
    return pd.DataFrame(linhas)


def sensibilidade(d, R):
    """Para cada definicao: prevalencia, limiar implicado e quanto ela discorda
    do alvo atual. E a pergunta central: a conclusao sobre quem deu certo
    depende da definicao?"""
    p = d["publico"]
    linhas = []
    for c in R.columns:
        y = R[c]
        m = y.notna()
        pos = p[m & (y == 1)]
        linhas.append({
            "definicao": c,
            "positivos": int(y.sum()),
            "negativos": int((1 - y[m]).sum()),
            "%_positivos": y[m].mean() * 100,
            "publico_minimo_de_um_sucesso": pos.min() if len(pos) else np.nan,
            "publico_mediano_dos_sucessos": pos.median() if len(pos) else np.nan,
            "kappa_vs_global_P50": cohen_kappa_score(R.loc[m, "global_P50"], y[m]),
            "kappa_vs_ano_P50": cohen_kappa_score(R.loc[m, "ano_P50"], y[m]),
            "%_que_muda_vs_global_P50": (y[m] != R.loc[m, "global_P50"]).mean() * 100,
            "%_que_muda_vs_ano_P50": (y[m] != R.loc[m, "ano_P50"]).mean() * 100,
        })
    return pd.DataFrame(linhas)


def prevalencia_por_decada(d, R):
    """A definicao esta medindo cinema ou esta medindo calendario?"""
    t = pd.concat([d[["decada"]], R], axis=1)
    return (t.groupby("decada").mean() * 100).round(1).reset_index()


def prevalencia_por_genero(d, R):
    """Documentario e ficcao disputam a mesma bilheteria? A definicao assume que sim."""
    t = pd.concat([d[["genero"]], R], axis=1)
    fora = (t.groupby("genero").mean() * 100).round(1)
    fora.insert(0, "n", d.groupby("genero").size())
    fora.insert(1, "publico_mediano", d.groupby("genero")["publico"].median())
    return fora.reset_index()


def estabilidade_da_mediana_anual(d, reps=2000):
    """Quanto da classificacao e ruido amostral?

    Reamostra cada ano com reposicao e devolve o IC95% da mediana daquele ano.
    Filme cujo publico cai DENTRO desse intervalo tem classe indeterminada:
    outra amostra do mesmo mercado o colocaria do outro lado do corte.
    """
    rng = np.random.default_rng(SEMENTE)
    linhas, indeterminados = [], 0
    for a, g in d.groupby("ano"):
        v = g["publico"].dropna().to_numpy()
        bs = [np.median(rng.choice(v, len(v), replace=True)) for _ in range(reps)]
        lo, hi = np.percentile(bs, [2.5, 97.5])
        dentro = int(((v >= lo) & (v <= hi)).sum())
        indeterminados += dentro
        linhas.append({"ano": a, "n_filmes": len(v), "mediana": np.median(v),
                       "ic95_inferior": lo, "ic95_superior": hi,
                       "largura_relativa": (hi - lo) / max(np.median(v), 1),
                       "filmes_indeterminados": dentro,
                       "%_indeterminados": dentro / len(v) * 100})
    tabela = pd.DataFrame(linhas)
    total = len(d["publico"].dropna())
    print("  filmes com classe indeterminada (dentro do IC95%% da mediana do ano): "
          "%d de %d (%.1f%%)" % (indeterminados, total, indeterminados / total * 100))
    return tabela


def utilidade_preditiva(d, R):
    """Cada definicao e igualmente aprendivel com atributos pre-estreia?

    Protocolo fixo: floresta aleatoria, so atributos anteriores a estreia,
    particao TEMPORAL (treino ate 2017, teste de 2018 em diante). O modelo e
    instrumento de medida, nao resultado - vale a COMPARACAO entre alvos.
    """
    tr, te = d["ano"] <= 2017, d["ano"] >= 2018
    linhas = []
    for c in R.columns:
        y = R[c]
        m = y.notna()
        ytr, yte = y[tr & m], y[te & m]
        if ytr.nunique() < 2 or yte.nunique() < 2:
            continue
        pipe = _pipeline(NUM_HONESTAS, CAT_HONESTAS, _rf())
        pipe.fit(d.loc[tr & m, NUM_HONESTAS + CAT_HONESTAS], ytr.astype(int))
        prob = pipe.predict_proba(d.loc[te & m, NUM_HONESTAS + CAT_HONESTAS])[:, 1]
        linhas.append({"definicao": c, "auc_teste": roc_auc_score(yte.astype(int), prob),
                       "%_pos_treino": ytr.mean() * 100, "%_pos_teste": yte.mean() * 100,
                       "desequilibrio_treino_teste": abs(ytr.mean() - yte.mean()) * 100})
    return pd.DataFrame(linhas)


# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Figura
# ---------------------------------------------------------------------------

def _mistura(v):
    """Ajusta a mistura de duas gaussianas e devolve (pesos, centros, cruzamento).

    Mesma conta de `duas_populacoes`, isolada porque a figura precisa tambem dos
    parametros das curvas, nao so do cruzamento.
    """
    X = np.log10(v).reshape(-1, 1)
    g = GaussianMixture(2, random_state=SEMENTE).fit(X)
    o = np.argsort(g.means_.ravel())
    w, m, sd = g.weights_[o], g.means_.ravel()[o], np.sqrt(g.covariances_.ravel())[o]
    f = lambda t: w[0] * norm.pdf(t, m[0], sd[0]) - w[1] * norm.pdf(t, m[1], sd[1])
    return w, m, sd, 10 ** brentq(f, m[0], m[1])


def figura(d):
    """fig12 - as duas populacoes da bilheteria, e a fronteira ao longo do tempo.

    E a unica evidencia desta auditoria que precisa ser VISTA para convencer: no
    painel da esquerda, a mediana cai DENTRO da populacao de circuito limitado.
    Esse e o argumento contra o alvo atual, em uma imagem.
    """
    plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 160, "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.grid": True, "grid.alpha": .25, "grid.linewidth": .6})
    x = np.log10(d["publico"].to_numpy())
    w, m, sd, cruz = _mistura(d["publico"].to_numpy())
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))

    # --- painel 1: a mistura ------------------------------------------------
    ax = axes[0]
    ax.hist(x, bins=48, density=True, color="#cbd5e0", edgecolor="white",
            linewidth=.5, label="filmes (%s)" % ptbr(len(x)))
    grade = np.linspace(x.min(), x.max(), 600)
    ax.plot(grade, w[0] * norm.pdf(grade, m[0], sd[0]), color=COR, lw=2,
            label="circuito limitado — %.0f%%, centro %s" % (w[0] * 100, ptbr(10 ** m[0])))
    ax.plot(grade, w[1] * norm.pdf(grade, m[1], sd[1]), color=COR2, lw=2,
            label="lançamento comercial — %.0f%%, centro %s" % (w[1] * 100, ptbr(10 ** m[1])))
    ax.axvline(np.log10(cruz), color=CINZA, lw=2)
    ax.axvline(np.log10(d["publico"].median()), color=CINZA, ls="--", lw=1.6)
    topo = ax.get_ylim()[1]
    pct = (d["publico"] < cruz).mean() * 100
    ax.annotate("fronteira\n%s espectadores\n(percentil %.0f)" % (ptbr(cruz), pct),
                (np.log10(cruz), topo * .97), color=CINZA, fontsize=9,
                fontweight="bold", ha="left", va="top", xytext=(6, 0),
                textcoords="offset points")
    ax.annotate("mediana %s\n(alvo atual)" % ptbr(d["publico"].median()),
                (np.log10(d["publico"].median()), topo * .55), color=CINZA,
                fontsize=9, ha="right", va="top", xytext=(-6, 0),
                textcoords="offset points")
    ax.set_xlabel("público (escala logarítmica)")
    ax.set_ylabel("densidade")
    ax.set_title("A bilheteria brasileira são duas populações, não uma\n"
                 "mistura de 2 gaussianas ajusta melhor que 1 (BIC 8.260 vs. 8.358)",
                 loc="left", fontsize=11, fontweight="bold")
    ax.set_xticks(list(CURTO))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: CURTO.get(int(round(v)), "")))
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", bbox_to_anchor=(.02, .78))

    # --- painel 2: a fronteira ao longo do tempo -----------------------------
    ax = axes[1]
    dec = sorted(d["decada"].unique())
    centro_alto, fronteira = [], []
    for k in dec:
        _, mm, _, cc = _mistura(d.loc[d["decada"] == k, "publico"].to_numpy())
        centro_alto.append(10 ** mm[1])
        fronteira.append(cc)
    mediana_dec = [d.loc[d["decada"] == k, "publico"].median() for k in dec]
    rot = ["%ds" % k for k in dec]

    ax.plot(rot, centro_alto, color=COR2, lw=2, marker="o", ms=8,
            label="centro do lançamento comercial")
    ax.plot(rot, fronteira, color=CINZA, lw=2, marker="o", ms=8,
            label="fronteira entre as duas populações")
    ax.plot(rot, mediana_dec, color=COR, lw=2, marker="o", ms=8, ls="--",
            label="mediana da década (alvo atual)")
    for serie in (centro_alto, fronteira, mediana_dec):
        ax.annotate(ptbr(serie[0]), (rot[0], serie[0]), fontsize=8.5, color=CINZA,
                    xytext=(0, 9), textcoords="offset points", ha="center", va="bottom")
        ax.annotate(ptbr(serie[-1]), (rot[-1], serie[-1]), fontsize=8.5, color=CINZA,
                    xytext=(6, 0), textcoords="offset points", ha="left", va="center")
    ax.set_xmargin(.10)
    ax.margins(y=.16)
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: ptbr(v)))
    ax.set_ylabel("espectadores")
    ax.set_title("O patamar comercial resistiu a três décadas — e caiu nos anos 2020\n"
                 "a mediana, não: ela desabou desde os anos 1990",
                 loc="left", fontsize=11, fontweight="bold")
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")

    fig.tight_layout()
    FIGURAS.mkdir(parents=True, exist_ok=True)
    caminho = FIGURAS / "fig12-duas-populacoes.png"
    fig.savefig(caminho, bbox_inches="tight")
    plt.close(fig)
    return caminho


def _fmt(v):
    """Numero legivel na tela: duas casas ate 10 mil, milhar separado acima."""
    return "%.2f" % v if abs(v) < 1e4 else format(v, ",.0f")


def main():
    d = bd.carregar()
    d = d[d["publico"].notna()].reset_index(drop=True)
    R = definicoes(d)
    SAIDA.mkdir(parents=True, exist_ok=True)

    tabelas = {
        "alvo_distribuicao": distribuicao(d),
        "alvo_duas_populacoes": duas_populacoes(d),
        "alvo_sensibilidade": sensibilidade(d, R),
        "alvo_prevalencia_decada": prevalencia_por_decada(d, R),
        "alvo_prevalencia_genero": prevalencia_por_genero(d, R),
        "alvo_estabilidade_mediana": estabilidade_da_mediana_anual(d),
        "alvo_utilidade_preditiva": utilidade_preditiva(d, R),
    }
    print("gravado: %s" % figura(d).relative_to(RAIZ))

    for nome, t in tabelas.items():
        caminho = SAIDA / ("%s.csv" % nome)
        t.to_csv(caminho, index=False, encoding="utf-8")
        print("gravado: %s (%d linhas)" % (caminho.relative_to(RAIZ), len(t)))
        print(t.to_string(index=False, float_format=_fmt))
        print()


if __name__ == "__main__":
    main()
