# Guia do projeto

Por onde começar, e em que ordem ler.

## Em uma frase

Prever se um filme brasileiro alcançará público acima da mediana, usando **só** o que
se sabe antes da estreia — e mostrar, com número, quanto custa fazer isso honestamente.

## Ordem de leitura

| # | documento | quando ler |
|---|---|---|
| 1 | [`../README.md`](../README.md) | visão geral e achado principal |
| 2 | [`01-fontes-de-dados.md`](01-fontes-de-dados.md) | antes de mexer em ingestão |
| 3 | [`02-decisoes-e-escopo.md`](02-decisoes-e-escopo.md) | antes de mexer em atributo ou alvo |
| 4 | o notebook em `notebooks/` | a análise em si |
| 5 | [`03-melhorias-e-tradeoffs.md`](03-melhorias-e-tradeoffs.md) | ao planejar a Entrega 2 |
| 6 | [`relatorio-entrega1.md`](relatorio-entrega1.md) | o documento que vai ser entregue |

## As etapas do pipeline

```
  fontes.py          registro: URL, licenca, cobertura, data de teste
       |
  ingestao.py        baixa o bruto -> data/raw/          (cache; nao transforma)
       |
  build_dataset.py   tipa, junta, define alvos -> data/processed/filmes.csv
       |             (NAO imputa, NAO normaliza, NAO codifica, NAO balanceia)
       |
       +---> notebook da entrega  descreve, visualiza, diagnostica
       |
       +---> sensibilidades.py   mede o peso de cada decisao
```

A separação entre `build_dataset.py` e `sensibilidades.py` é a espinha do projeto. O
primeiro produz o que é **entregue**; o segundo produz **evidência sobre o que ainda
não foi decidido**. Nenhuma transformação testada no segundo toca o primeiro.

## Por que `data/raw` é versionado

Órgão público republica arquivo sem avisar — a própria edição `2024r` da ANCINE é uma
retificação da `2024`. Versionar o bruto é o que garante que outra pessoa reproduza
**os mesmos números**, e não números parecidos, meses depois.

## O que a Entrega 1 é, e o que não é

| é | não é |
|---|---|
| descrever, visualizar, diagnosticar | corrigir, imputar, balancear |
| escrever e **medir** hipóteses | aplicar as hipóteses à base |
| escolher e justificar o alvo | escolher o melhor modelo |

Rodamos modelos em `sensibilidades.py`, mas eles são **instrumento de medida**. Nenhum
número de lá será reportado como desempenho do trabalho. Isso é a Entrega 2.

## O que ficou de fora, e por quê

- **Duração do filme.** A ANCINE não publica. Viria do Wikidata (licença CC0), mas o
  endpoint não é alcançável neste ambiente. Registrado como melhoria M6.
- **Orçamento e fomento recebido.** Existe em outro conjunto da ANCINE, com chave de
  junção diferente (CPB). É a melhoria de maior impacto potencial — ver M1.
- **Data exata de estreia.** Sem ela, não dá para separar as salas decididas na estreia
  das salas ganhas por bom desempenho. É a razão de `max_salas` ser tratado como
  vazamento provável, e não como atributo.

## Convenções de código

- **Português** em nomes, comentários e docstrings. Código sem acento em identificador
  (evita problema de encoding no Windows); texto de documentação **com** acento.
- **Comentário explica o porquê**, não o quê. Este repositório é material de estudo:
  comentário aqui justifica a escolha e ensina a interpretar o resultado.
- Toda URL mora em `src/fontes.py`. Nenhuma URL no notebook.
- Fonte testada e **descartada** também entra no registro, em `fontes.DESCARTADAS`, com
  o motivo — evita que a próxima pessoa gaste a mesma tarde.
- Sem dependência pesada nova: pandas, numpy, matplotlib, seaborn e scikit-learn. A
  ingestão usa só a biblioteca padrão.
- Todo gráfico do notebook vem seguido de interpretação, e o notebook é executado de
  ponta a ponta antes de ser commitado.

## Os três atalhos proibidos

Antes de mexer em qualquer lista de atributos ou no protocolo de avaliação:

| atalho | por quê | medido |
|---|---|---|
| usar `renda_corrente` / `renda_deflacionada_2024` | é público × preço do ingresso | ρ = 0,99; AUC vai a 0,993 |
| usar `max_salas` | é o máximo **atingido durante** a carreira, não na estreia | +0,108 de AUC |
| usar `sucesso_global` sem ressalva | a mediana global embute o ano: 86% nos anos 1990 contra 26% nos 2020 | −0,062 ao trocar |

E o *k-fold* aleatório é **+0,087 otimista** frente à partição temporal. O conjunto
honesto de atributos está em `sensibilidades.NUM_HONESTAS` e `CAT_HONESTAS`; para
acrescentar algo ali, prove antes que é conhecido antes da estreia.
