# 3.1 · Técnicas — valores ausentes

> Dona: Ana Raquel · Orçamento: parte das 2,0 páginas da §3

O tratamento de valores ausentes é obrigatório nas 144 combinações. O kNN decide por
distância euclidiana, e não há distância definida com `NaN`, de modo que não existe a opção
de deixar a base como está. O que varia entre as combinações é a forma do tratamento.

A ausência relevante nesta base é a dos três atributos de histórico, e ela é estrutural:
indica que a entidade nunca lançou filme antes.

| atributo | ausente |
|---|---|
| `hist_diretor` | 67,88% |
| `hist_produtora` | 59,61% |
| `hist_distribuidora` | 20,81% |
| maior ausência entre os outros 15 atributos | 0,46% |

A última linha explica por que a etapa só passou a ter conteúdo com a entrada dos históricos.
Sem eles, a maior ausência da base seria de meio por cento, e a comparação entre imputações
seria um empate previsível.

## As duas opções

| id | numéricas | nominais e ordinais |
|---|---|---|
| `mediana_moda` | `SimpleImputer(strategy="median")` | `SimpleImputer(strategy="most_frequent")` |
| `mediana_indicadora` | `SimpleImputer(strategy="median", add_indicator=True)` | `SimpleImputer(strategy="constant", fill_value="ausente")` |

A opção `mediana_moda` é a imputação mais elementar e compõe o baseline. A mediana foi
preferida à média por ser robusta à cauda das contagens de fomento; nos históricos, que já
estão em `log10` e têm assimetria entre −0,02 e 0,56, as duas medidas praticamente coincidem.
O efeito dessa opção sobre a geometria do problema é posicionar o filme de estreante no meio
da nuvem dos veteranos típicos, que é a região de maior densidade de vizinhos.

A opção `mediana_indicadora` parte de um achado da E1, que classificou a ausência desta base
em quatro naturezas e identificou dois casos em que ela carrega informação: `max_salas`,
ausente de forma não aleatória, e `coproducao`, atributo derivado de uma ausência. Nos
históricos a ausência é estrutural, e a coluna indicadora permite ao kNN distinguir o
estreante em vez de atribuir-lhe reputação mediana.

## A hipótese desta etapa

Medimos, nos 2.590 filmes, quanto a falta de histórico coincide com a inexistência de filme
anterior registrado:

| atributo | coincide com `filmes_*_antes = 0` | exceções |
|---|---|---|
| `hist_diretor` | 99,85% | 4 filmes |
| `hist_distribuidora` | 99,92% | 2 filmes |
| `hist_produtora` | 99,88% | 3 filmes |

As nove exceções são entidades cujos filmes anteriores existem mas não têm público informado.
A informação de que o filme é de estreante, portanto, já consta de outras colunas:
`filmes_*_antes = 0`, `experiencia_da_direcao` igual a `estreante` e
`porte_da_distribuidora` igual a `nova`. A previsão é que as duas imputações empatem. A
indicadora acrescenta sete colunas, e três delas, as dos históricos, repetem informação já
disponível. As outras quatro vêm do fomento e marcam os 12 filmes sem CPB, que não puderam
ser cruzados com os registros. Todas diluem as demais dimensões no cálculo da distância. Caso
o empate se confirme na §5.2, essa é a explicação, e não a equivalência entre as técnicas.

## Alternativas consideradas e descartadas

O `KNNImputer` estima o valor ausente a partir de filmes semelhantes. Quando a ausência é
estrutural não há valor a recuperar, já que o estreante não tem público registrado em
nenhuma forma. A técnica também inseriria um kNN no pré-processamento de um kNN, misturando
os efeitos que o experimento pretende isolar.

Descartar as linhas com ausência eliminaria 68% da base por causa de `hist_diretor`.

Os números desta seção estão em `reports/e2/base_ausencia.csv` e
`reports/e2/base_ausencia_estrutural.csv`, gerados por `python src/e2/base.py`. O código da
etapa está em `src/e2/etapas/ausentes.py`.
