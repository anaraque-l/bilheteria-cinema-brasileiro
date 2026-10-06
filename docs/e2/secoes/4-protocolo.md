# 4 · Protocolo executado

> Dona: Ana Raquel; parágrafo de métricas: Laura · Orçamento: 0,75 página

As 144 combinações foram avaliadas com **os mesmos cinco folds**, pela mesma semente, na
mesma ordem de etapas. É isso que autoriza comparar duas linhas da tabela de resultados e
atribuir a diferença ao pré-processamento.

## 4.1 Validação

`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`, gerado **uma única vez** em
`e2/base.py` e gravado em `reports/e2/folds.csv` com o fold de cada um dos 2.590 filmes. A
grade e a análise de robustez recebem essa lista de índices — não reconstroem a partição.
Estratificado pelo alvo, então todos os folds têm perto de 25,3% de positivos.

A E1 defendeu partição temporal, e o enunciado da E2 fixa 5-fold. Seguimos o enunciado, e a
partição temporal entra na §6 como robustez.

## 4.2 Ajuste só no treino

Todas as cinco etapas vivem dentro de um `imblearn.pipeline.Pipeline`, e o pipeline é
construído **de novo** para cada combinação e cada fold. Mediana de imputação, categorias do
*one-hot*, médias do encoding pelo alvo, parâmetros de escala, eixos do PCA: tudo é estimado
no treino do fold e aplicado ao teste. O `Pipeline` do `imbalanced-learn` é usado porque é o
único que aceita um *sampler* no meio e só o aciona no `fit` — **o fold de teste nunca é
reamostrado**, nem pela subamostragem nem pelo SMOTE.

## 4.3 A ordem das etapas, e o motivo de cada posição

```
ausentes → encoding → normalização → redução → balanceamento → kNN(k=7)
```

| posição | por quê |
|---|---|
| ausentes antes de encoding | o encoder não aceita `NaN`, e a categoria "ausente" precisa existir antes de virar coluna |
| normalização depois de encoding | o kNN mede distância na matriz **inteira**, dummies incluídas; normalizar só as numéricas esconderia a interação encoding × normalização |
| redução antes de balanceamento | PCA e seleção são ajustados só com filmes **reais**; depois do SMOTE, pontos sintéticos definiriam os eixos |
| balanceamento por último | o SMOTE interpola no mesmo espaço em que o kNN vai medir distância |

`KNeighborsClassifier(n_neighbors=7)`, pesos uniformes, distância euclidiana, o resto no
padrão — fixo pelo enunciado, para que toda diferença venha do pré-processamento.

## 4.4 Métricas

*[parágrafo da Laura — ver `4-metricas.md`]*

## 4.5 Reprodutibilidade

| garantia | como |
|---|---|
| semente única | `base.SEMENTE = 42`, repassada a todo objeto com `random_state` |
| folds materializados | `reports/e2/folds.csv` |
| versões das bibliotecas | `reports/e2/ambiente.json`, gravado pela própria execução |
| retomada sem perder trabalho | cada combinação é gravada assim que termina; ao reiniciar, os `id` já gravados são pulados |
| falha é resultado | combinação que lança exceção vira linha com métricas vazias e a mensagem na coluna `erro`, e não derruba a grade |
| nenhum número à mão | todo valor citado no relatório vem de arquivo em `reports/e2/` |

O critério de aceite da execução é que **rodar a grade duas vezes dê exatamente os mesmos
números**; se não der, há semente faltando em algum transformador. Verificado por combinação
durante a construção do motor, e a ser confirmado na grade completa.

## 4.6 O teste de que o histórico não vaza

Os três atributos `hist_*` são o único ponto do pré-processamento em que informação de um
filme passa por outro, e por isso levam uma prova própria, não um argumento. O teste
multiplica por mil o público de **todos** os filmes de um ano *t* e verifica duas coisas:

1. nenhum `hist_*` de filme com ano ≤ *t* muda — se o histórico olhasse para o próprio ano,
   esta condição falharia;
2. algum `hist_*` de filme com ano > *t* muda — garante que o teste de fato toca a coluna.

Roda para *t* ∈ {2005, 2012, 2019}, em `base.checar_nao_vazamento()`, e falha a execução de
`base.py` se qualquer das duas condições quebrar.

**Limitação declarada.** Com *k-fold* aleatório, o público de um filme do fold de teste pode
compor o `hist_*` de um filme **posterior** do fold de treino. O rótulo do próprio filme de
teste nunca entra nos atributos dele, mas essa contaminação indireta entre folds existe, é
consequência de o enunciado fixar partição aleatória, e é o que a partição temporal da §6
verifica.

> Código: `src/e2/base.py`, `src/e2/espaco.py`, `src/executar_e2.py`.
> Arquivos do protocolo: `reports/e2/folds.csv` e `reports/e2/ambiente.json`.
