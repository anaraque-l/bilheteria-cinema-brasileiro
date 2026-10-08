# 5.4 · Custo

> Dona: Ana Laura · Orçamento: parte das 4,0 páginas da §5

A grade inteira levou 3,9 minutos de ajuste e predição somados, com mediana de 0,92 segundo por
combinação e máximo de 3,99 segundos.

| etapa | opção mais barata | opção mais cara |
|---|---|---|
| ausentes | mediana e moda, 1,54 s | indicadora, 1,69 s |
| encoding | pelo alvo, 1,02 s | one-hot, 2,21 s |
| normalização | sem normalização, 1,33 s | padronização, 1,74 s |
| redução | sem redução, 0,76 s | seleção de dez colunas, 2,60 s |
| balanceamento | subamostragem, 1,56 s | SMOTE, 1,69 s |

Três leituras. A normalização, que domina o resultado, é praticamente de graça: 0,42 segundo
separa a mais barata da mais cara, e as três escalas custam o mesmo entre si, com diferença de
0,07 segundo. A etapa de maior efeito é a de menor custo relativo da grade.

O custo se concentra em duas escolhas, o one-hot e a seleção por informação mútua, e as dez
combinações mais caras são todas interseção das duas, todas com imputação por indicadora. A mais
cara leva 3,99 segundos, mais de quatro vezes a mediana.

A terceira leitura é a interessante. A correlação de Spearman entre o tempo total e o número de
colunas que chegam ao classificador é de −0,144, fraca e não significativa (p = 0,09): a dimensão
final não prediz o tempo, o que parece absurdo e não é. As dez mais caras entregam exatamente dez colunas
ao kNN, porque todas usam a seleção; o custo não está em medir distância em muitas dimensões, está
em estimar informação mútua entre 84 colunas e o alvo, cinco vezes, uma por fold, antes de o
classificador existir. Nas combinações com seleção o gargalo é o ajuste do pré-processamento, não a
predição, e é por isso que a dimensão final não prediz o tempo.

A consequência de projeto é que a seleção, que custa mais que o triplo de não reduzir e não ganha
em nenhum contexto, só se paga quando o objetivo é um modelo final mais enxuto: compra-se uma
matriz cinco vezes menor com um ajuste mais caro, pago uma única vez.
