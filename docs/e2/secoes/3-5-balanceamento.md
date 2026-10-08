# 3.5 · Técnicas — balanceamento

> Dona: Laura · Orçamento: parte das 2,0 páginas da §3

Com 25,3% de sucessos há um para cada três fracassos. A E1 decidiu não balancear, mas com o alvo na
mediana, que divide os filmes ao meio; com o novo alvo a classe de sucesso é minoritária e o
balanceamento entrou na grade, com a opção de não balancear preservada para testar se a decisão da
E1 ainda vale.

O kNN prevê sucesso quando pelo menos quatro dos sete vizinhos são sucesso. Como a maioria dos
vizinhos costuma ser fracasso, esse limite raramente é atingido. Outros modelos permitem dar mais
peso à classe rara; o kNN não, e a única forma de mudar a votação é mudar a proporção de sucessos
no treino.

| opção | o que faz | vantagem e custo |
|---|---|---|
| sem balanceamento | mantém a base | serve de referência |
| subamostragem | remove fracassos ao acaso até igualar as classes | equilibra o voto, mas descarta cerca de 1.020 dos 2.070 filmes de cada treino, e o kNN depende de densidade de vizinhos |
| SMOTE | cria sucessos entre dois sucessos parecidos, usando os cinco mais próximos | não descarta nada, mas no espaço dos indicadores cria filmes impossíveis, com metade de uma distribuidora e metade de outra |

A biblioteca de reamostragem garante que o balanceamento aconteça apenas no treino: os filmes de
teste são avaliados como estão, sem remoção nem criação de exemplos.

Duplicar sucessos ao acaso ficou fora porque um mesmo filme copiado pode ocupar vários dos sete
vizinhos e decidir o voto sozinho; a versão do SMOTE para categóricas precisa das colunas
originais, e aqui o balanceamento vem depois do encoding. A hipótese, registrada antes de rodar a
grade, é que o balanceamento aumente a revocação e o F1, diminua a precisão e a acurácia, e quase
não mexa na AUC, que não depende de ponto de corte.
