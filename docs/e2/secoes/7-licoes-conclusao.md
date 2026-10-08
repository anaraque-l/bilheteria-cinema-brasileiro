# 7 · Lições, limitações e conclusão

> Dona: Laura · Orçamento: 0,75 página

**Uma etapa decide, e as outras quatro empatam.** Normalizar move a AUC em cerca de 0,04 e nunca
prejudicou em 108 comparações pareadas. Para um classificador que decide por distância é coerente:
a única etapa que mexe diretamente na métrica de distância é a de escala.

**O perigo está nas combinações incoerentes.** As piores configurações não usam técnica
desaconselhada: aplicam PCA, que é padrão, a uma matriz não escalada, e sobram dois componentes; nas
doze vezes em que isso ocorre, o PCA perde em média 0,065 contra não reduzir. É o argumento a favor
de examinar combinações em vez de ajustar uma etapa por vez.

**Reduzir não melhora, mas pode baratear.** A seleção empata com a matriz completa em 43 dos 48
contextos com dez colunas.

**Empate sob um protocolo não é equivalência.** Pela regra de empate quase nada do que um ranking
por média sugeriria sobrevive aos cinco folds, e a validação temporal mostrou o outro lado: seis
combinações que empatam com a melhor se separam em cerca de 0,06 no futuro, e o baseline cai de
0,827 para 0,588. Com padronização e encoding pelo alvo o modelo perde cerca de 0,05 ao prever o futuro, em vez de
0,24, porque deixa de escolher vizinhos pelo ano e pelas contagens acumuladas.

**Limitações.** A contaminação indireta dos históricos entre folds decorre da divisão aleatória e é
o que a validação temporal mede. Em documentário a revocação é de 0,118; entre as doze combinações
verificadas, só as de PCA sem normalização com subamostragem passam de 0,47, marcando mais filmes
como sucesso e com AUC de 0,64 nesse gênero, contra 0,69 da melhor. E os sete vizinhos, fixados pelo
enunciado, são parte da razão de a classe rara quase nunca ser prevista.

**O que faríamos a seguir.** Uma transformação de potência antes da escala; a grade sem o
agrupamento de categorias raras do one-hot, que isolaria o efeito que a §5.3 só pôde conjeturar; e
o número de vizinhos ajustado em cada fold, com limiar próprio por gênero.
