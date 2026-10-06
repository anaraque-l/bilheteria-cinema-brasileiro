# 3.1 · Técnicas — valores ausentes

> Dona: Ana Raquel · Orçamento: parte das 2,0 páginas da §3

**Não existe a opção de não tratar.** O kNN decide por distância euclidiana, e não há
distância com `NaN`. Por isso a etapa de valores ausentes é obrigatória nas 144 combinações,
e o que varia é só *como* se trata.

A ausência que importa nesta base é a dos três históricos de sucesso, e ela é
**estrutural**: significa que a entidade nunca lançou filme antes.

| atributo | ausente |
|---|---|
| `hist_diretor` | 67,9% |
| `hist_produtora` | 59,6% |
| `hist_distribuidora` | 20,8% |
| maior ausência entre os demais 15 atributos | **0,46%** |

Essa última linha é o que torna a etapa interessante. Sem os históricos, a maior ausência
da base seria de meio por cento, e qualquer comparação entre imputações seria um empate
garantido e sem nada a discutir. Com eles, a escolha da imputação passa a ser uma pergunta
de conceito: **o que é a reputação de quem nunca estreou?**

## As duas opções

| id | numéricas | nominais e ordinais |
|---|---|---|
| `mediana_moda` | `SimpleImputer(strategy="median")` | `SimpleImputer(strategy="most_frequent")` |
| `mediana_indicadora` | `SimpleImputer(strategy="median", add_indicator=True)` | `SimpleImputer(strategy="constant", fill_value="ausente")` |

**`mediana_moda` — a imputação mais elementar, e é de propósito.** É a opção do *baseline*:
se uma técnica mais elaborada não ganhar dela, o relatório tem de dizer isso. Mediana e não
média porque é robusta à cauda das contagens de fomento; nos históricos, que já estão em
`log10` e são quase simétricos, com assimetria de −0,02 a 0,56, as duas praticamente
coincidem. O efeito dessa opção é geométrico: ela coloca o estreante **no meio** da nuvem de
veteranos típicos, que é exatamente onde os vizinhos mais numerosos estão.

**`mediana_indicadora` — porque ausência pode ser informação.** A E1 classificou a ausência
desta base em quatro naturezas e mostrou dois casos em que ela carrega sinal: `max_salas`,
ausente de forma não aleatória, e `coproducao`, um atributo que **nasceu** de uma ausência.
Nos históricos a ausência é estrutural, e a coluna indicadora deixa o kNN enxergar
"estreante" em vez de fingir que o estreante tem reputação mediana.

## A hipótese que esta seção precisa testar

Medimos, nos 2.590 filmes, quanto a falta de histórico coincide com não haver filme anterior
registrado:

| atributo | coincide com `filmes_*_antes = 0` | exceções |
|---|---|---|
| `hist_diretor` | 99,85% | 4 filmes |
| `hist_distribuidora` | 99,92% | 2 filmes |
| `hist_produtora` | 99,88% | 3 filmes |

As nove exceções são entidades cujos filmes anteriores existem mas não têm público
informado. Ou seja: **a ausência já está dita em outras colunas** — `filmes_*_antes = 0`,
`experiencia_da_direcao = "estreante"`, `porte_da_distribuidora = "nova"`. A previsão, então,
é que a indicadora **empate** com a mediana pura: ela acrescenta três colunas que repetem
informação que o kNN já tinha, e três dimensões a mais numa distância euclidiana diluem as
que informam. Se o empate aparecer em §5.2, é este o motivo, e não "as técnicas são
equivalentes".

## Consideradas e descartadas

- **`KNNImputer`** — inventaria uma reputação a partir de filmes parecidos. Quando a ausência
  é estrutural não há valor escondido a recuperar: o estreante não tem público oculto, ele
  não tem público. E poria um kNN dentro do pré-processamento de um kNN, misturando
  justamente os efeitos que o experimento quer isolar.
- **descartar as linhas com ausência** — custaria 68% da base por causa de `hist_diretor`.

> Números desta seção: `reports/e2/base_ausencia.csv` e
> `reports/e2/base_ausencia_estrutural.csv`, gerados por `python src/e2/base.py`.
> Código: `src/e2/etapas/ausentes.py`.
