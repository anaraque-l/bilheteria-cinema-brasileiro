# -*- coding: utf-8 -*-
"""Baixa as fontes brutas para data/raw/, com cache.

Executar: python src/ingestao.py [chave ...]   (sem argumento roda tudo)

Principios:
  - so biblioteca padrao (urllib), para nao exigir instalacao alem do
    requirements.txt;
  - cache em disco: rodar de novo NAO vai a rede. Para forcar, apague o
    arquivo em data/raw/ ou passe --forcar;
  - o bruto e gravado byte a byte, sem transformacao. Toda limpeza mora em
    build_dataset.py. Assim da para auditar o que o orgao publicou de fato.
"""

import json
import ssl
import sys
import urllib.request
from datetime import date
from pathlib import Path

import fontes

RAIZ = Path(__file__).resolve().parent.parent
BRUTO = RAIZ / "data" / "raw"

CABECALHO = {"User-Agent": "CIn-UFPE-CIN0144-projeto-academico/1.0"}
TEMPO_LIMITE = 90


def _contexto_ssl():
    """Contexto permissivo.

    Alguns servidores do gov.br apresentam cadeia incompleta dependendo do
    ponto de saida da rede. Como so LEMOS dado publico e nao enviamos nada
    sensivel, afrouxar a verificacao aqui e aceitavel e evita que a ingestao
    falhe em maquina de integrante do grupo.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _baixar(url):
    req = urllib.request.Request(url, headers=CABECALHO)
    with urllib.request.urlopen(req, timeout=TEMPO_LIMITE, context=_contexto_ssl()) as r:
        return r.read(), r.headers.get("Content-Type", "")


def _gravar(destino, dados):
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(dados)
    print("    gravado %s (%s bytes)" % (destino.relative_to(RAIZ), f"{len(dados):,}"))


def _ja_existe(destino, forcar):
    if destino.exists() and not forcar:
        print("    cache: %s (%s bytes)" % (destino.relative_to(RAIZ), f"{destino.stat().st_size:,}"))
        return True
    return False


# ---------------------------------------------------------------------------


def ancine_filmes(forcar=False):
    destino = BRUTO / "ancine_filmes_1995_2024r.csv"
    if _ja_existe(destino, forcar):
        return destino
    dados, tipo = _baixar(fontes.ANCINE_FILMES.url)
    # Guarda-chuva contra a pegadinha do Plone: sem /@@download/file o servidor
    # responde 200 com a pagina HTML do arquivo. Falhar aqui e melhor do que
    # gravar HTML e so descobrir no pandas.
    if "html" in tipo.lower() or dados[:200].lstrip().startswith(b"<"):
        raise RuntimeError(
            "A ANCINE devolveu HTML, nao CSV. A URL perdeu o sufixo "
            "/@@download/file? Content-Type=%r" % tipo
        )
    _gravar(destino, dados)
    return destino


def bcb_ipca(forcar=False):
    destino = BRUTO / "bcb_ipca_433.json"
    if _ja_existe(destino, forcar):
        return destino
    dados, _ = _baixar(fontes.BCB_IPCA.url)
    serie = json.loads(dados)
    if not isinstance(serie, list) or not serie:
        raise RuntimeError("Serie 433 do BCB veio vazia ou em formato inesperado.")
    print("    serie 433: %d pontos, de %s a %s"
          % (len(serie), serie[0]["data"], serie[-1]["data"]))
    _gravar(destino, dados)
    return destino


def ibge_populacao(forcar=False):
    destino = BRUTO / "ibge_populacao.json"
    if _ja_existe(destino, forcar):
        return destino
    # Pede a faixa que cobre a base da ANCINE. Anos sem estimativa publicada
    # (os de Censo) simplesmente nao voltam - tratamos em build_dataset.py.
    periodos = "|".join(str(a) for a in range(1995, 2025))
    dados, _ = _baixar(fontes.IBGE_POPULACAO.url.format(periodos=periodos))
    corpo = json.loads(dados)
    serie = corpo[0]["resultados"][0]["series"][0]["serie"]
    print("    IBGE: %d anos com estimativa (%s a %s)"
          % (len(serie), min(serie), max(serie)))
    _gravar(destino, dados)
    return destino


def _fomento(fonte, nome_arquivo, coluna_chave, forcar=False):
    """Baixa um dos dois arquivos de fomento da ANCINE.

    Os dois tem a mesma forma: TITULO_ORIGINAL;CPB;<numero do instrumento>.
    Uma obra aparece uma vez por contrato, entao o arquivo tem mais linhas do
    que obras - a agregacao por CPB e feita em build_dataset.py.
    """
    destino = BRUTO / nome_arquivo
    if _ja_existe(destino, forcar):
        return destino
    dados, _ = _baixar(fonte.url)
    cabecalho = dados[:200].decode("utf-8-sig", "replace").splitlines()[0]
    if coluna_chave not in cabecalho:
        raise RuntimeError(
            "Cabecalho inesperado em %s: esperava %r, veio %r"
            % (nome_arquivo, coluna_chave, cabecalho[:120])
        )
    _gravar(destino, dados)
    return destino


def ancine_fsa(forcar=False):
    return _fomento(fontes.ANCINE_FSA, "ancine_fomento_fsa.csv",
                    "NUMERO_CONTRATO_FSA", forcar)


def ancine_fomento_indireto(forcar=False):
    return _fomento(fontes.ANCINE_FOMENTO_INDIRETO, "ancine_fomento_indireto.csv",
                    "NUMERO_SALIC", forcar)


ETAPAS = {
    "ancine_filmes": ancine_filmes,
    "bcb_ipca": bcb_ipca,
    "ibge_populacao": ibge_populacao,
    "ancine_fsa": ancine_fsa,
    "ancine_fomento_indireto": ancine_fomento_indireto,
}


def main(argv):
    forcar = "--forcar" in argv
    pedidas = [a for a in argv if not a.startswith("--")] or list(ETAPAS)
    desconhecidas = [p for p in pedidas if p not in ETAPAS]
    if desconhecidas:
        raise SystemExit("Etapa desconhecida: %s. Conhecidas: %s"
                         % (desconhecidas, list(ETAPAS)))

    print("Ingestao em %s" % date.today().isoformat())
    for chave in pedidas:
        print("  [%s] %s" % (chave, fontes.POR_CHAVE[chave].nome[:64]))
        ETAPAS[chave](forcar=forcar)
    print("Concluido. Bruto em %s" % BRUTO.relative_to(RAIZ))


if __name__ == "__main__":
    main(sys.argv[1:])
