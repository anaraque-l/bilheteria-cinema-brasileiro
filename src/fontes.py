# -*- coding: utf-8 -*-
"""Registro unico das fontes de dados do projeto.

Regra do projeto: nenhuma URL entra no notebook ou em outro modulo. Toda fonte
mora aqui, com licenca, cobertura e a data em que o endpoint foi testado de
verdade. Se uma fonte cair, o conserto e num lugar so.

Todas as tres fontes sao publicas, federais e nao exigem cadastro, chave de
API nem aceite de termos. Isso e requisito do projeto: qualquer integrante do
grupo (e o professor) reproduz a ingestao numa maquina limpa.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Fonte:
    """Uma fonte de dados externa, com tudo o que precisa ser citado."""

    chave: str
    nome: str
    orgao: str
    url: str
    formato: str
    licenca: str
    cobertura: str
    testado_em: str
    observacoes: str = ""
    campos: tuple = field(default=())


# ---------------------------------------------------------------------------
# Fonte primaria
# ---------------------------------------------------------------------------

ANCINE_FILMES = Fonte(
    chave="ancine_filmes",
    nome="Listagem dos Filmes Brasileiros Lancados Comercialmente em Salas de Exibicao",
    orgao="ANCINE / OCA - Observatorio Brasileiro do Cinema e do Audiovisual",
    # O gov.br roda Plone. A URL "bonita" devolve a PAGINA do arquivo (text/html,
    # ~323 KB). O arquivo mesmo so vem com o sufixo /@@download/file. Isso ja
    # custou tempo: sem o sufixo, o pandas le HTML e falha com erro de parsing.
    url=(
        "https://www.gov.br/ancine/pt-br/oca/cinema/arquivos.csv/"
        "listagem-de-filmes-brasileiros-lancados-1995-a-2024r.csv/@@download/file"
    ),
    formato="CSV, separador ';', UTF-8 com BOM, decimal pt-BR",
    # Dado aberto governamental federal. A Lei 12.527/2011 (LAI) e o Decreto
    # 8.777/2016 (Politica de Dados Abertos) obrigam formato aberto e uso livre.
    # Nao ha clique de aceite nem termo adicional no portal do OCA.
    licenca="Dado aberto federal (Lei 12.527/2011 + Decreto 8.777/2016) - uso livre com citacao da fonte",
    cobertura="Filmes brasileiros de longa-metragem lancados comercialmente, 1995 a 2024",
    testado_em="2026-09-10",
    observacoes=(
        "NAO existe edicao 1995-2025 publicada ate 2026-09-10: as variantes "
        "'1995-a-2025' e '1995-a-2025r' devolvem 404. A edicao vigente e "
        "'2024r' (o sufixo 'r' e de retificada; ela e 22 bytes maior que a "
        "'2024' e e a que o portal linka). O arquivo traz um bloco de ~47 "
        "linhas de notas de rodape no fim, que NAO sao filmes."
    ),
    campos=(
        "Ano de Lancamento", "Certificado de Produto Brasileiro (CPB)", "Titulo",
        "Direcao", "Genero", "Empresa Produtora Brasileira Majoritaria", "UF",
        "Empresa Produtora Minoritaria Brasileira", "UF2", "Distribuidora",
        "Maximo de Salas", "Publico acumulado", "Renda (R$) acumulada",
    ),
)


# ---------------------------------------------------------------------------
# Fontes complementares
# ---------------------------------------------------------------------------

BCB_IPCA = Fonte(
    chave="bcb_ipca",
    nome="IPCA - variacao percentual mensal (serie 433 do SGS)",
    orgao="Banco Central do Brasil - Sistema Gerenciador de Series Temporais",
    # ATENCAO: passar dataInicial/dataFinal nesta serie devolveu erro nos testes
    # de 10/09/2026. Baixamos a serie inteira (559 pontos, ~20 KB) e filtramos
    # em memoria. E mais barato do que descobrir o formato de data aceito.
    url="https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json",
    formato="JSON, lista de {data: 'dd/mm/aaaa', valor: 'x.yz'}",
    licenca="Dado aberto federal - uso livre, sem cadastro nem chave",
    cobertura="Janeiro/1980 ate o mes corrente (2026-07 no teste)",
    testado_em="2026-09-10",
    observacoes=(
        "Serve para deflacionar a renda de bilheteria. A renda da ANCINE esta "
        "em reais correntes da epoca do lancamento: comparar 1995 com 2024 sem "
        "deflacionar e comparar moedas diferentes. O deflator NAO entra como "
        "atributo do modelo - entra para tornar a renda legivel na EDA."
    ),
)

IBGE_POPULACAO = Fonte(
    chave="ibge_populacao",
    nome="Populacao residente estimada (agregado 6579, variavel 9324)",
    orgao="IBGE - API de agregados v3 (servicodados)",
    url=(
        "https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/"
        "{periodos}/variaveis/9324?localidades=N1[all]"
    ),
    formato="JSON aninhado (resultados > series > serie)",
    licenca="Dado aberto federal - uso livre, sem cadastro nem chave",
    cobertura="Brasil, serie anual. Anos de Censo faltam nas estimativas.",
    testado_em="2026-09-10",
    observacoes=(
        "Serve para calcular publico per capita e mostrar que o crescimento do "
        "publico do cinema nacional nao e so crescimento populacional. "
        "O host apisidra.ibge.gov.br NAO resolve DNS neste ambiente; use "
        "servicodados.ibge.gov.br, que foi testado e responde."
    ),
)


# ---------------------------------------------------------------------------
# Fomento publico - fontes ativas
# ---------------------------------------------------------------------------
# O fomento e APROVADO antes de a obra existir, o que torna estas duas fontes
# legitimamente anteriores a estreia - entram na base sem risco de vazamento.
#
# COMO FORAM ENCONTRADAS - registrar isso importa: o host NAO e o gov.br.
# O catalogo dados.gov.br e uma SPA; o HTML cru nao traz URL de arquivo e a API
# devolve 401 para cliente externo. Renderizando a pagina num navegador, a mesma
# API responde 200 e o campo `resources[].url` aponta para dados.ancine.gov.br,
# um dominio separado que nao aparece em lugar nenhum do portal do OCA.

ANCINE_FSA = Fonte(
    chave="ancine_fsa",
    nome="Obras Nao Publicitarias Brasileiras com Investimento do FSA",
    orgao="ANCINE - Fundo Setorial do Audiovisual",
    url="https://dados.ancine.gov.br/dados-abertos/obras-nao-pub-brasileiras-investimento-fsa.csv",
    formato="CSV, separador ';', UTF-8 com BOM, 138 KB",
    licenca="Creative Commons Attribution (CC-BY) - declarada no catalogo",
    cobertura="Obras com contrato do FSA; uma linha por contrato",
    testado_em="2026-09-10",
    observacoes=(
        "Junta na listagem por CPB. ATENCAO ao que ela NAO tem: o arquivo traz "
        "TITULO_ORIGINAL;CPB;NUMERO_CONTRATO_FSA e nenhum VALOR. Da para derivar "
        "'recebeu FSA' (binaria) e 'quantos contratos' (contagem), nao o "
        "orcamento. Uma obra aparece varias vezes, uma por contrato - agregue por "
        "CPB antes de juntar, ou a listagem duplica."
    ),
    campos=("TITULO_ORIGINAL", "CPB", "NUMERO_CONTRATO_FSA"),
)

ANCINE_FOMENTO_INDIRETO = Fonte(
    chave="ancine_fomento_indireto",
    nome="Obras Brasileiras com Fomento Indireto Aprovado (leis de incentivo)",
    orgao="ANCINE",
    url="https://dados.ancine.gov.br/dados-abertos/obras-nao-pub-brasileiras-fomento-indireto.csv",
    formato="CSV, separador ';', 140 KB",
    licenca="Creative Commons Attribution (CC-BY)",
    cobertura="Obras com projeto aprovado nas leis de incentivo federais",
    testado_em="2026-09-10",
    observacoes=(
        "Mesma estrutura do FSA, com NUMERO_SALIC no lugar do contrato. Tambem "
        "sem valor. Fomento e APROVADO antes de a obra existir, entao a variavel "
        "derivada e legitimamente anterior a estreia - nao ha risco de vazamento, "
        "ao contrario do que a primeira versao deste projeto supunha. Casa em "
        "67,1% dos filmes com CPB (31,2% FSA, 54,1% leis de incentivo)."
    ),
    campos=("TITULO_ORIGINAL", "CPB", "NUMERO_SALIC"),
)

ANCINE_BILHETERIA_DIARIA = Fonte(
    chave="ancine_bilheteria_diaria",
    nome="Relatorio de bilheteria diaria de obras informadas pelas distribuidoras",
    orgao="ANCINE - Sistema de Controle de Bilheteria (SCB)",
    url="https://dados.ancine.gov.br/dados-abertos/bilheteria-diaria-obras-por-distribuidoras-csv.zip",
    formato="ZIP com 152 CSV mensais (latin-1, ';'). 486 MB comprimido, ~3,8 GB aberto",
    licenca="Creative Commons Attribution (CC-BY)",
    cobertura="2014-01 a 2026-08. Cobre 1.617 dos 2.626 filmes da base (61,6%)",
    testado_em="2026-09-10",
    observacoes=(
        "E a fonte que resolve o problema aberto de docs/02, D6. Uma linha por "
        "obra x sala x dia. De min(DATA_EXIBICAO) por CPB sai a DATA EXATA DE "
        "ESTREIA; contando REGISTRO_SALA distintos nos 7 primeiros dias sai "
        "SALAS NA PRIMEIRA SEMANA - que e decidida antes de o desempenho ser "
        "conhecido e portanto NAO e vazamento, ao contrario de max_salas. "
        "Nao carregue os 152 arquivos de uma vez: processe mes a mes e agregue."
    ),
    campos=(
        "DATA_EXIBICAO", "TITULO_ORIGINAL", "TITULO_BRASIL", "CPB_ROE",
        "PAIS_OBRA", "REGISTRO_SALA", "NOME_SALA", "PUBLICO",
        "REGISTRO_GRUPO_EXIBIDOR", "REGISTRO_EXIBIDOR", "REGISTRO_COMPLEXO",
        "MUNICIPIO_SALA_COMPLEXO", "UF_SALA_COMPLEXO",
        "RAZAO_SOCIAL_DISTRIBUIDORA", "CNPJ_DISTRIBUIDORA",
    ),
)

# A bilheteria diaria continua reservada: 486 MB e cobre so 2014 em diante.
PARA_ENTREGA_2 = (ANCINE_BILHETERIA_DIARIA,)


TODAS = (ANCINE_FILMES, BCB_IPCA, IBGE_POPULACAO,
         ANCINE_FSA, ANCINE_FOMENTO_INDIRETO)

POR_CHAVE = {f.chave: f for f in TODAS}


# ---------------------------------------------------------------------------
# Fontes avaliadas e DESCARTADAS
# ---------------------------------------------------------------------------
# Registrar o que nao deu certo evita que o proximo integrante do grupo gaste
# a mesma tarde. Cada linha foi testada em 2026-09-10.

DESCARTADAS = {
    "wikidata": (
        "query.wikidata.org nao resolve DNS neste ambiente (getaddrinfo failed). "
        "Era o plano para trazer duracao do filme (P2047), que a ANCINE nao "
        "publica. Licenca seria CC0, ideal. Se voce estiver numa rede que "
        "alcance o endpoint, vale reabrir: ver docs/03-melhorias-e-tradeoffs.md, "
        "melhoria M6."
    ),
    "dados.gov.br_api": (
        "https://dados.gov.br/api/publico/... devolve HTTP 401 para cliente "
        "externo (urllib, curl). NAO exige chave: a mesma URL responde 200 "
        "quando chamada de dentro da pagina renderizada, e e assim que se "
        "descobre o campo resources[].url. Foi o caminho que revelou o host "
        "dados.ancine.gov.br - ver PARA_ENTREGA_2."
    ),
    "apisidra.ibge.gov.br": (
        "Nao resolve DNS neste ambiente. Substituido por servicodados.ibge.gov.br."
    ),
    "listagem_de_pastas_do_OCA": (
        "https://www.gov.br/ancine/pt-br/oca/cinema e .../arquivos.csv devolvem "
        "HTTP 401 (permissao do Plone). Nao da para listar o diretorio: as URLs "
        "de arquivo precisam ser descobertas uma a uma."
    ),
    "tmdb": (
        "A API do TMDB traz duracao, orcamento e elenco, mas exige cadastro e "
        "chave. O projeto decidiu nao depender de credencial (ver docs/02, D1). "
        "Fica como extensao opcional para a Entrega 2."
    ),
}
