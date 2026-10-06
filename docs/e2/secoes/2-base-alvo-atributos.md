# 2 · Base, alvo e atributos da E2

> Dona: Ana Raquel · Orçamento: 0,75 página

A base é a mesma da Entrega 1 — 2.626 longas brasileiros lançados em sala entre 1995 e
2024, montados por `src/build_dataset.py` a partir dos dados abertos da ANCINE, do IBGE e
do Banco Central. Esse arquivo **não foi alterado**: ele é o entregável congelado da E1, e
tudo o que a E2 precisa a mais vive no pacote `src/e2/`.

## 2.1 O alvo mudou, e a E1 é quem pediu

> **sucesso = público acima do percentil 75 dos filmes brasileiros do ano anterior.**

A auditoria da definição de sucesso mediu três defeitos no alvo da E1, que era a mediana
global: o limiar global embute a inflação e o crescimento do parque de salas em trinta anos;
a mediana *do próprio ano* só é conhecida depois que todos os filmes do ano estrearam, e
portanto olha para o futuro; e a mediana cai **dentro** da população de circuito limitado,
separando filmes que o mercado não distingue. O P75 do ano anterior é conhecido antes da
estreia e cai perto da fronteira entre as duas populações de público.

| | valor |
|---|---|
| filmes com alvo definido | **2.590** |
| filmes sem alvo | 36 — 22 sem público informado e 14 de 1995, sem ano anterior |
| prevalência de `sucesso` | **25,3%**, razão de 1 para 3 |
| prevalência por década | 26,7% · 25,2% · 23,0% · 29,1% |

A prevalência estável entre décadas é consequência da construção: o limiar acompanha o ano,
então a definição não fica mais fácil nem mais difícil com o tempo.

**Isso muda uma hipótese da E1, e é honesto dizer.** A H10 concluiu "não balancear", mas foi
medida com o alvo na mediana, que é 50/50 por construção. Com o P75 a classe positiva é 1
para 3 de verdade, e o balanceamento volta a ser pergunta legítima — consequência de ter
adotado a recomendação, não contradição.

## 2.2 Três atributos novos: o histórico de sucesso

Para cada filme, `hist_diretor`, `hist_distribuidora` e `hist_produtora` são o `log10` da
mediana do público dos filmes da mesma entidade lançados em **anos estritamente
anteriores**, e `NaN` quando não há nenhum. Mediana e log porque o público é lei de
potência, com Gini de 0,92: a média de três filmes de um diretor seria praticamente o maior
deles. Eles carregam o sinal das colunas de identidade que ficaram fora, sem o custo de
dimensão que 1.738 categorias de `direcao` imporiam ao kNN.

## 2.3 Atributos: 18, e por que não mais

| grupo | colunas | n |
|---|---|---|
| numéricas | `ano`, `filmes_diretor_antes`, `filmes_distribuidora_antes`, `filmes_produtora_antes`, `coproducao`, `recebeu_fsa`, `recebeu_incentivo`, `contratos_fsa`, `projetos_incentivo` | 9 |
| numéricas de histórico | `hist_diretor`, `hist_distribuidora`, `hist_produtora` | 3 |
| nominais | `genero`, `uf_maj`, `distribuidora`, `origem_do_fomento` | 4 |
| ordinais | `experiencia_da_direcao`, `porte_da_distribuidora` | 2 |

Cada exclusão é uma decisão da E1 aplicada, não uma escolha nova desta entrega:

| fora | motivo | origem |
|---|---|---|
| `publico`, `renda_*`, `max_salas`, `mediana_publico_do_ano`, `filmes_no_ano` | vazamento: só se conhecem depois da estreia | `build_dataset.COLUNAS_PROIBIDAS` |
| `cpb`, `titulo` | identificador | idem |
| `n_ufs` | moda em 97,1% dos filmes, efeito medido de 0,000 | H8 / S6 |
| `uf_bruto`, `uf2_bruto` | malformadas; `uf_maj` as substitui | H6 / P7 |
| `direcao`, `produtora_maj`, `produtora_min` | 1.738 / 1.502 / 714 categorias; o sinal entra pelos `hist_*` | P5 |
| `decada`, `deflator`, `populacao_br` | função do `ano`; `populacao_br` tem 23% de falha de junção | P8 |
| `estreia_do_diretor` | redundante com `experiencia_da_direcao` | — |

Um `assert` em `e2/base.py` derruba a execução se qualquer coluna de
`build_dataset.COLUNAS_PROIBIDAS` aparecer entre os atributos. A garantia de não vazamento
não depende de alguém lembrar.

> Números desta seção: `reports/e2/base_descricao.json` e `reports/e2/base_ausencia.csv`,
> gerados por `python src/e2/base.py`.
