# 3.5 · Técnicas — balanceamento

> Dona: Laura · Orçamento: parte das 2,0 páginas da §3

<!-- Rascunho. Números de prevalência conferir com base.carregar_xy; nada daqui depende da grade. -->

**Por que a etapa existe.** Com o alvo P75 do ano anterior, 25,3% dos filmes são sucesso,
uma razão de 1 : 3. A H10 da E1, "não balancear", valia para o alvo na mediana, que é 50/50
por construção. Adotada a M8, a classe positiva passa a ser minoritária de verdade e a
etapa se torna aplicável. Não é contradição, é consequência. A opção `sem` continua na
grade, de modo que a H10 é testada num alvo em que poderia falhar.

**Onde ela fica e por quê.** É a última etapa antes do kNN. Os *samplers* do
`imbalanced-learn` só agem no `fit` do `Pipeline`, então o fold de teste nunca é
reamostrado; é a razão de a dependência existir. Ficar depois da redução garante que PCA e
seleção de atributos sejam ajustados só com filmes reais, e ficar no fim faz o SMOTE
interpolar no mesmo espaço em que o kNN vai medir distância.

**Por que o balanceamento mexe no kNN.** O kNN não tem `class_weight`, e com k = 7 a
classe prevista é o voto de 7 vizinhos, de modo que a probabilidade só assume oito valores.
Num bairro típico há três fracassos para cada sucesso, e chegar a 4 votos de 7 é difícil.
Mudar a proporção do treino é o único jeito de mudar essa votação.

| opção | objeto | evidência e custo |
|---|---|---|
| `sem` | passagem direta | referência; é a H10 da E1 |
| `subamostragem` | `RandomUnderSampler` | iguala as classes. Num fold de treino de cerca de 2.070 filmes, descarta cerca de 1.020 fracassos, metade da base, e o kNN depende de densidade |
| `smote` | `SMOTE`, 5 vizinhos | não descarta dado, cria sucessos sintéticos interpolando entre sucessos vizinhos. Em espaço *one-hot* a interpolação gera dummies fracionárias, filmes "0,4 de uma distribuidora e 0,6 de outra" que não existem; em espaço do encoding pelo alvo ou de PCA, interpola valores contínuos |

**Considerados e descartados.**
- `RandomOverSampler` duplica sucessos; para o kNN, um sucesso copiado três vezes pode
  ocupar três dos 7 vizinhos de um filme de teste e viciar o voto em cópias.
- `SMOTENC` trata categóricas, mas exige as colunas antes do encoding; a ordem do protocolo
  põe o balanceamento no fim, depois da redução, por um motivo mais forte.
- ADASYN e Tomek ficaram fora do que foi visto em sala, sem ganho de argumento que
  justifique o custo de explicá-los.

**Hipóteses registradas antes da grade**, em `docs/e2/hipoteses-balanceamento.md`: balancear
sobe revocação e F1 e derruba precisão e acurácia; a AUC muda pouco, provavelmente
empate; `smote` ganha de `subamostragem` em espaço contínuo; sem normalização o SMOTE
herda a distância distorcida. O veredito de cada uma entra na §5.2.
