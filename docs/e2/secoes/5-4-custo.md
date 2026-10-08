# 5.4 · Custo

> Dona: Ana Laura · Orçamento: parte das 4,0 páginas da §5

A grade inteira levou 3,9 minutos de ajuste e predição somados, com mediana de 0,92 segundo por
combinação e máximo de 3,99 segundos. A escala absoluta é modesta, mas a distribuição do tempo
entre as etapas contraria a expectativa com que começamos.

| etapa | opção mais barata | opção mais cara |
|---|---|---|
| ausentes | mediana e moda, 1,54 s | indicadora, 1,69 s |
| encoding | pelo alvo, 1,02 s | one-hot, 2,21 s |
| normalização | sem normalização, 1,33 s | padronização, 1,74 s |
| redução | sem redução, 0,76 s | seleção de dez colunas, 2,60 s |
| balanceamento | subamostragem, 1,56 s | SMOTE, 1,69 s |

Três leituras. A primeira é que a normalização, que domina o resultado, é praticamente de graça:
0,41 segundo separa a opção mais barata da mais cara, e as três técnicas custam o mesmo entre si,
com diferença de 0,07 segundo. A etapa de maior efeito é a de menor custo relativo da grade.

A segunda é que o custo se concentra em duas escolhas, o one-hot e a seleção por informação mútua,
e as dez combinações mais caras da grade são todas interseção das duas, todas com a imputação por
indicadora. A mais cara leva 3,99 segundos, mais de quatro vezes a mediana.

A terceira leitura é a interessante. A correlação de Spearman entre o tempo total e o número de
colunas que chegam ao classificador é negativa, de −0,144: combinações com mais colunas tendem a
ser mais rápidas, o que parece absurdo e não é. As dez mais caras entregam exatamente dez colunas
ao kNN, porque todas usam a seleção; o custo não está em o classificador medir distância em muitas
dimensões, está em estimar informação mútua entre 84 colunas e o alvo, cinco vezes, uma por fold,
antes de o classificador existir. Nesta grade o gargalo é o ajuste do pré-processamento, não a
predição do modelo, e é por isso que a dimensão final não prediz o tempo.

Isso tem consequência de projeto. A seleção custa 2,60 segundos em média, mais que o triplo de não
reduzir, e não ganha da ausência de redução em um único contexto, como a §5.2 mostrou. Ela só se
paga quando o objetivo é um modelo final mais enxuto, caso em que se compra uma matriz cinco vezes
menor com um ajuste mais caro, pago uma única vez.
