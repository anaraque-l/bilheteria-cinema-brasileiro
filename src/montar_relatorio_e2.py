# -*- coding: utf-8 -*-
"""Monta o relatorio da Entrega 2 a partir das secoes.

Executar: python src/montar_relatorio_e2.py [--docx]

Cada secao mora num arquivo de docs/e2/secoes, com a linha da dona no topo. A montagem
junta as secoes na ordem do relatorio, tira a linha da dona, encaixa o paragrafo das
metricas no fim da secao 4 e poe a tabela das 144 no anexo. Com --docx, gera tambem o
.docx pelo pandoc, com A4, Arial 11 e tabelas em corpo 9 do modelo docs/e2/estilo-relatorio.docx.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SECOES = RAIZ / "docs" / "e2" / "secoes"
SAIDA_MD = RAIZ / "docs" / "e2" / "relatorio-entrega2.md"
SAIDA_DOCX = RAIZ / "docs" / "e2" / "Relatorio_Entrega_2_Grupo_11.docx"
MODELO_DOCX = RAIZ / "docs" / "e2" / "estilo-relatorio.docx"

# largura de cada figura no .docx; o Markdown nao tem como dizer isso
LARGURA = {"fig-al-ranking": "100%", "fig-al-interacoes": "100%",
           "fig-lf-auc-5fold-temporal": "50%"}

ORDEM = ["1-contexto", "2-base-alvo-atributos", "3-1-ausentes", "3-2-encoding",
         "3-3-normalizacao", "3-4-reducao", "3-5-balanceamento", "4-protocolo",
         "5-1-visao-geral", "5-2-efeitos-isolados", "5-3-interacoes", "5-4-custo",
         "6-robustez", "7-licoes-conclusao", "anexo"]

CABECALHO = """# Pré-processamento e pipelines na previsão de sucesso de bilheteria do cinema brasileiro

**Entrega 2 · CIN0144 — Aprendizado de Máquina e Ciência de Dados · Grupo 11**
Ana Laura, Ana Raquel e Laura Virginia

---

"""

# a secao 4 cita o paragrafo da Laura; ele entra no fim dela
METRICAS = "4-metricas"
MARCA_TABELA = "<!-- tabela: reports/e2/anexo_144.md -->"


def ler(nome):
    """Texto da secao sem a linha da dona e com as figuras apontadas a partir de docs/e2."""
    texto = (SECOES / (nome + ".md")).read_text(encoding="utf-8")
    texto = texto.replace("](../../../reports/", "](../../reports/")
    return "\n".join(linha for linha in texto.split("\n") if not linha.startswith("> Dona"))


def montar():
    partes = [ler(nome) for nome in ORDEM]
    # o paragrafo das metricas entra sem o titulo, as duas linhas em branco e a da dona
    metricas = (SECOES / (METRICAS + ".md")).read_text(encoding="utf-8").split("\n", 3)[3]
    i = ORDEM.index("4-protocolo")
    partes[i] = partes[i] + "\n\n" + metricas.rstrip("\n") + "\n"
    texto = CABECALHO + "\n".join(partes) + "\n"
    tabela = (RAIZ / "reports" / "e2" / "anexo_144.md").read_text(encoding="utf-8").strip()
    return texto.replace(MARCA_TABELA, tabela)


def gerar_docx():
    if shutil.which("pandoc") is None:
        sys.exit("pandoc nao encontrado; o .md foi gerado, o .docx nao")
    texto = SAIDA_MD.read_text(encoding="utf-8")
    for nome, largura in LARGURA.items():
        texto = re.sub(r"(/%s\.png\))" % re.escape(nome), r"\1{width=%s}" % largura, texto)
    temporario = SAIDA_MD.with_name("montagem-docx.md")
    temporario.write_text(texto, encoding="utf-8")
    try:
        subprocess.run(["pandoc", temporario.name, "-o", SAIDA_DOCX.name,
                        "--reference-doc", str(MODELO_DOCX)],
                       cwd=SAIDA_MD.parent, check=True)
    finally:
        temporario.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--docx", action="store_true", help="gera tambem o .docx")
    args = parser.parse_args()
    SAIDA_MD.write_text(montar(), encoding="utf-8")
    print("gravado: %s" % SAIDA_MD.relative_to(RAIZ).as_posix())
    if args.docx:
        gerar_docx()
        print("gravado: %s" % SAIDA_DOCX.relative_to(RAIZ).as_posix())


if __name__ == "__main__":
    main()
