# 4 · Protocolo executado

> Dona: Ana Raquel; parágrafo de métricas: Laura · Orçamento: 0,75 página

As 144 combinações foram avaliadas com os mesmos cinco folds, pela mesma semente e na mesma
ordem de etapas. É essa uniformidade que autoriza comparar duas linhas da tabela de
resultados e atribuir a diferença ao pré-processamento.

## 4.1 Validação

`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`, gerado uma única vez em
`e2/base.py` e gravado em `reports/e2/folds.csv` com o fold de cada um dos 2.590 filmes. A
grade e a análise de robustez recebem essa lista de índices e não reconstroem a partição. A
estratificação é pelo alvo, de modo que todos os folds ficam perto de 25,3% de positivos.

A E1 defendeu partição temporal, e o enunciado da E2 fixa 5-fold. Seguimos o enunciado, e a
partição temporal entra na §6 como análise de robustez.

## 4.2 Ajuste só no treino

Todas as cinco etapas vivem dentro de um `imblearn.pipeline.Pipeline`, construído de novo
para cada combinação e cada fold. Mediana de imputação, categorias do one-hot, médias do
encoding pelo alvo, parâmetros de escala e eixos do PCA são estimados no treino do fold e
aplicados ao teste. O `Pipeline` do `imbalanced-learn` foi escolhido por ser o único que
aceita um sampler no meio da sequência e o aciona apenas no `fit`, de modo que o fold de
teste não é reamostrado nem pela subamostragem nem pelo SMOTE.

## 4.3 A ordem das etapas

```
ausentes → encoding → normalização → redução → balanceamento → kNN(k=7)
```

| posição | motivo |
|---|---|
| ausentes antes de encoding | o encoder não aceita `NaN`, e a categoria ausente precisa existir antes de virar coluna |
| normalização depois de encoding | o kNN mede distância na matriz inteira, dummies incluídas; normalizar só as numéricas esconderia a interação entre encoding e normalização |
| redução antes de balanceamento | PCA e seleção são ajustados apenas com filmes reais; depois do SMOTE, pontos sintéticos definiriam os eixos |
| balanceamento por último | o SMOTE interpola no mesmo espaço em que o kNN vai medir distância |

`KNeighborsClassifier(n_neighbors=7)`, pesos uniformes, distância euclidiana e o restante nos
valores padrão. O classificador é fixado pelo enunciado para que toda diferença entre
combinações venha do pré-processamento.

## 4.4 Métricas

*[parágrafo da Laura, ver `4-metricas.md`]*

## 4.5 Reprodutibilidade

| garantia | como |
|---|---|
| semente única | `base.SEMENTE = 42`, repassada a todo objeto com `random_state` |
| folds materializados | `reports/e2/folds.csv` |
| versões das bibliotecas | `reports/e2/ambiente.json`, gravado pela própria execução |
| retomada sem perder trabalho | cada combinação é gravada assim que termina; ao reiniciar, os `id` já gravados são pulados |
| falha é resultado | combinação que lança exceção vira linha com métricas vazias e a mensagem na coluna `erro`, e não derruba a grade |
| nenhum número à mão | todo valor citado no relatório vem de arquivo em `reports/e2/` |

O critério de aceite da execução é que rodar a grade duas vezes produza exatamente os mesmos
números. Se isso não ocorrer, há semente faltando em algum transformador. A verificação foi
feita por combinação durante a construção do motor e será confirmada na grade completa.

## 4.6 O teste de que o histórico não vaza

Os três atributos `hist_*` são o único ponto do pré-processamento em que informação de um
filme passa por outro, e por isso recebem uma verificação própria em vez de um argumento. O
teste multiplica por mil o público de todos os filmes de um ano t e verifica duas condições:

1. nenhum `hist_*` de filme com ano ≤ t muda, condição que falharia se o histórico olhasse
   para o próprio ano;
2. algum `hist_*` de filme com ano > t muda, o que garante que o teste de fato toca a coluna.

O teste roda para t em {2005, 2012, 2019}, dentro de `base.checar_nao_vazamento()`, e
interrompe a execução de `base.py` se qualquer das duas condições quebrar.

Resta uma limitação, que declaramos. Com k-fold aleatório, o público de um filme do fold de
teste pode compor o `hist_*` de um filme posterior do fold de treino. O rótulo do próprio
filme de teste nunca entra nos atributos dele, mas essa contaminação indireta entre folds
existe. Ela decorre de o enunciado fixar partição aleatória, e é o que a partição temporal da
§6 verifica.

O código do protocolo está em `src/e2/base.py`, `src/e2/espaco.py` e `src/executar_e2.py`. Os
arquivos gerados são `reports/e2/folds.csv` e `reports/e2/ambiente.json`.
