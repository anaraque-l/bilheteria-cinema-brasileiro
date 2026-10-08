# 1 · Contexto: o problema, o que a E1 deixou, o alvo P75

> Dona: Laura · Orçamento: 0,75 página

**O problema.** Queremos prever se um filme brasileiro vai ter público acima do comum,
usando apenas informações disponíveis antes da estreia. A base é a listagem oficial da
ANCINE de 1995 a 2024, com dados de fomento público ligados a cada filme. A decisão de
financiar um filme acontece antes de ele existir. Por isso a pergunta que motiva o
trabalho continua a mesma da Entrega 1: o dinheiro público está indo para filmes que
encontram plateia?

**O que aprendemos na Entrega 1.** Medimos três atalhos que inflam o resultado sem ensinar
nada ao modelo. Usar a renda como atributo somava 0,161 à AUC. Usar o número máximo de
salas somava 0,108. Validar com k-fold aleatório em vez de separar por ano somava 0,087.
Junto com um alvo que dependia do ano de lançamento, esses atalhos levavam a AUC de 0,725
para 0,995. Também auditamos o próprio alvo. O público dos filmes brasileiros não forma um
grupo único: são dois, os filmes de circuito limitado e os de lançamento comercial, e a
fronteira entre eles fica perto do percentil 69. A mediana cai dentro do primeiro grupo, e
por isso separava filmes pequenos bons de filmes pequenos ruins.

**Por que o percentil 75 do ano anterior.** Foi a recomendação da auditoria da E1, e ela
resolve três problemas. O alvo global dependia do ano. A mediana do próprio ano só é
conhecida em dezembro, depois da estreia do filme. E a mediana separava os grupos no lugar
errado. O percentil do ano anterior já está publicado quando o filme estreia. Com ele,
2.590 filmes têm alvo e 25,3% deles são sucesso. Os cortes em P50 e P90 entram como teste
de robustez, como a E1 recomendou.

**O que muda nesta entrega.** Duas hipóteses da E1 precisam ser revistas. A primeira dizia
para não balancear as classes, mas valia para o alvo na mediana, que tem metade de
sucessos por definição. Com P75 há um sucesso para cada três fracassos, e o balanceamento
passa a fazer sentido. Mesmo assim, a opção sem balanceamento continua na grade. A segunda
dizia para não usar PCA, mas foi testada com floresta aleatória, que não é afetada pela
escala nem pelo número de atributos. O kNN é afetado pelos dois. Nesta entrega o modelo é
fixo, um kNN com 7 vizinhos, e comparamos 144 formas de preparar os dados para ele.
