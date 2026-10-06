# 3.2 · Técnicas — encoding

> Dona: Ana Raquel · Orçamento: parte das 2,0 páginas da §3

Como a etapa de ausentes, o encoding também é **obrigatório**: há 4 atributos nominais e 2
ordinais, e o kNN não calcula distância sobre texto. A pergunta desta etapa é específica do
modelo escolhido — **cada coluna que o encoding cria é uma dimensão a mais na distância
euclidiana**, e é por isso que a decisão pesa aqui mais do que pesaria numa árvore.

O que pesa é `distribuidora`: **455 categorias, 278 delas com um único filme**.

## As ordinais não variam, e isso é uma decisão

`experiencia_da_direcao` e `porte_da_distribuidora` recebem sempre `OrdinalEncoder` com a
ordem declarada em `build_dataset.ORDEM_ORDINAIS` — estreante < iniciante < estabelecida <
veterana, e nova < pequena < media < grande. São faixas com ordem natural, e codificá-las
como inteiros crescentes preserva a única coisa que elas afirmam. Pôr `OneHotEncoder` nelas
destruiria essa ordem e gastaria oito dimensões para dizer o que duas dizem.

O encoder recebe `handle_unknown="use_encoded_value", unknown_value=-1`. O `-1` existe por um
motivo concreto: a opção `mediana_indicadora` da etapa anterior cria a categoria `"ausente"`,
que não tem lugar na ordem das faixas. Ela vira um código **abaixo** de todas elas, o que é a
leitura correta — sem histórico é menos do que a menor faixa.

## As duas opções variam só nas nominais

| id | nominais | colunas que chegam ao kNN |
|---|---|---|
| `onehot` | `OneHotEncoder(min_frequency=10, handle_unknown="infrequent_if_exist", sparse_output=False)` | 78, média de 76 entre os folds |
| `alvo` | `TargetEncoder(target_type="binary", cv=5, shuffle=True, random_state=42)` | **18**, exatas |

A contagem do *one-hot* oscila entre os folds porque o corte de frequência é reajustado em
cada treino: uma categoria com dez filmes pode ficar acima do corte num fold e abaixo em
outro. A do encoding pelo alvo não oscila — são sempre 12 numéricas, 4 nominais e 2 ordinais.
Com `mediana_indicadora` o encoding pelo alvo sobe para 25, sete indicadoras a mais, uma por
atributo com ausência no treino; o *one-hot* sobe para 86, as mesmas sete mais a dummy da
categoria `"ausente"` criada em `uf_maj` e em `origem_do_fomento`.

**`onehot` — a técnica padrão, com um corte justificado.** É a opção do *baseline*. O
`min_frequency=10` não é arbitrário: a sensibilidade S4 da E1 mediu a faixa de 5 a 15 e
encontrou custo de **0,009 de AUC** para o corte de cerca de 380 colunas. Pagar nove
milésimos de AUC para tirar 380 dimensões de uma distância euclidiana é uma troca que o kNN
agradece. As categorias raras caem num nível `infrequent` comum, em vez de cada filme único
virar a própria dimensão.

**`alvo` — porque dimensão é o custo que mais dói no kNN.** O encoding pelo alvo põe cada
nominal em **uma** coluna, com o valor médio do alvo na categoria. As 4 nominais passam a
ocupar 4 dimensões em vez de 64, e categorias com um único filme deixam de ser direções
próprias no espaço. O `TargetEncoder` do scikit-learn faz validação cruzada **interna** no
`fit_transform`, então nenhum filme de treino é codificado com o próprio rótulo; e o
transformador é ajustado só no treino de cada fold, porque está dentro do `Pipeline`. São
duas barreiras, não uma.

> *Target encoding* não é técnica de sala. O enunciado aceita técnica de fora com
> justificativa, e a justificativa é a frase acima: num classificador que decide por
> distância, trocar 64 dimensões por 4 é uma intervenção de natureza diferente das outras
> etapas da grade. O substituto, se o grupo preferisse ficar no programa, seria *frequency
> encoding* — também uma coluna por nominal, mas sem usar o alvo.

## As hipóteses que esta seção leva para §5.2

1. `alvo` **empata ou ganha** de `onehot` em AUC — menos dimensões para a distância.
2. `onehot` sofre mais com PCA e `kbest`: 78 colunas esparsas é justamente o caso em que a
   redução tem algo a fazer, e também o mais caro de rodar.
3. **SMOTE sobre `onehot` cria filmes que não existem.** O SMOTE interpola entre vizinhos; a
   interpolação entre duas dummies produz "0,4 de uma distribuidora e 0,6 de outra". Sobre
   `alvo`, interpola valores contínuos, que é o que o SMOTE pressupõe. Isso é interação
   encoding × balanceamento, e aparece na §3.5 e na §5.3.

> Código: `src/e2/etapas/encoding.py`. Contagem de colunas por fold:
> coluna `n_atributos` de `reports/e2/resultados.csv`.
