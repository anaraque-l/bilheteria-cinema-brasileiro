# Fontes de dados

Todas testadas em **10/09/2026**. O registro executável está em
[`../src/fontes.py`](../src/fontes.py) — este documento é a versão longa.

Nenhuma fonte exige cadastro, chave de API ou aceite de termos. A restrição é
deliberada: qualquer integrante do grupo e o professor precisam reproduzir a ingestão
numa máquina limpa.

---

## 1. ANCINE — Listagem dos Filmes Brasileiros Lançados (primária)

**Órgão.** ANCINE / OCA — Observatório Brasileiro do Cinema e do Audiovisual.

**URL.**
```
https://www.gov.br/ancine/pt-br/oca/cinema/arquivos.csv/
listagem-de-filmes-brasileiros-lancados-1995-a-2024r.csv/@@download/file
```

> ⚠️ **O sufixo `/@@download/file` é obrigatório.** O portal roda Plone: sem ele, o
> servidor responde **HTTP 200 com a página HTML do arquivo** (~323 KB), não o CSV.
> O pandas lê o HTML e falha com erro de parsing que não aponta para a causa.
> `ingestao.py` detecta e falha explicitamente.

**Formato.** CSV, separador `;`, UTF-8 **com BOM**, números em pt-BR.

**Cobertura.** Filmes brasileiros de longa-metragem lançados comercialmente em salas de
exibição, 1995–2024. **2.626 registros.**

**Licença.** Dado aberto federal — Lei 12.527/2011 (LAI) e Decreto 8.777/2016. Uso
livre, com citação da fonte. Não há clique de aceite nem termo adicional no portal.

**Campos publicados (13).**

| campo | tipo | observação |
|---|---|---|
| Ano de Lançamento | temporal | 1995–2024 |
| Certificado de Produto Brasileiro (CPB) | identificador | chave da ANCINE; 14 registros com `-` |
| Título | identificador | 6 títulos repetidos em anos distintos |
| Direção | categórica | 1.738 distintos |
| Gênero | categórica | **só 4**: Ficção, Documentário, Animação, Videomusical (n=1) |
| Empresa Produtora Brasileira Majoritária | categórica | 1.502 distintos |
| UF | categórica | **87 valores distintos para 27 UFs** (90 no bruto) — ver abaixo |
| Empresa Produtora Minoritária | categórica | `-` em 60% (não houve coprodução) |
| UF2 | categórica | idem |
| Distribuidora | categórica | 467 distintos |
| Máximo de Salas | numérica | `ND` em 2,1% |
| Público acumulado | numérica | **origem do alvo**; `ND` em 0,8% |
| Renda (R$) acumulada | numérica | reais correntes da época |

### Armadilhas confirmadas

1. **Rodapé lido como dado.** O arquivo termina com ~47 linhas de notas metodológicas
   que o pandas lê como filmes. Corte: linha de filme tem ano com exatamente 4 dígitos.
2. **Falta é texto, não `NaN`.** `ND` e `-`. Sem traduzir, a coluna numérica vira
   `object` e `ND` vira categoria legítima.
3. **Números em pt-BR.** `1.286.000` (ponto = milhar) e `6.430.000,00` (vírgula =
   decimal). Ler sem tratar dá valores mil vezes errados.
4. **UF concatenada.** A ANCINE junta as UFs num campo só: `RJ/RJ`, `SP/RJ`,
   `PE/RS/RJ/SP`, ` -/DF`, `-`. Daí 87 valores distintos (90 no arquivo bruto, antes de
   normalizar espaço e marcar `-` como ausente). `build_dataset.py` extrai o primeiro
   código de duas letras para `uf_maj` (24 valores) e **preserva** o original em
   `uf_bruto` para auditoria.
5. **Entidade fragmentada.** `Downtown` (65 filmes), `Paris` (59) e `Downtown/Paris`
   (92) são categorias distintas para as mesmas empresas em arranjos diferentes.

### A edição 1995–2025 não existe

Várias referências mencionam uma listagem *1995–2025*. Em 10/09/2026 ela **não está
publicada**: as URLs `...1995-a-2025.csv` e `...1995-a-2025r.csv` devolvem **HTTP 404**.
A edição vigente é a **`2024r`** (`r` de retificada), que é a linkada pelo portal e é
22 bytes maior que a `2024`.

**Trabalhamos com 1995–2024 e dizemos isso no relatório.** Inventar dois anos de dados
para casar com um enunciado seria o oposto do que a disciplina cobra.

---

## 2. ANCINE — Fomento público (FSA e leis de incentivo)

**URLs testadas em 10/09/2026:**

```
https://dados.ancine.gov.br/dados-abertos/obras-nao-pub-brasileiras-investimento-fsa.csv
https://dados.ancine.gov.br/dados-abertos/obras-nao-pub-brasileiras-fomento-indireto.csv
```

**Formato.** CSV, separador `;`, UTF-8 com BOM. 138 KB e 140 KB.

| arquivo | colunas | linhas | CPBs distintos |
|---|---|---|---|
| FSA | `TITULO_ORIGINAL` · `CPB` · `NUMERO_CONTRATO_FSA` | 3.301 | 2.869 |
| fomento indireto | `TITULO_ORIGINAL` · `CPB` · `NUMERO_SALIC` | 3.179 | 3.082 |

**Licença.** **Creative Commons Attribution (CC-BY)**, declarada nominalmente no
catálogo — mais explícita que o arcabouço geral da LAI que rege as outras fontes.

**Cobertura da junção.** Por CPB, casam com **67,1%** dos 2.612 filmes com CPB válido:
31,2% têm FSA, 54,1% têm incentivo.

> ⚠️ **Estes arquivos não estão no portal do OCA, e o host não é o gov.br.** O catálogo
> `dados.gov.br` é uma aplicação de página única: o HTML cru não traz URL de arquivo, e
> a API devolve **HTTP 401** para cliente externo. Renderizada num navegador, a mesma
> API responde 200 e o campo `resources[].url` aponta para **`dados.ancine.gov.br`** —
> um domínio separado que não é linkado de lugar nenhum.

> ⚠️ **Agregue por CPB antes de juntar.** Uma obra aparece uma vez por contrato ou
> projeto aprovado; a junção crua multiplicaria linhas de filme.

**O que estes arquivos NÃO têm: valor.** Só o número do instrumento. Dá para derivar
"recebeu" (binária) e "quantos contratos" (contagem), não o orçamento.

**Por que não há risco de vazamento.** Fomento é **aprovado antes de a obra existir** —
é informação genuinamente anterior à estreia, diferente da renda e do número de salas.

---

## 3. Banco Central — IPCA, série 433 do SGS (complementar)

**URL.** `https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json`

**Formato.** JSON: lista de `{"data": "dd/mm/aaaa", "valor": "x.yz"}`. 559 pontos,
01/1980 a 07/2026, ~20 KB.

**Uso.** Deflacionar a renda de bilheteria. A ANCINE publica em reais **correntes da
época**: comparar 1995 com 2024 sem deflacionar é comparar moedas diferentes.
`build_dataset.py` encadeia a variação mensal num índice, tira a média anual e produz
`renda_deflacionada_2024`.

O deflator **não é atributo do modelo** — serve para tornar a renda legível na EDA.
(E a renda em si é vazamento; ver `02-decisoes-e-escopo.md`, D5.)

> ⚠️ Passar `dataInicial`/`dataFinal` nesta série devolveu erro nos testes. Baixe a
> série inteira e filtre em memória.

---

## 4. IBGE — População residente estimada (complementar)

**URL.**
```
https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/{periodos}/
variaveis/9324?localidades=N1[all]
```

**Cobertura.** Série anual, Brasil. **Devolveu 20 dos 30 anos pedidos (2001–2024)** —
o IBGE não publica estimativa para 1995–2000 nem para anos de Censo. Daí os 23,3% de
ausência em `populacao_br`, que é falta de **junção**, não do dado original.

**Uso.** Contexto de mercado: mostrar que o crescimento do público do cinema nacional
não é só crescimento populacional.

> ⚠️ `apisidra.ibge.gov.br` **não resolve DNS** neste ambiente. Use `servicodados`.

---

## Fontes testadas e descartadas

Registrar o que não deu certo evita que a próxima pessoa gaste a mesma tarde. Todas
testadas em 10/09/2026; o registro executável está em `fontes.DESCARTADAS`.

| fonte | o que traria | por que foi descartada |
|---|---|---|
| **Wikidata (SPARQL)** | **duração** do filme (P2047), que a ANCINE não publica; licença CC0 | `query.wikidata.org` não resolve DNS neste ambiente. Vale reabrir em outra rede — melhoria M6 |
| **API do dados.gov.br** | catálogo de conjuntos | passou a exigir chave: **HTTP 401** |
| **`apisidra.ibge.gov.br`** | mesmos dados do IBGE | não resolve DNS. Substituída por `servicodados` |
| **Listagem de pastas do OCA** | descobrir outros CSVs | `/oca/cinema` e `/oca/cinema/arquivos.csv` devolvem **HTTP 401** (permissão do Plone). URLs têm de ser descobertas uma a uma |
| **TMDB** | duração, orçamento, elenco | exige cadastro e chave. O projeto decidiu não depender de credencial (D1). Extensão opcional para a Entrega 2 |

### Um esclarecimento sobre `duração`

A proposta inicial do trabalho listava **duração** como atributo. Ela **não existe** na
listagem da ANCINE, e a fonte aberta que a traria não é alcançável daqui. O trabalho
segue sem ela, e isso está dito no relatório em vez de silenciado.

## Como citar

> ANCINE. *Listagem dos Filmes Brasileiros Lançados Comercialmente em Salas de Exibição
> 1995 a 2024*. Observatório Brasileiro do Cinema e do Audiovisual. Acesso em
> 10 set. 2026.
>
> BANCO CENTRAL DO BRASIL. *IPCA — variação percentual mensal*. Série 433, Sistema
> Gerenciador de Séries Temporais. Acesso em 10 set. 2026.
>
> IBGE. *População residente estimada*. Agregado 6579, variável 9324, API de agregados
> v3. Acesso em 10 set. 2026.
