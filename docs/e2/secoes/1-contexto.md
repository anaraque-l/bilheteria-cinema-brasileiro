# 1 · Contexto: o problema, o que a E1 deixou, o alvo P75

> Dona: Laura · Orçamento: 0,75 página

**O problema.** Queremos prever se um filme brasileiro vai ter público acima do comum usando
apenas informações disponíveis antes da estreia. A base é a listagem oficial da ANCINE de 1995 a
2024, com os dados de fomento público ligados a cada filme. A decisão de financiar um filme
acontece antes de ele existir, e por isso a pergunta que motiva o trabalho continua a mesma da
Entrega 1: o dinheiro público está indo para filmes que encontram plateia?

**O que a E1 deixou.** Medimos três atalhos que inflam o resultado sem ensinar nada ao modelo:
usar a renda como atributo somava 0,161 à AUC, usar o número máximo de salas somava 0,108, e
validar com divisão aleatória em vez de separar por ano somava 0,087. Somados a um alvo que
dependia do ano de lançamento, levavam a AUC de 0,725 a 0,995. Auditamos também o alvo: o público
dos filmes brasileiros não forma um grupo único, e sim dois, os de circuito limitado e os de
lançamento comercial, com fronteira perto do percentil 69. A mediana cai dentro do primeiro
grupo, e por isso separava filmes pequenos bons de filmes pequenos ruins.

**Por que o percentil 75 do ano anterior.** Ele resolve os três problemas do alvo anterior: não
embute o ano, já está publicado quando o filme estreia, e cai perto da fronteira entre as duas
populações. Com ele, 2.590 filmes têm alvo e 25,3% são sucesso. Os cortes em P50 e P90 entram
como teste de robustez na §6, como a E1 recomendou.

**O que muda nesta entrega.** O modelo é fixo, um kNN de sete vizinhos, e comparamos 144 formas
de preparar os dados para ele. Duas conclusões da E1 entram em revisão por consequência direta
disso. A primeira recomendava não balancear, mas foi medida num alvo que era meio a meio por
construção; com um sucesso para cada três fracassos, o balanceamento volta a ser aplicável. A
segunda recomendava não aplicar PCA, mas foi medida com floresta aleatória, que não é afetada
pela escala nem pelo número de atributos. O kNN é afetado pelos dois, e é essa diferença que a
grade mede.
