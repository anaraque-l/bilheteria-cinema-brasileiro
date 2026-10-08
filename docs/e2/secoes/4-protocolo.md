# 4 · Protocolo executado

> Dona: Ana Raquel; parágrafo de métricas: Laura · Orçamento: 0,75 página

**Validação.** As 144 combinações usam os mesmos cinco folds estratificados, embaralhados com
semente 42, gerados uma única vez e gravados com o fold de cada filme; todos ficam perto de 25,3% de
positivos. Assim, duas linhas da tabela diferem só pelo pré-processamento. A E1 defendeu partição
temporal; seguimos o enunciado, e a temporal entra na §6.

**Ajuste só no treino e ordem das etapas.** As cinco etapas vivem num pipeline do
`imbalanced-learn` construído de novo a cada combinação e fold, o único que aceita um reamostrador
no meio da sequência e o aciona só no ajuste. A ordem é

```
ausentes → encoding → normalização → redução → balanceamento → kNN de 7 vizinhos
```

Ausentes primeiro porque o codificador não aceita valor ausente; normalização depois do encoding
porque o kNN mede distância na matriz inteira; redução antes do balanceamento para que os eixos
saiam só de filmes reais; balanceamento por último porque o SMOTE interpola no espaço em que o kNN
mede distância. O kNN usa pesos uniformes e distância euclidiana.

**Métricas.** *[parágrafo da Laura, ver `4-metricas.md`]*

**Regra de empate.** Duas combinações empatam numa métrica quando a diferença entre as médias é
menor que o maior dos dois desvios entre folds. A regra tem uma única implementação e é
conservadora; a §5.2 acrescenta um Wilcoxon pareado como verificação.

**Reprodutibilidade e vazamento.** Rodar a grade duas vezes dá as mesmas métricas em todos os
folds; versões no anexo B. Os históricos têm teste próprio: multiplicar por mil o público de um ano
não pode mudar nenhum histórico daquele ano ou anterior. Resta uma limitação: com divisão aleatória,
o público de um filme de teste pode compor o histórico de um filme posterior do treino. É o que a
validação temporal da §6 mede.
