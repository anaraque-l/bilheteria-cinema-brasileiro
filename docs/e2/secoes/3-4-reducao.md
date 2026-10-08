# 3.4 · Técnicas — redução de dimensionalidade

> Dona: Ana Laura · Orçamento: parte das 2,0 páginas da §3

Com o encoding por indicadores a matriz chega a cerca de 84 colunas, boa parte quase vazia. Em
dimensão alta as distâncias se concentram: o vizinho mais próximo deixa de ser significativamente
mais próximo que o mais distante, e o voto dos sete perde o sentido que tem num espaço de poucas
dimensões. A H13 da E1 concluiu que não valia aplicar PCA, mas foi medida com floresta aleatória,
modelo indiferente a escala e a dimensão. O kNN não é, e é essa diferença que a etapa põe à prova.

| opção | estratégia | característica dos dados que a motiva |
|---|---|---|
| sem redução | preserva todas as colunas; compõe o baseline | é a H13 da E1, agora testada num modelo sensível a dimensão |
| PCA retendo 95% da variância | troca as colunas por combinações delas | as 84 colunas do one-hot são em boa parte esparsas, e é o caso em que a concentração de distâncias morde |
| seleção das dez melhores por informação mútua | mantém colunas originais e descarta o resto | a E1 achou redundância entre atributos, e na distância um atributo ruidoso pesa tanto quanto um útil |

As duas técnicas atacam o mesmo problema por lados opostos, e é essa oposição que torna a
comparação informativa: o PCA preserva a variância mas entrega eixos que não correspondem a
atributo nenhum, de modo que se perde a leitura de qual característica decidiu; a seleção preserva
essa leitura e descarta informação de forma irreversível. A informação mútua foi escolhida em vez
do teste F porque o kNN é não paramétrico, e a relação que lhe interessa não precisa ser linear. O
orçamento de dez colunas é absoluto, e não proporcional, porque ao seletor chegam cerca de vinte
colunas com o encoding pelo alvo e cerca de 84 com o de indicadores: só um número igual mantém a
frase "as dez melhores colunas" com o mesmo significado nos dois casos.

A etapa fica antes do balanceamento porque o PCA e a seleção precisam ser ajustados só com filmes
reais. A hipótese é que a redução só seja inofensiva na presença da normalização, e o caso crítico
é o PCA: sem correção de escala a variância é quase toda de duas colunas, de modo que o corte de
95% sairia em um ou dois componentes que carregam apenas elas.
