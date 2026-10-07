# 3.2 · Técnicas — encoding

> Dona: Ana Raquel · Orçamento: parte das 2,0 páginas da §3

O encoding é obrigatório pela mesma razão que o tratamento de ausentes: há 4 atributos
nominais e 2 ordinais, e o kNN não calcula distância sobre texto. A pergunta desta etapa é
específica do modelo escolhido, porque cada coluna criada pelo encoding é uma dimensão a mais
na distância euclidiana. A decisão pesa aqui mais do que pesaria numa árvore de decisão.

O atributo que determina o tamanho do problema é `distribuidora`, com 455 categorias, 278
delas com um único filme.

## As ordinais não variam entre as combinações

`experiencia_da_direcao` e `porte_da_distribuidora` recebem sempre `OrdinalEncoder` com a
ordem declarada em `build_dataset.ORDEM_ORDINAIS`: estreante < iniciante < estabelecida <
veterana, e nova < pequena < media < grande. São faixas com ordem natural, e codificá-las
como inteiros crescentes preserva a única informação que elas afirmam. Aplicar
`OneHotEncoder` a elas destruiria essa ordem e gastaria oito dimensões para dizer o que duas
dizem.

O encoder recebe `handle_unknown="use_encoded_value", unknown_value=-1`. O valor -1 atende a
um caso concreto: a opção `mediana_indicadora` da etapa anterior cria a categoria `ausente`,
que não tem lugar na ordem das faixas. Ela recebe um código abaixo de todas elas, que é a
leitura adequada, já que não ter histórico é menos do que pertencer à menor faixa.

## As duas opções

| id | nominais | colunas que chegam ao kNN |
|---|---|---|
| `onehot` | `OneHotEncoder(min_frequency=10, handle_unknown="infrequent_if_exist", sparse_output=False)` | 78, média de 76 entre os folds |
| `alvo` | `TargetEncoder(target_type="binary", cv=5, shuffle=True, random_state=42)` | 18, exatas |

A contagem do one-hot oscila entre os folds porque o corte de frequência é reajustado em cada
treino: uma categoria com dez filmes pode ficar acima do corte num fold e abaixo em outro. A
contagem do encoding pelo alvo não oscila, porque são sempre 12 numéricas, 4 nominais e 2
ordinais. Com `mediana_indicadora` o encoding pelo alvo sobe para 25 colunas, sete
indicadoras a mais, uma por atributo com ausência no treino; o one-hot sobe para 86, as
mesmas sete mais a dummy da categoria `ausente` criada em `uf_maj` e em `origem_do_fomento`.

A opção `onehot` é a técnica padrão e compõe o baseline. O corte `min_frequency=10` vem de
medição: a sensibilidade S4 da E1 avaliou a faixa de 5 a 15 e encontrou custo de 0,009 de AUC
para a remoção de cerca de 380 colunas. Nove milésimos de AUC é um preço baixo por tirar 380
dimensões de uma distância euclidiana. As categorias raras caem num nível `infrequent` comum,
em vez de cada filme único ocupar uma dimensão própria.

A opção `alvo` responde ao custo de dimensão. O encoding pelo alvo põe cada nominal em uma
única coluna, com o valor médio do alvo na categoria. As 4 nominais passam a ocupar 4
dimensões em vez de 64, e categorias com um único filme deixam de ser direções próprias no
espaço. O `TargetEncoder` do scikit-learn faz validação cruzada interna no `fit_transform`,
de modo que nenhum filme de treino é codificado com o próprio rótulo; além disso, o
transformador é ajustado apenas no treino de cada fold, porque está dentro do `Pipeline`. São
duas barreiras independentes contra o vazamento do alvo.

O target encoding não é técnica vista em sala. O enunciado aceita técnica externa mediante
justificativa, e a justificativa é a do parágrafo anterior: num classificador que decide por
distância, trocar 64 dimensões por 4 é uma intervenção de natureza diferente da das outras
etapas da grade. O substituto, caso o grupo preferisse ficar restrito ao programa da
disciplina, seria o frequency encoding, que também usa uma coluna por nominal e não recorre
ao alvo.

## As hipóteses desta etapa

1. `alvo` empata ou supera `onehot` em AUC, por submeter menos dimensões à distância.
2. `onehot` sofre mais com PCA e com `kbest`: 78 colunas esparsas são o caso em que a redução
   tem mais a fazer, e também o mais caro de rodar.
3. SMOTE sobre `onehot` gera filmes que não existem. O SMOTE interpola entre vizinhos, e a
   interpolação entre duas dummies produz valores como 0,4 de uma distribuidora e 0,6 de
   outra. Sobre `alvo`, a interpolação se dá entre valores contínuos, que é o pressuposto da
   técnica. Trata-se de interação entre encoding e balanceamento, tratada na §3.5 e na §5.3.

O código desta etapa está em `src/e2/etapas/encoding.py`. A contagem de colunas por fold está
na coluna `n_atributos` de `reports/e2/resultados.csv`.
