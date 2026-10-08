# Resumo

> Dona: a confirmar · Orçamento: meia página

Este trabalho avalia sistematicamente o efeito do pré-processamento sobre o desempenho de um
classificador k-Nearest Neighbors na previsão de sucesso de bilheteria do cinema brasileiro.
Partindo da base de 2.626 filmes analisada na Entrega 1, construímos um pipeline de cinco etapas e
avaliamos as 144 combinações possíveis das opções escolhidas, sempre com o mesmo modelo, sete
vizinhos, e a mesma partição em cinco folds.

Consideramos sucesso o público acima do percentil 75 dos filmes do ano anterior, limiar conhecido
antes da estreia. Restam 2.590 filmes, dos quais 25,3% são sucesso.

As 144 combinações executaram sem falha. Com o modelo fixo, a escolha do pré-processamento move a
AUC em 0,122, de 0,731 a 0,853. Três resultados sustentam a discussão. A normalização é a única
etapa que decide o desempenho, com 68 vitórias e nenhuma derrota em 108 comparações pareadas. A
aplicação de PCA sobre uma matriz não escalada reduz o espaço a dois componentes e custa 0,065 de
AUC. E o balanceamento não altera a AUC, mas eleva a revocação em 0,19 em todos os contextos, ao
custo de 0,15 de precisão.

Adotamos a regra de empate exigida pelo enunciado, segundo a qual diferença menor que a
variabilidade entre folds não sustenta conclusão. Por ela, 104 das outras 143 combinações empatam
com a configuração de referência. A validação temporal qualifica esse resultado: a configuração sem
nenhuma transformação opcional cai de 0,827 para 0,588 ao prever anos futuros, enquanto as
combinações com padronização e encoding pelo alvo permanecem acima de 0,79.
