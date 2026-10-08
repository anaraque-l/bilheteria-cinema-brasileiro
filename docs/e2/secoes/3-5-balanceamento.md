# 3.5 · Técnicas — balanceamento

> Dona: Laura · Orçamento: parte das 2,0 páginas da §3

Com 25,3% de sucessos há um para cada três fracassos. A E1 decidiu não balancear com o alvo na
mediana, meio a meio; com o novo alvo a classe de sucesso é minoritária. O kNN prevê sucesso quando
pelo menos quatro dos sete vizinhos são sucesso, e não tem peso por classe: a única forma de mudar a
votação é mudar a proporção de sucessos no treino.

| opção | o que faz | vantagem e custo |
|---|---|---|
| sem balanceamento | mantém a base | referência |
| subamostragem | remove fracassos ao acaso até igualar as classes | equilibra o voto, mas descarta cerca de 1.020 dos 2.070 filmes de cada treino, e o kNN depende de densidade |
| SMOTE | cria sucessos entre dois sucessos parecidos, entre os cinco mais próximos | não descarta nada, mas no espaço do one-hot cria filmes com metade de uma distribuidora e metade de outra |

O balanceamento acontece só no treino. Duplicar sucessos ao acaso ficou fora porque um filme
copiado pode ocupar vários dos sete vizinhos. A hipótese, registrada antes da grade, é que
balancear aumente a revocação e o F1, diminua a precisão e a acurácia e quase não mexa na AUC, que
não depende de ponto de corte.
