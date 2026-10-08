# 5.4 · Custo

> Dona: Ana Laura · Orçamento: parte das 4,0 páginas da §5

A grade inteira levou 3,9 minutos de ajuste e predição, com mediana de 0,92 segundo por combinação
e máximo de 3,99; o tempo de cada opção está no anexo G. A normalização, que decide o resultado, é
quase de graça: 0,42 segundo separa a opção mais barata da mais cara. O custo se concentra no
one-hot, 2,21 segundos em média contra 1,02 do encoding pelo alvo, e na seleção por informação
mútua, 2,60 contra 0,76 sem redução; as dez combinações mais caras são todas one-hot, seleção e
indicadora.

A correlação de Spearman entre o tempo e o número de colunas que chegam ao kNN é de −0,144, fraca e
não significativa (p = 0,09). As combinações mais caras entregam exatamente dez colunas, porque
usam a seleção: o custo não está em medir distância em muitas dimensões, está em estimar
informação mútua entre até 84 colunas e o alvo em cada fold. Nessas combinações o ajuste custa três
vezes a predição. A seleção, que custa mais que o triplo de não reduzir e não ganha em nenhum
contexto, só se paga quando o objetivo é um modelo final mais enxuto.
