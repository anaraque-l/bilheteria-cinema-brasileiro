# Licença dos dados

A [licença MIT](LICENSE) cobre o **código** deste repositório. Os dados em `data/`
são públicos e pertencem aos órgãos que os publicam:

- **ANCINE / OCA** — Observatório Brasileiro do Cinema e do Audiovisual
- **Banco Central do Brasil** — Sistema Gerenciador de Séries Temporais
- **IBGE** — Instituto Brasileiro de Geografia e Estatística

São dados abertos federais, regidos pela **Lei 12.527/2011** (Lei de Acesso à
Informação) e pelo **Decreto 8.777/2016** (Política de Dados Abertos do Poder
Executivo Federal). O uso e a redistribuição são livres, com citação da fonte.
Não há restrição a uso acadêmico e não houve aceite de termo adicional. Os dois
arquivos de fomento da ANCINE declaram, no catálogo, a licença CC-BY, que a
citação da fonte abaixo também cumpre.

Nenhuma das cinco fontes exige cadastro, chave de API ou aceite de termos — foi
condição de escolha do projeto, para que a ingestão seja reproduzível em qualquer
máquina. Ver [`docs/02-decisoes-e-escopo.md`](docs/02-decisoes-e-escopo.md), D1.

As referências completas, com data de acesso, estão em
[`src/fontes.py`](src/fontes.py) e em
[`docs/01-fontes-de-dados.md`](docs/01-fontes-de-dados.md).

## Como citar

> ANCINE. *Listagem dos Filmes Brasileiros Lançados Comercialmente em Salas de
> Exibição 1995 a 2024*. Observatório Brasileiro do Cinema e do Audiovisual.
> Acesso em 10 set. 2026.
>
> ANCINE. *Obras não publicitárias brasileiras com investimento do FSA* e
> *Obras não publicitárias brasileiras com fomento indireto*. Dados abertos da
> ANCINE. Acesso em 10 set. 2026.
>
> BANCO CENTRAL DO BRASIL. *IPCA — variação percentual mensal*. Série 433,
> Sistema Gerenciador de Séries Temporais. Acesso em 10 set. 2026.
>
> IBGE. *População residente estimada*. Agregado 6579, variável 9324, API de
> agregados v3. Acesso em 10 set. 2026.
