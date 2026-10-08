# 3.4 · Técnicas — redução de dimensionalidade

> Dona: Ana Laura · Orçamento: parte das 2,0 páginas da §3

A etapa responde a uma fragilidade que a E1 identificou e decidiu não tratar. Com o encoding por
indicadores a matriz chega a cerca de 84 colunas, boa parte quase vazia, porque nasce de
categorias com pouquíssimos filmes. Em dimensão alta as distâncias se concentram: o vizinho mais
próximo deixa de ser significativamente mais próximo que o mais distante, e o voto dos sete perde
o sentido que tem num espaço de poucas dimensões. A H13 da E1 concluiu que não valia aplicar PCA,
mas foi medida com floresta aleatória, modelo indiferente a escala e a dimensão. O kNN não é, e é
essa diferença que a etapa põe à prova.

| opção | objeto | estratégia |
|---|---|---|
| sem | mantém a matriz | preserva todas as colunas; compõe o baseline |
| PCA | `PCA` retendo 95% da variância | troca as colunas por combinações delas |
| seleção | `SelectKBest` com informação mútua, dez colunas | mantém colunas originais e descarta o resto |

As duas técnicas atacam o mesmo problema por lados opostos, e é essa oposição que torna a
comparação informativa. O PCA preserva a variância do conjunto, mas entrega ao classificador
eixos que já não correspondem a nenhum atributo do mundo real, de modo que se perde a leitura de
qual característica do filme decidiu. A seleção preserva essa leitura e descarta informação de
forma irreversível. Reter 95% da variância é o corte usual e evita escolher um número de
componentes para cada uma das 144 combinações, que variam muito em largura de matriz.

A escolha da informação mútua, em vez do teste F, decorre da natureza do classificador: o kNN é
não paramétrico, e a relação que lhe interessa entre atributo e alvo não precisa ser linear nem
monótona. Usar um critério linear para selecionar colunas de um modelo que não supõe linearidade
seria incoerente. O orçamento de dez colunas é absoluto, e não proporcional, porque ao seletor
chegam cerca de vinte colunas com o encoding pelo alvo e cerca de 84 com o one-hot: apenas um
número igual nos dois casos mantém a frase "as dez melhores colunas" com o mesmo significado
para o kNN, o que é condição para isolar o efeito da etapa na §5.2.

A etapa fica depois da normalização e antes do balanceamento. Antes do balanceamento porque o
PCA e a seleção precisam ser ajustados apenas com filmes reais; se viessem depois, pontos
sintéticos criados pelo SMOTE ajudariam a definir os eixos e a escolha das colunas.

A hipótese desta etapa é que **a redução só seja inofensiva na presença da normalização**, e o
caso crítico é o PCA. O PCA persegue variância, e sem correção de escala a variância da matriz é
quase toda da contagem de filmes anteriores da distribuidora e do ano, que são as colunas de
maior amplitude. O corte de 95% sairia então em um ou dois componentes que carregam apenas essas
duas informações. A §5.3 confirma a hipótese e mostra o número exato de componentes.
