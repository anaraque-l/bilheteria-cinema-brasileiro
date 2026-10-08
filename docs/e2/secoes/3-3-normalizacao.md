# 3.3 · Técnicas — normalização

> Dona: Ana Laura · Orçamento: parte das 2,0 páginas da §3

A distância euclidiana soma as diferenças de todas as colunas sem distinguir o que cada uma mede,
e aqui as escalas são incomparáveis: o ano vai de 1996 a 2024, a contagem de filmes anteriores da
distribuidora de zero a 179 com mediana 10, os indicadores de fomento valem zero ou um. Sem
correção, as colunas de maior amplitude decidem quem é vizinho. A etapa age na matriz inteira,
depois do encoding, porque é nela que o kNN mede distância.

| opção | o que faz | característica dos dados que a motiva |
|---|---|---|
| sem normalização | preserva as escalas cruas; compõe o baseline | testa se as escalas cruas já servem |
| padronização | centra em zero e divide pelo desvio-padrão | é o tratamento direto do problema de amplitude |
| escala por intervalo | leva cada coluna a zero a um | as binárias ficam intactas; o custo é depender do máximo, e numa cauda longa a maioria dos filmes fica perto de zero |
| escala robusta | centra na mediana e divide pelo intervalo interquartil | as contagens de filmes anteriores têm assimetria de 2,0 a 3,8, e mediana e intervalo interquartil são as medidas dessa cauda |

A hipótese é que a melhor normalização dependa do encoding: numa binária em que 1% dos filmes vale
um, o desvio-padrão é cerca de 0,0995, e a padronização leva o valor um a cerca de 9,9. Previmos
que ela renderia menos no one-hot; a §5.3 mostra outra forma. Uma transformação de potência ficou
fora para manter o espaço em 144 combinações.
