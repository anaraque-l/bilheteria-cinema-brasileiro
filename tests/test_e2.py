# -*- coding: utf-8 -*-
"""Testes rapidos da Entrega 2: alvo, folds, etapas, robustez, anexo e analise.

Executar: python -m unittest discover -s tests
"""

import itertools
import sys
import unittest
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from e2 import analise, anexo, base, espaco, robustez  # noqa: E402
from e2.etapas import ausentes, balanceamento, encoding, normalizacao, reducao  # noqa: E402
from e2.metricas import SCORING  # noqa: E402


class TestAlvo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.X, cls.y, cls.ano = base.carregar_xy()

    def test_tamanho_e_prevalencia(self):
        self.assertEqual(len(self.y), 2590)
        self.assertAlmostEqual(self.y.mean(), 0.253, places=3)

    def test_alvo_e_binario_e_alinhado_aos_atributos(self):
        self.assertEqual(set(self.y.unique()), {0, 1})
        self.assertEqual(list(self.X.columns), base.ATRIBUTOS)
        self.assertTrue(self.X.index.equals(self.y.index))

    def test_nenhuma_coluna_proibida_entre_os_atributos(self):
        import build_dataset
        self.assertFalse(set(base.ATRIBUTOS) & set(build_dataset.COLUNAS_PROIBIDAS))

    def test_primeiro_ano_nao_tem_alvo(self):
        # sem ano anterior nao ha limiar, entao 1995 sai da base
        self.assertEqual(self.ano.min(), 1996)

    def test_ordinais_nao_tem_ausente(self):
        # a imputacao constante nunca chega a elas
        self.assertEqual(int(self.X[base.ORDINAIS].isna().sum().sum()), 0)

    def test_historico_so_olha_para_tras(self):
        self.assertTrue(base.checar_nao_vazamento())


class TestFolds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.y = base.carregar_xy()[1]
        cls.pares = base.folds()

    def test_cinco_folds_cobrem_a_base_sem_repetir(self):
        testes = np.concatenate([teste for _, teste in self.pares])
        self.assertEqual(len(self.pares), 5)
        self.assertEqual(sorted(testes), list(range(len(self.y))))

    def test_treino_e_teste_nao_se_misturam(self):
        for treino, teste in self.pares:
            self.assertFalse(set(treino) & set(teste))

    def test_estratificado_pelo_alvo(self):
        for _, teste in self.pares:
            self.assertAlmostEqual(self.y.iloc[teste].mean(), self.y.mean(), delta=0.01)

    def test_os_tres_cortes_tem_as_mesmas_linhas(self):
        # a robustez reaproveita estes folds em P50 e P90, o que so vale se as linhas forem as mesmas
        indices = [base.carregar_xy(quantil=q)[0].index for q in (0.50, 0.75, 0.90)]
        self.assertTrue(all(i.equals(indices[1]) for i in indices))

    def test_sempre_os_mesmos(self):
        for (a, b), (c, d) in zip(self.pares, base.folds()):
            self.assertTrue(np.array_equal(a, c) and np.array_equal(b, d))


class TestEtapasDaE2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.X, cls.y, _ = base.carregar_xy()
        cls.treino = base.folds()[0][0]

    def aplica(self, opcao_ausentes, opcao_encoding):
        etapas = make_pipeline(ausentes.OPCOES[opcao_ausentes](), encoding.OPCOES[opcao_encoding]())
        # o aviso do TargetEncoder esta tratado em requirements.txt, e aqui so poluiria a saida
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return etapas.fit_transform(self.X.iloc[self.treino], self.y.iloc[self.treino])

    def test_saida_sem_nan_nas_quatro_combinacoes(self):
        for a in ausentes.OPCOES:
            for e in encoding.OPCOES:
                with self.subTest(ausentes=a, encoding=e):
                    self.assertFalse(np.isnan(self.aplica(a, e).astype(float)).any())

    def test_encoding_pelo_alvo_tem_uma_coluna_por_atributo(self):
        self.assertEqual(self.aplica("mediana_moda", "alvo").shape[1], len(base.ATRIBUTOS))

    def test_indicadora_acrescenta_uma_coluna_por_atributo_com_ausencia(self):
        com = self.aplica("mediana_indicadora", "alvo").shape[1]
        sem = self.aplica("mediana_moda", "alvo").shape[1]
        self.assertEqual(com - sem, 7)

    def test_onehot_gera_bem_mais_colunas_que_o_alvo(self):
        self.assertGreater(self.aplica("mediana_moda", "onehot").shape[1], 4 * len(base.ATRIBUTOS))

    def test_cada_chamada_devolve_objeto_novo(self):
        for modulo in (ausentes, encoding, normalizacao, reducao, balanceamento):
            for fabrica in modulo.OPCOES.values():
                if fabrica() != "passthrough":
                    self.assertIsNot(fabrica(), fabrica())

    def test_toda_opcao_tem_justificativa(self):
        for modulo in (ausentes, encoding, normalizacao, reducao, balanceamento):
            self.assertEqual(set(modulo.OPCOES), set(modulo.JUSTIFICATIVA))

    def test_codigo_do_baseline(self):
        self.assertEqual(espaco.codigo(espaco.BASELINE), "mediana_moda|onehot|sem|sem|sem")


def grade_inventada():
    """Doze combinacoes no formato de resultados.csv, com a ultima falhando."""
    opcoes = [["mediana_moda", "mediana_indicadora"], ["onehot", "alvo"], ["sem"], ["sem"],
              ["sem", "subamostragem", "smote"]]
    linhas = []
    for i, escolha in enumerate(itertools.product(*opcoes), start=1):
        linha = {"id": i, **dict(zip(espaco.ETAPAS, escolha)), "eh_baseline": int(i == 1),
                 "n_atributos": 18.0, "tempo_total_s": 1.0, "erro": None}
        for m in SCORING:
            linha[m + "_media"], linha[m + "_dp"] = 0.5 + i / 100, 0.01
        linhas.append(linha)
    grade = pd.DataFrame(linhas)
    grade.loc[grade["id"] == 12, [m + "_media" for m in SCORING]] = np.nan
    grade.loc[grade["id"] == 12, "erro"] = "ValueError: falhou"
    return grade


class TestRobustezEAnexo(unittest.TestCase):
    def test_selecao_tem_o_baseline_e_nao_repete(self):
        ids = list(robustez.selecionar(grade_inventada())["id"])
        self.assertIn(1, ids)
        self.assertEqual(len(ids), len(set(ids)))

    def test_selecao_ignora_quem_falhou_e_cobre_os_balanceamentos(self):
        escolhidas = robustez.selecionar(grade_inventada())
        self.assertNotIn(12, list(escolhidas["id"]))
        self.assertEqual(set(escolhidas["balanceamento"]), {"sem", "subamostragem", "smote"})

    def test_anexo_tem_uma_linha_por_combinacao(self):
        tabela = anexo.tabela(grade_inventada())
        self.assertEqual(len(tabela), 12)
        self.assertTrue(tabela["id"].iloc[0].endswith("(base)"))
        self.assertEqual(tabela["AUC"].iloc[-1], "—")


class TestMontagemDoRelatorio(unittest.TestCase):
    """A montagem encaixa a secao das metricas dentro da §4 por indice.

    Se alguem puser 4-metricas na ORDEM, o paragrafo sai duas vezes e ninguem
    percebe lendo o .md de ponta a ponta. Foi o que chegou ao documento final.
    """

    @classmethod
    def setUpClass(cls):
        import montar_relatorio_e2 as montagem
        cls.texto = montagem.montar()

    def paragrafos(self):
        # so os de texto corrido; tabela e figura repetem celula por natureza
        return [p.strip() for p in self.texto.split("\n\n")
                if len(p.split()) > 25 and not p.lstrip().startswith(("|", "!", ">"))]

    def test_nenhum_paragrafo_aparece_duas_vezes(self):
        vistos = set()
        for p in self.paragrafos():
            self.assertNotIn(p[:120], vistos, "paragrafo repetido na montagem")
            vistos.add(p[:120])

    def test_o_paragrafo_das_metricas_entra_uma_vez(self):
        self.assertEqual(self.texto.count("O filme de sucesso é a classe positiva"), 1)

    def test_a_marca_da_tabela_do_anexo_foi_substituida(self):
        import montar_relatorio_e2 as montagem
        self.assertNotIn(montagem.MARCA_TABELA, self.texto)


class TestGradeCompleta(unittest.TestCase):
    def test_sao_144_combinacoes_com_um_unico_baseline(self):
        todas = espaco.combinacoes()
        self.assertEqual(len(todas), 144)
        self.assertEqual([c["id"] for c in todas], list(range(1, 145)))
        self.assertEqual(sum(espaco.eh_baseline(c) for c in todas), 1)


def grade_plantada():
    """As 144 combinacoes com dois efeitos conhecidos e nenhum ruido.

    Normalizar soma 0,04 em qualquer contexto, e o PCA tira 0,06 so quando nao ha
    normalizacao. O resto nao muda nada.
    """
    linhas = []
    for c in espaco.combinacoes():
        auc = 0.80 + 0.04 * (c["normalizacao"] != "sem")
        auc -= 0.06 * (c["reducao"] == "pca" and c["normalizacao"] == "sem")
        linha = {"id": c["id"], "codigo": espaco.codigo(c), **{e: c[e] for e in espaco.ETAPAS},
                 "eh_baseline": int(espaco.eh_baseline(c)), "n_atributos": 18.0,
                 "tempo_total_s": 1.0, "erro": None}
        for m in SCORING:
            linha[m + "_media"], linha[m + "_dp"] = auc, 0.01
        linhas.append(linha)
    return pd.DataFrame(linhas)


class TestAnalise(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grade = grade_plantada()

    def test_regra_de_empate(self):
        a = {"roc_auc_media": 0.80, "roc_auc_dp": 0.01}
        self.assertTrue(analise.empata(a, {"roc_auc_media": 0.805, "roc_auc_dp": 0.002}, "roc_auc"))
        self.assertFalse(analise.empata(a, {"roc_auc_media": 0.82, "roc_auc_dp": 0.002}, "roc_auc"))

    def test_recupera_o_efeito_plantado_da_normalizacao(self):
        efeito = analise.efeito_por_etapa(self.grade, "normalizacao").set_index("opcao")
        for opcao in ("padrao", "minmax", "robusto"):
            self.assertEqual(efeito.loc[opcao, "vitorias"], 36)
            self.assertEqual(efeito.loc[opcao, "derrotas"], 0)

    def test_etapa_sem_efeito_so_empata(self):
        efeito = analise.efeito_por_etapa(self.grade, "encoding").set_index("opcao")
        self.assertEqual(efeito.loc["alvo", "empates"], 72)

    def test_acha_a_interacao_plantada_e_nenhuma_outra(self):
        tabela = analise.interacoes(self.grade, "reducao", "normalizacao").set_index(["opcao_a", "opcao_b"])
        self.assertEqual(tabela.loc[("pca", "sem"), "veredito"], "perde")
        self.assertEqual(tabela.loc[("pca", "padrao"), "veredito"], "empata")
        self.assertTrue(tabela.loc[("pca", "sem"), "interacao"])
        self.assertFalse(tabela.loc[("kbest", "sem"), "interacao"])

    def test_ranking_comeca_pela_melhor_e_inclui_o_baseline(self):
        r = analise.ranking(self.grade)
        self.assertEqual(r["roc_auc_media"].iloc[0], r["roc_auc_media"].max())
        self.assertEqual(len(r), 144)
        self.assertTrue(r["empata_com_a_melhor"].iloc[0])


if __name__ == "__main__":
    unittest.main()
