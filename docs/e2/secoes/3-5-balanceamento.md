# 3.5 · Técnicas — balanceamento

> Dona: Laura · Orçamento: parte das 2,0 páginas da §3

**Por que balancear.** Com o alvo em P75 do ano anterior, 25,3% dos filmes são sucesso,
ou seja, um sucesso para cada três fracassos. Na Entrega 1 decidimos não balancear, mas
naquela época o alvo era a mediana, que divide os filmes ao meio. Com o novo alvo a classe
de sucesso passou a ser minoritária, e o balanceamento entrou na grade. A opção sem
balanceamento continua lá, para testar se a decisão da E1 ainda vale.

**Como o desbalanceamento afeta o kNN.** O kNN classifica um filme pelo voto dos 7 filmes
mais parecidos com ele no treino. Se pelo menos 4 forem sucesso, o filme é previsto como
sucesso. Como a maioria dos vizinhos costuma ser fracasso, esse limite raramente é
atingido. Outros modelos permitem dar mais peso à classe rara, mas o kNN não. A única
forma de mudar a votação é mudar a proporção de sucessos no treino.

**Onde a etapa fica.** O balanceamento é a última etapa antes do kNN, por dois motivos. O
PCA e a seleção de atributos são ajustados antes, só com filmes reais, sem a influência de
filmes criados artificialmente. E o SMOTE cria os filmes novos no mesmo espaço em que o
kNN vai medir distâncias. A biblioteca imbalanced-learn garante que o balanceamento só
aconteça no treino: os filmes de teste são avaliados como estão, sem remoção nem criação
de exemplos. É por isso que adicionamos essa dependência ao projeto.

| opção | o que faz | vantagem e custo |
|---|---|---|
| sem | mantém a base como está | serve de referência |
| subamostragem | sorteia e remove fracassos até as classes ficarem do mesmo tamanho | equilibra o voto, mas descarta cerca de 1.020 dos 2.070 filmes de cada treino; o kNN perde vizinhos e piora em regiões com poucos filmes |
| SMOTE | cria sucessos novos entre dois sucessos parecidos, usando os 5 mais próximos | não descarta nada, mas com one-hot cria filmes impossíveis, como "metade de uma distribuidora e metade de outra"; com atributos contínuos, os filmes criados são plausíveis |

**Técnicas que ficaram de fora.**
- Duplicar sucessos ao acaso: um mesmo filme copiado várias vezes pode ocupar vários dos 7
  vizinhos de um filme de teste e decidir o voto sozinho.
- SMOTENC, a versão do SMOTE para atributos categóricos: precisa das colunas originais,
  mas no nosso pipeline o balanceamento vem depois do encoding e da redução.
- ADASYN e Tomek: não foram vistos em sala e não mudariam a análise.

**Hipóteses.** Antes de rodar a grade, registramos o que esperávamos em
`docs/e2/hipoteses-balanceamento.md`. Em resumo: o balanceamento deve aumentar a revocação
e o F1 e diminuir a precisão e a acurácia; a AUC deve mudar pouco; o SMOTE deve render
mais com atributos contínuos; e sem normalização o SMOTE deve escolher vizinhos piores. A
§5.2 compara essas expectativas com os resultados.
