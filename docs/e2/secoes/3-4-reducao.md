# 3.4 · Técnicas — redução de dimensionalidade

> Dona: Ana Laura · Orçamento: parte das 2,0 páginas da §3

Com o one-hot chegam ao kNN de 76 a 84 colunas, boa parte quase vazia, e em dimensão alta o
vizinho mais próximo deixa de ser muito mais próximo que o mais distante. A H13 da E1 concluiu que
não valia aplicar PCA, mas foi medida com floresta aleatória, indiferente a escala e dimensão.

| opção | estratégia | característica dos dados que a motiva |
|---|---|---|
| sem redução | preserva todas as colunas; compõe o baseline | é a H13 da E1, agora num modelo sensível a dimensão |
| PCA retendo 95% da variância | troca as colunas por combinações delas | as colunas do one-hot são em boa parte esparsas, o caso em que a concentração de distâncias pesa |
| dez melhores por informação mútua | mantém colunas originais e descarta o resto | a E1 achou atributos redundantes, e na distância um atributo ruidoso pesa tanto quanto um útil |

Informação mútua em vez de teste F porque a relação que interessa ao kNN não precisa ser linear. O
orçamento de dez colunas é absoluto porque ao seletor chegam de 18 a 84 colunas, conforme o
encoding, e só um número fixo mantém "as dez melhores" com o mesmo sentido. A etapa vem antes do
balanceamento para ser ajustada só com filmes reais. A hipótese é que a redução só seja inofensiva
com normalização: sem ela, a variância é quase toda de duas colunas, e o corte de 95% sairia em um
ou dois componentes.
