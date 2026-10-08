# 2 · Base, alvo e atributos da E2

> Dona: Ana Raquel · Orçamento: 0,75 página

A base é a mesma da Entrega 1: 2.626 longas brasileiros lançados em sala entre 1995 e 2024,
montados a partir dos dados abertos da ANCINE, do IBGE e do Banco Central. O módulo que a monta
não foi alterado, porque é o entregável congelado da E1.

**A definição de sucesso.** Público acima do percentil 75 dos filmes brasileiros do ano anterior.
A auditoria da E1 mediu três problemas no alvo antigo, que era a mediana global dos trinta anos.
Um limiar global embute o ano, porque o número de lançamentos cresceu catorze vezes entre 1995 e
2024 enquanto o público mediano por filme caiu quinze vezes, de modo que um filme de 1997 e um de
2023 seriam julgados pela mesma régua. A mediana do próprio ano só é conhecida depois que todos os
filmes do ano estrearam, o que a torna indisponível para prever antes da estreia. E a mediana cai
dentro da população de circuito limitado, separando filmes que o mercado não distingue.

| | valor |
|---|---|
| filmes com alvo definido | 2.590 |
| filmes sem alvo | 36, dos quais 22 sem público informado e 14 de 1995, que não têm ano anterior |
| prevalência de sucesso | 25,3%, razão de um para três |
| prevalência por década | 26,7% · 25,2% · 23,0% · 29,1% |

A prevalência é estável entre as décadas porque o limiar acompanha o ano, condição para que a
comparação entre pipelines não dependa do período.

**Os atributos de histórico.** Três atributos novos medem a reputação da direção, da distribuidora
e da produtora: o logaritmo da mediana do público dos filmes da mesma entidade lançados em anos
estritamente anteriores, com ausência quando não há nenhum. A mediana e o logaritmo vêm da
distribuição do público, que é lei de potência com Gini de 0,92, de modo que a média de três filmes
de um diretor ficaria próxima do maior deles. Esses três atributos carregam o sinal das colunas de
identidade que ficaram fora, sem o custo de dimensão que as 1.738 categorias de direção imporiam
ao kNN.

**Os dezoito atributos.** Nove numéricas, três de histórico, quatro nominais e duas ordinais; o
anexo A traz a lista e o motivo de cada exclusão, todas aplicando decisões já tomadas na E1. Saem
do conjunto as colunas que só se conhecem depois da estreia, os identificadores, as colunas
malformadas, as de alta cardinalidade cujo sinal entra pelos históricos e as que são função do
ano. Uma verificação no código interrompe a execução se qualquer coluna proibida aparecer entre os
atributos, de modo que a garantia não depende de alguém lembrar de conferir.
