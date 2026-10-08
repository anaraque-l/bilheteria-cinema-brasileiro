# 5.1 · Visão geral, baseline, melhores e piores

> Dona: Ana Laura · Orçamento: parte das 4,0 páginas da §5

As 144 combinações executaram sem nenhuma falha; a tabela completa está no anexo A.

| | combinação | AUC |
|---|---|---|
| melhor | mediana e moda, encoding pelo alvo, padronização, PCA e subamostragem | 0,853 ± 0,016 |
| baseline | sem nenhuma transformação opcional | 0,827 ± 0,014 |
| pior | indicadora, one-hot, sem normalização, PCA e subamostragem | 0,731 ± 0,015 |

Com o modelo fixo e os mesmos folds, o pré-processamento move a AUC em 0,122, mais do que a E1
ganhou trocando de modelo. Mas a regra de empate cobra o seu preço: o baseline ocupa a 61ª posição
e **104 das outras 143 combinações empatam com ele**; só dez o superam de forma que a variabilidade
entre folds sustente, e 21 empatam com a melhor. O que a grade autoriza afirmar não é qual pipeline
é o melhor, e sim quais opções nunca prejudicam e quais podem destruir o resultado.

![As 144 combinações em ordem de AUC, com o desvio entre folds; em azul as que empatam com a melhor](../../../reports/figuras/e2/fig-al-ranking.png)

As doze piores, da 133ª à 144ª, são exatamente as doze que aplicam PCA sem normalização, todas com
2,0 colunas chegando ao classificador: são os pontos depois do salto na figura. As melhores têm em
comum o encoding pelo alvo e alguma normalização.

A combinação do topo aplica PCA, e a §5.2 conclui que a redução não venceu em nenhum contexto. As
duas coisas convivem porque a posição no ranking vem da média e o veredito vem do pareado: a mesma
combinação sem o PCA fica em 0,848, dentro do desvio. Ocupar o primeiro lugar não é o mesmo que ter
chegado lá por causa de uma etapa.
