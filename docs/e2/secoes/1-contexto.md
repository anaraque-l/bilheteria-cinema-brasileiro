# 1 · Contexto: o problema, o que a E1 deixou, o alvo P75

> Dona: Laura · Orçamento: 0,75 página

<!-- Rascunho. Números da E1 saem de docs/relatorio-entrega1.md; os do alvo P75 conferir em base.py antes de fechar. -->

**O problema.** Prevemos, só com o que se sabe antes da estreia, se um filme brasileiro
vai ter público acima do que é comum no mercado. A base é a listagem oficial da ANCINE,
1995–2024, enriquecida com fomento público por CPB. A decisão de financiar um filme é
tomada antes de ele existir, e a pergunta que justifica o trabalho é a mesma da Entrega 1:
o dinheiro público está indo para filmes que encontram plateia?

**O que a Entrega 1 deixou.** Três atalhos medidos — renda como atributo (+0,161 de AUC),
máximo de salas (+0,108) e *k-fold* aleatório no lugar da partição temporal (+0,087) —, que
juntos com um alvo que embute o ano levam a AUC de 0,725 para 0,995 sem que o modelo
aprenda nada sobre cinema. E uma auditoria do próprio alvo: o público brasileiro não é uma
distribuição a ser partida ao meio, mas duas populações — circuito limitado e lançamento
comercial — com fronteira perto do percentil 69. A mediana cai dentro da primeira.

**Por que P75 do ano anterior.** É a recomendação M8 da E1, que resolve três problemas de
uma vez: o alvo global embutia o ano (P1); a mediana do próprio ano só é conhecida em 31 de
dezembro, depois da estreia (P15); e a mediana separava circuito limitado bom de circuito
limitado ruim (§2.9). O percentil do ano anterior é conhecido e publicado antes da estreia.
Com ele ficam 2.590 filmes com alvo e 25,3% de sucessos. P50 e P90 entram como robustez,
cumprindo a condição que a própria E1 impôs (§6).

**O que é diferente agora.** Duas hipóteses da E1 mudam de status, e não por contradição.
A H10, "não balancear", valia para um alvo 50/50 por construção; com P75 a razão é 1 : 3
de verdade, e o balanceamento entra na grade com "sem" como uma das opções. A H13, "não
aplicar PCA", foi medida com floresta, que ignora escala e dimensão; o kNN da E2 não ignora.
Nesta entrega o modelo fica fixo — kNN com k = 7 — e o que se compara são 144 maneiras de
preparar os dados para ele.
