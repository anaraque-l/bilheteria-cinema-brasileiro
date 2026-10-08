# 3.3 · Técnicas — normalização

> Dona: Ana Laura · Orçamento: parte das 2,0 páginas da §3

A distância euclidiana soma as diferenças de todas as colunas sem distinguir o que cada uma
mede, e nesta base as escalas são incomparáveis: o ano vai de 1996 a 2024, a contagem de filmes
anteriores da distribuidora vai de zero a 179 com mediana 9,5, os indicadores de fomento valem
zero ou um, e os três históricos, porque estão em logaritmo, ficam entre zero e cerca de sete.
Sem correção de escala, as duas colunas de maior amplitude decidem sozinhas quem é vizinho de
quem, e as demais entram na conta como arredondamento.

A etapa age na matriz inteira, depois do encoding, e não apenas nas colunas originalmente
numéricas, porque é na matriz inteira que o kNN mede distância. Escalar só as numéricas deixaria
metade da distância fora do controle da etapa e esconderia a interação com o encoding, que a
§5.3 discute.

| opção | objeto | o que faz |
|---|---|---|
| sem | mantém a matriz | preserva as escalas cruas; compõe o baseline |
| padrão | `StandardScaler` | centra em zero e divide pelo desvio-padrão da coluna |
| por intervalo | `MinMaxScaler` | comprime cada coluna para o intervalo de zero a um |
| robusta | `RobustScaler` | centra na mediana e divide pelo intervalo interquartil |

A escala por intervalo é a candidata natural para o espaço criado pelo encoding por indicadores,
porque as colunas binárias já vivem entre zero e um e permanecem intactas; o custo é depender do
valor máximo, de modo que numa coluna de cauda longa a maioria dos filmes fica espremida perto
de zero. A escala robusta foi escolhida contra essa cauda, com mediana e intervalo interquartil,
medidas que a E1 apontou como adequadas aos históricos, cuja assimetria ficou entre 2,0 e 3,8.
Vale registrar um detalhe de implementação com consequência estatística: numa coluna binária de
categoria rara o intervalo interquartil é zero, e nesse caso o scikit-learn substitui o divisor
por um, o que deixa a coluna como está.

A hipótese desta etapa não é a de que normalizar ajuda, que seria trivial, mas a de que **a
melhor normalização depende do encoding**. O argumento é aritmético: numa coluna binária em que
um por cento dos filmes vale um, o desvio-padrão é de cerca de 0,0995, e dividir por ele
transforma o valor um em aproximadamente 9,9, de modo que uma categoria com um punhado de filmes
pesaria dez vezes mais na distância que uma numérica bem comportada. Daí a previsão de que a
padronização renderia menos no espaço do one-hot e que a escala por intervalo seria a mais segura
ali. A §5.3 mostra que o efeito medido tem outra forma, e explica qual.

Consideramos e deixamos fora uma transformação de potência antes da escala. A S5 da E1 mediu com
ela 0,024 de ganho no modelo linear, e a assimetria das contagens sugere que o kNN também se
beneficiaria. Ficou fora para manter o espaço nas 144 combinações que o enunciado delimita e
porque os três atributos de cauda mais longa já entram em logaritmo. A sugestão volta na §7 como
extensão.
