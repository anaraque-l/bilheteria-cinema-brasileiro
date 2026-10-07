# -*- coding: utf-8 -*-
"""Testes rapidos da Entrega 1: tipagem, historico e a base montada.

Executar: python -m unittest discover -s tests
"""

import sys
import ssl
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import build_dataset as bd  # noqa: E402
import ingestao  # noqa: E402


class TestTipagem(unittest.TestCase):
    def test_numero_ptbr_com_ponto_de_milhar(self):
        self.assertEqual(bd._num_ptbr(pd.Series(["1.286.000"])).iloc[0], 1286000.0)

    def test_numero_ptbr_com_virgula_decimal(self):
        s = pd.Series(["6.430.000,00"])
        self.assertEqual(bd._num_ptbr(s, decimal=True).iloc[0], 6430000.0)

    def test_falta_numerica_vira_nan(self):
        s = bd._num_ptbr(pd.Series(["ND", "-", "12"]))
        self.assertTrue(s.iloc[:2].isna().all())
        self.assertEqual(s.iloc[2], 12)

    def test_falta_em_texto_vira_nan_e_nao_categoria(self):
        # sem isso o ND de uma coluna de texto viraria um genero ou uma distribuidora
        s = bd._texto(pd.Series(["Ficção", "-", "ND", " "]))
        self.assertEqual(s.iloc[0], "Ficção")
        self.assertTrue(s.iloc[1:].isna().all())

    def test_uf_principal_pega_o_primeiro_codigo(self):
        uf = bd._uf_principal(pd.Series(["RJ", "SP/RJ", " -/DF", "-", "PE/RS/RJ/SP"]))
        self.assertEqual(uf.iloc[0], "RJ")
        self.assertEqual(uf.iloc[1], "SP")
        self.assertEqual(uf.iloc[2], "DF")
        self.assertTrue(pd.isna(uf.iloc[3]))
        self.assertEqual(uf.iloc[4], "PE")


class TestHistorico(unittest.TestCase):
    def test_conta_so_anos_anteriores(self):
        d = pd.DataFrame({"direcao": ["A", "A", "A", "B"], "ano": [2000, 2000, 2001, 2001]})
        # dois filmes de A em 2000 nao contam entre si, e os dois contam para 2001
        self.assertEqual(list(bd._historico_anterior(d, "direcao")), [0, 0, 2, 0])

    def test_entidade_ausente_fica_sem_historico(self):
        d = pd.DataFrame({"direcao": ["A", None, "A"], "ano": [2000, 2000, 2001]})
        h = bd._historico_anterior(d, "direcao")
        self.assertTrue(np.isnan(h[1]))
        self.assertEqual(h[2], 1)


class TestBaseMontada(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = bd.carregar()

    def test_dimensoes_da_entrega(self):
        self.assertEqual(self.d.shape, (2626, 35))

    def test_alvo_global_e_equilibrado_por_construcao(self):
        y = self.d["sucesso_global"].dropna()
        self.assertEqual(len(y), 2604)
        self.assertAlmostEqual(y.mean(), 0.5, places=3)

    def test_ordinais_voltam_ordenadas(self):
        for coluna, ordem in bd.ORDEM_ORDINAIS.items():
            tipo = self.d[coluna].dtype
            self.assertTrue(tipo.ordered)
            self.assertEqual(list(tipo.categories), ordem)

    def test_colunas_proibidas_nao_sao_atributos(self):
        legitimos = set(bd.atributos_legitimos(self.d))
        self.assertFalse(legitimos & set(bd.COLUNAS_PROIBIDAS))
        self.assertFalse(legitimos & {"cpb", "titulo"})


class TestIngestao(unittest.TestCase):
    def test_certificado_e_verificado_por_padrao(self):
        self.assertTrue(ingestao.VERIFICAR_SSL)
        ctx = ingestao._contexto_ssl()
        self.assertEqual(ctx.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(ctx.check_hostname)


if __name__ == "__main__":
    unittest.main()
