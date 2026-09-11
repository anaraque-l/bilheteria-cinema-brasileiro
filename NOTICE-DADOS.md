# Licenca dos dados

A [licenca MIT](LICENSE) cobre o **codigo** deste repositorio. Os dados em `data/`
sao publicos e pertencem aos orgaos que os publicam:

- **ANCINE / OCA** — Observatorio Brasileiro do Cinema e do Audiovisual
- **Banco Central do Brasil** — Sistema Gerenciador de Series Temporais
- **IBGE** — Instituto Brasileiro de Geografia e Estatistica

Sao dados abertos federais, regidos pela **Lei 12.527/2011** (Lei de Acesso a
Informacao) e pelo **Decreto 8.777/2016** (Politica de Dados Abertos do Poder
Executivo Federal). O uso e a redistribuicao sao livres, com citacao da fonte.
Nao ha restricao a uso academico e nao houve aceite de termo adicional.

Nenhuma das tres fontes exige cadastro, chave de API ou aceite de termos — foi
condicao de escolha do projeto, para que a ingestao seja reproduzivel em qualquer
maquina. Ver [`docs/02-decisoes-e-escopo.md`](docs/02-decisoes-e-escopo.md), D1.

As referencias completas, com data de acesso, estao em
[`src/fontes.py`](src/fontes.py) e em
[`docs/01-fontes-de-dados.md`](docs/01-fontes-de-dados.md).

## Como citar

> ANCINE. *Listagem dos Filmes Brasileiros Lancados Comercialmente em Salas de
> Exibicao 1995 a 2024*. Observatorio Brasileiro do Cinema e do Audiovisual.
> Acesso em 10 set. 2026.
>
> BANCO CENTRAL DO BRASIL. *IPCA — variacao percentual mensal*. Serie 433,
> Sistema Gerenciador de Series Temporais. Acesso em 10 set. 2026.
>
> IBGE. *Populacao residente estimada*. Agregado 6579, variavel 9324, API de
> agregados v3. Acesso em 10 set. 2026.
