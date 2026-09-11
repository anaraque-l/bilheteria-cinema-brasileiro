# Prever bilheteria de filme brasileiro antes da estreia

**Entrega 1 — Análise Exploratória de Dados**
CIN0144 · Aprendizado de Máquina e Ciência de Dados · CIn/UFPE

> **Um filme brasileiro vai alcançar público acima da mediana do seu ano de
> lançamento — prevendo apenas com atributos conhecidos antes da estreia?**

Classificação binária sobre **2.626 filmes brasileiros** lançados comercialmente entre
1995 e 2024 — **35 atributos** a partir da listagem oficial da ANCINE, dos registros de
fomento público, do IPCA e do IBGE.

---

## O achado principal

Este trabalho começou com uma pergunta sobre cinema e terminou com uma lição sobre
definição de alvo.

A forma literal de construir o alvo — *sucesso = público acima da mediana da base* —
produz classes perfeitamente equilibradas (50,0% / 49,7%) e parece impecável. Só que a
mediana global embute o **ano**:

| década | % de "sucesso" com mediana **global** | com mediana **do ano** |
|---|---|---|
| 1990 | **85,6%** | 49,0% |
| 2000 | 75,7% | 49,5% |
| 2010 | 50,2% | 49,8% |
| 2020 | **26,3%** | 49,7% |

O mercado mudou: em 1995 lançaram-se 14 filmes brasileiros; nos anos 2010, mais de 180
por ano — em larga medida documentários de circuito limitado. O público **mediano** por
filme caiu mais de uma ordem de grandeza. Um corte pela mediana global classifica quase
todo filme antigo como sucesso e quase todo filme recente como fracasso.

**Um modelo treinado assim não aprende sobre cinema: aprende a ler o calendário.**

Somando os três atalhos disponíveis nesta base, a diferença é brutal:

| versão | AUC |
|---|---|
| caminho fácil — alvo global, com `renda` e `max_salas`, *k-fold* aleatório | **0,995** |
| versão honesta — alvo relativo ao ano, só atributos pré-estreia, partição temporal | **0,725** |

**0,27 de AUC** separa as duas, e nenhuma linha de código as distingue à primeira vista.

---

## Como este repositório está organizado

```
├── src/
│   ├── fontes.py              registro das fontes: URL, licenca, cobertura, data de teste
│   ├── ingestao.py            baixa o bruto para data/raw/ (com cache)
│   ├── build_dataset.py       tipagem, juncoes e definicao dos alvos
│   └── sensibilidades.py      mede o peso de cada decisao de pre-processamento
├── notebooks/
│   └── Entrega_1_...ipynb     ENTREGAVEL PRINCIPAL — executado, com saidas
├── docs/
│   ├── 00-guia-do-projeto.md  por onde comecar
│   ├── 01-fontes-de-dados.md  as tres fontes, e as que foram descartadas
│   ├── 02-decisoes-e-escopo.md decisoes D1..D9, com justificativa
│   ├── 03-melhorias-e-tradeoffs.md  melhorias, impacto medido, viabilidade
│   ├── dicionario-de-dados.csv gerado pelo notebook
│   └── relatorio-entrega1.md  DOCUMENTO DE ENTREGA
├── data/
│   ├── raw/                   bruto, versionado de proposito
│   └── processed/filmes.csv   base analitica (2.626 x 28)
└── reports/figuras/           as 12 figuras do relatorio, em PNG
```

## Rodando

Python 3.12. Nenhuma fonte exige cadastro, chave de API ou aceite de termos.

```bash
pip install -r requirements.txt
python src/ingestao.py        # baixa o bruto (cache: repetir nao vai a rede)
python src/build_dataset.py   # monta data/processed/filmes.csv
python src/sensibilidades.py  # roda as seis analises de sensibilidade
jupyter lab notebooks/
```

---

## As fontes

| fonte | órgão | uso | licença |
|---|---|---|---|
| Listagem dos Filmes Brasileiros Lançados 1995–2024 | ANCINE / OCA | base primária — 2.626 filmes, 13 campos | dado aberto federal |
| Obras com Investimento do FSA | ANCINE | fomento direto, junção por CPB | **CC-BY** |
| Obras com Fomento Indireto Aprovado | ANCINE | leis de incentivo, junção por CPB | **CC-BY** |
| IPCA, série 433 do SGS | Banco Central | deflacionar a renda para reais de 2024 | dado aberto federal |
| População residente estimada (agregado 6579) | IBGE | contexto de mercado | dado aberto federal |

Todas regidas pela Lei 12.527/2011 (LAI) e pelo Decreto 8.777/2016: uso livre, com
citação da fonte, sem restrição a uso acadêmico.

**Ressalva.** A listagem *1995–2025* mencionada em várias referências **não existe**.
Em 10/09/2026, a edição publicada mais recente é a `1995 a 2024r`; as URLs de 2025
devolvem HTTP 404. Trabalhamos com 1995–2024.

Fontes testadas e descartadas — e o motivo de cada uma — estão em `fontes.DESCARTADAS`.
Entre elas, o Wikidata, que traria a **duração** dos filmes (atributo que a ANCINE não
publica) mas cujo endpoint não é alcançável neste ambiente.

---

## O que a análise encontrou

**A bilheteria brasileira é uma distribuição de lei de potência.** Público mediano de
**2.806 espectadores** contra média de 148.399 — 53 vezes maior. Assimetria 10,0,
curtose 135,3, máximo 4.342 vezes a mediana. **1% dos filmes concentra 36% do público;
10% concentram 91%; a metade inferior responde por 0,28%.**

**Treze problemas diagnosticados**, dos quais quatro são estruturais: alvo que embute o
ano, vazamento por `renda`, vazamento provável por `max_salas`, e assimetria extrema.
Os demais vão de cardinalidade (467 distribuidoras, muitas com um único filme) a
ausência MNAR e a um campo de UF malformado (87 valores distintos para 27 UFs
possíveis).

**Duas hipóteses são de *não fazer*.** Não aplicar balanceamento, porque as classes já
estão em 50/50 por construção — SMOTE aqui seria cumprir tabela. E não remover a cauda
como *outlier*, porque num regime de lei de potência a cauda não é anomalia, é o
fenômeno.

---

## O que mede o quê

Cada hipótese de pré-processamento foi transformada em número por
[`src/sensibilidades.py`](src/sensibilidades.py). Protocolo fixo: floresta aleatória,
5-fold estratificado, todo o pré-processamento dentro dos folds.

| # | pergunta | resposta |
|---|---|---|
| S1 | quanto vale cada atributo posterior ao lançamento? | `max_salas` +0,108 · `renda` +0,161 |
| S2 | mediana global ou mediana do ano? | o alvo relativo custa −0,062 e elimina o atalho |
| S3 | partição aleatória ou temporal? | a aleatória é +0,087 otimista |
| S4 | como tratar 467 distribuidoras? | `min_frequency` 5–15: −0,009 de AUC, −380 colunas |
| S5 | `log1p` ajuda? | +0,024 na regressão logística, **0,000** na floresta |
| S6 | remover `n_ufs` (moda em 97,1%)? | 0,000 — indistinguível de zero |

> O modelo aqui é **instrumento de medida**, como um termômetro. Nenhum destes números
> é "o desempenho do nosso modelo": a modelagem é a Entrega 2. A base entregue
> permanece sem imputação, sem remoção de *outlier* e sem codificação, como o enunciado
> exige de uma entrega exploratória.

---

## Entregáveis

| item | onde |
|---|---|
| Notebook executado, com as visualizações | [`notebooks/`](notebooks/) |
| Relatório | [`docs/relatorio-entrega1.md`](docs/relatorio-entrega1.md) |
| Figuras em PNG | [`reports/figuras/`](reports/figuras/) |

---

## Licença

Código sob [licença MIT](LICENSE). Os dados são públicos e pertencem aos órgãos que os
publicam (ANCINE, IBGE, Banco Central), redistribuídos aqui sob as condições de dado
aberto federal, com citação da fonte — ver [`NOTICE-DADOS.md`](NOTICE-DADOS.md).
