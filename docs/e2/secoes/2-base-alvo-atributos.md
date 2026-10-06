# 2 · Base, alvo e atributos da E2

> Dona: Ana Raquel · Orçamento: 0,75 página

A base é a mesma da Entrega 1: 2.626 longas brasileiros lançados em sala entre 1995 e 2024,
montados por `src/build_dataset.py` a partir dos dados abertos da ANCINE, do IBGE e do Banco
Central. Esse arquivo não foi alterado nesta entrega, porque é o entregável congelado da E1.
Tudo o que a E2 acrescenta vive no pacote `src/e2/`.

## 2.1 A definição de sucesso

Nesta entrega, sucesso é público acima do percentil 75 dos filmes brasileiros do ano
anterior.

O alvo da E1 era a mediana global dos trinta anos. A auditoria da definição de sucesso
mediu três problemas nessa escolha. O limiar global embute a inflação e o crescimento do
parque de salas, de modo que um filme de 1997 e um de 2023 são avaliados pela mesma régua.
A mediana do próprio ano só é conhecida depois que todos os filmes do ano estrearam, o que a
torna indisponível para prever antes da estreia. E a mediana cai dentro da população de
filmes de circuito limitado, separando filmes que o mercado não distingue entre si. O
percentil 75 do ano anterior é conhecido antes de qualquer estreia do ano e cai perto da
fronteira entre as duas populações de público.

| | valor |
|---|---|
| filmes com alvo definido | 2.590 |
| filmes sem alvo | 36: 22 sem público informado e 14 de 1995, que não têm ano anterior |
| prevalência de sucesso | 25,3%, razão de 1 para 3 |
| prevalência por década | 26,7% · 25,2% · 23,0% · 29,1% |

A prevalência se mantém estável entre as décadas porque o limiar acompanha o ano. A
definição não fica mais fácil nem mais difícil com o tempo.

A adoção desse alvo revê uma hipótese da E1. A H10 concluiu que não se deveria balancear,
mas foi medida com o alvo na mediana, que é 50/50 por construção. Com o percentil 75 a
classe positiva passa a ser 1 para 3, e o balanceamento volta a ser aplicável.

## 2.2 Os atributos de histórico de sucesso

Para cada filme, `hist_diretor`, `hist_distribuidora` e `hist_produtora` são o `log10` da
mediana do público dos filmes da mesma entidade lançados em anos estritamente anteriores, e
`NaN` quando não há nenhum. A escolha da mediana e do logaritmo vem da distribuição do
público, que é lei de potência com Gini de 0,92: a média de três filmes de um diretor ficaria
próxima do maior deles. Esses três atributos carregam o sinal das colunas de identidade que
ficaram fora, sem o custo de dimensão que as 1.738 categorias de `direcao` imporiam ao kNN.

## 2.3 Os 18 atributos

| grupo | colunas | n |
|---|---|---|
| numéricas | `ano`, `filmes_diretor_antes`, `filmes_distribuidora_antes`, `filmes_produtora_antes`, `coproducao`, `recebeu_fsa`, `recebeu_incentivo`, `contratos_fsa`, `projetos_incentivo` | 9 |
| numéricas de histórico | `hist_diretor`, `hist_distribuidora`, `hist_produtora` | 3 |
| nominais | `genero`, `uf_maj`, `distribuidora`, `origem_do_fomento` | 4 |
| ordinais | `experiencia_da_direcao`, `porte_da_distribuidora` | 2 |

Cada exclusão abaixo aplica uma decisão já tomada na E1:

| fora | motivo | origem |
|---|---|---|
| `publico`, `renda_*`, `max_salas`, `mediana_publico_do_ano`, `filmes_no_ano` | vazamento: só se conhecem depois da estreia | `build_dataset.COLUNAS_PROIBIDAS` |
| `cpb`, `titulo` | identificador | idem |
| `n_ufs` | moda em 97,1% dos filmes, efeito medido de 0,000 | H8 e S6 |
| `uf_bruto`, `uf2_bruto` | malformadas, substituídas por `uf_maj` | H6 e P7 |
| `direcao`, `produtora_maj`, `produtora_min` | 1.738, 1.502 e 714 categorias; o sinal entra pelos históricos | P5 |
| `decada`, `deflator`, `populacao_br` | função do `ano`; `populacao_br` tem 23% de falha de junção | P8 |
| `estreia_do_diretor` | redundante com `experiencia_da_direcao` | — |

Um `assert` em `e2/base.py` interrompe a execução se qualquer coluna de
`build_dataset.COLUNAS_PROIBIDAS` aparecer entre os atributos, de modo que a verificação não
depende de alguém lembrar de fazê-la.

Os números desta seção estão em `reports/e2/base_descricao.json` e
`reports/e2/base_ausencia.csv`, gerados por `python src/e2/base.py`.
