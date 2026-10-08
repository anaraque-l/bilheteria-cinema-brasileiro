# 3.3 · Técnicas — normalização

> Dona: Ana Laura · Orçamento: parte das 2,0 páginas da §3

A distância euclidiana soma as diferenças de todas as colunas sem distinguir o que cada uma mede,
e nesta base as escalas são incomparáveis: o ano vai de 1996 a 2024, a contagem de filmes
anteriores da distribuidora vai de zero a 179 com mediana 10, os indicadores de fomento valem
zero ou um, e os históricos, em logaritmo, ficam entre zero e cerca de sete. Sem correção, as duas
colunas de maior amplitude decidem sozinhas quem é vizinho de quem.

A etapa age na matriz inteira, depois do encoding, porque é nela que o kNN mede distância; escalar
só as numéricas esconderia a interação com o encoding que a §5.3 discute.

| opção | o que faz | característica dos dados que a motiva |
|---|---|---|
| sem normalização | preserva as escalas cruas; compõe o baseline | testa se as escalas cruas já servem |
| padronização | centra em zero e divide pelo desvio-padrão | é o tratamento direto do problema de amplitude acima |
| escala por intervalo | comprime cada coluna para zero a um | as binárias do one-hot já vivem nesse intervalo e ficam intactas; o custo é depender do máximo, e numa coluna de cauda longa a maioria dos filmes fica perto de zero |
| escala robusta | centra na mediana e divide pelo intervalo interquartil | as contagens de filmes anteriores têm assimetria de 2,0 a 3,8, e mediana e intervalo interquartil são as medidas adequadas a essa cauda |

A hipótese não é a de que normalizar ajuda, que seria trivial, mas a de que a melhor normalização
depende do encoding. O argumento é aritmético: numa coluna binária em que um por cento dos filmes
vale um, o desvio-padrão é cerca de 0,0995, e dividir por ele transforma o valor um em
aproximadamente 9,9, de modo que uma categoria com um punhado de filmes pesaria dez vezes mais na
distância que uma numérica. Daí a previsão de que a padronização renderia menos no espaço dos
indicadores e que a escala por intervalo seria a mais segura ali; a §5.3 mostra que o efeito medido
tem outra forma. Uma transformação de potência antes da escala ficou fora para manter o espaço em
144 combinações, embora a S5 da E1 tenha medido com ela 0,024 de ganho no modelo linear.
