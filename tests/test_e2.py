# -*- coding: utf-8 -*-
"""Testes rapidos da Entrega 2: alvo, folds e as etapas de ausentes e encoding.

Executar: python -m unittest discover -s tests

Os testes da grade completa ficam pulados enquanto normalizacao, reducao e
balanceamento nao existirem em src/e2/etapas, e passam a rodar quando entrarem.
"""

import importlib.util
import itertools
import sys
import unittest
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from e2 import anexo, base, espaco, robustez  # noqa: E402
from e2.etapas import ausentes, balanceamento, encoding  # noqa: E402
from e2.metricas import SCORING  # noqa: E402

GRADE_COMPLETA = all(
    importlib.util.find_spec("e2.etapas." + etapa) is not None
    for etapa in ("normalizacao", "reducao", "balanceamento")
)


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
        for modulo in (ausentes, encoding, balanceamento):
            for fabrica in modulo.OPCOES.values():
                if fabrica() != "passthrough":
                    self.assertIsNot(fabrica(), fabrica())

    def test_toda_opcao_tem_justificativa(self):
        for modulo in (ausentes, encoding, balanceamento):
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


@unittest.skipUnless(GRADE_COMPLETA, "faltam etapas da grade em src/e2/etapas")
class TestGradeCompleta(unittest.TestCase):
    def test_sao_144_combinacoes_com_um_unico_baseline(self):
        todas = espaco.combinacoes()
        self.assertEqual(len(todas), 144)
        self.assertEqual([c["id"] for c in todas], list(range(1, 145)))
        self.assertEqual(sum(espaco.eh_baseline(c) for c in todas), 1)


if __name__ == "__main__":
    unittest.main()
