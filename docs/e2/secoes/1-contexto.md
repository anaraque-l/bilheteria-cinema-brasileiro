# 1 · Contexto: o problema, o que a E1 deixou, o alvo P75

> Dona: Laura · Orçamento: 0,75 página

**O problema.** Queremos prever se um filme brasileiro vai ter público acima do comum usando
apenas informações disponíveis antes da estreia, com a listagem da ANCINE de 1995 a 2024 e os
dados de fomento público de cada filme. A pergunta é a da Entrega 1: o dinheiro público está indo
para filmes que encontram plateia?

**O que a E1 deixou.** Medimos três atalhos que inflam o resultado sem ensinar nada ao modelo: a
renda como atributo somava 0,161 à AUC, o número máximo de salas 0,108, e a divisão aleatória em
vez de separar por ano 0,087. A auditoria do alvo mostrou ainda que o público forma duas
populações, a de circuito limitado e a de lançamento comercial, com fronteira perto do percentil
69, e que a mediana cai dentro da primeira.

**O alvo P75.** O percentil 75 do ano anterior não embute o ano, já está publicado quando o filme
estreia e cai perto da fronteira entre as duas populações. Com ele, 2.590 filmes têm alvo e 25,3%
são sucesso; os cortes em P50 e P90 entram na §6.

**O que muda.** O modelo é fixo, um kNN de sete vizinhos, e comparamos 144 formas de preparar os
dados para ele. Duas conclusões da E1 voltam à prova: não balancear, medida num alvo meio a meio,
e não aplicar PCA, medida com floresta aleatória, que não sente escala nem dimensão. O kNN sente
as duas.
