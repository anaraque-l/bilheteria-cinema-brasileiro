# 2 · Base, alvo e atributos da E2

> Dona: Ana Raquel · Orçamento: 0,75 página

A base é a mesma da Entrega 1: 2.626 longas brasileiros lançados em sala entre 1995 e 2024, a
partir dos dados abertos da ANCINE, do IBGE e do Banco Central, sem alteração no módulo que a
monta.

**A definição de sucesso.** Público acima do percentil 75 dos filmes brasileiros do ano anterior.
O alvo antigo, a mediana global dos trinta anos, embutia o ano: os lançamentos cresceram catorze
vezes entre 1995 e 2024 e o público mediano por filme caiu quinze vezes. A mediana do próprio ano
só se conhece depois de todas as estreias. Ficam sem alvo 36 filmes, 22 sem público informado e 14
de 1995, que não têm ano anterior. A prevalência de sucesso fica entre 23,0% e 29,1% nas quatro
décadas, porque o limiar acompanha o ano.

**Os atributos de histórico.** Três atributos novos medem a reputação da direção, da distribuidora
e da produtora: o logaritmo da mediana do público dos filmes da mesma entidade em anos estritamente
anteriores, ausente quando não há nenhum. Mediana e logaritmo porque o público é lei de potência,
com Gini de 0,92. Eles carregam o sinal das colunas de identidade sem o custo de dimensão que as
1.738 categorias de direção imporiam ao kNN.

**Os dezoito atributos.** Nove numéricas, três de histórico, quatro nominais e duas ordinais; o
anexo F traz a lista e o motivo de cada exclusão, todas decisões já tomadas na E1. Uma verificação
no código interrompe a execução se qualquer coluna conhecida só depois da estreia aparecer entre os
atributos.
