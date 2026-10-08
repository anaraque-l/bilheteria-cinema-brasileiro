# 5.2 · Efeito isolado de cada etapa

> Dona: cada uma as suas etapas, com as tabelas da Ana Laura · Orçamento: parte das 4,0 páginas da §5

A tabela traz as duas leituras que o módulo de análise produz para cada etapa. A primeira é a que
o enunciado pede, a média das combinações agrupadas pela opção adotada, e tem um defeito
conhecido: mistura contextos, porque a média de uma opção inclui combinações em que as outras
quatro etapas diferem. A segunda corrige isso por pareamento, fixando as outras quatro etapas e
comparando a opção com a de referência dentro de cada contexto, com vitória, empate ou derrota
decididos pela regra de empate da §4. É a contagem pareada que sustenta afirmação, e é ela que
autoriza dizer que uma técnica nunca piorou.

| etapa | opção | AUC média | pareado contra a referência |
|---|---|---|---|
| ausentes | mediana e moda | 0,820 | referência |
| | indicadora de ausência | 0,818 | 0 vitórias, 68 empates, 4 derrotas em 72 |
| encoding | one-hot | 0,815 | referência |
| | pelo alvo | 0,823 | 13 vitórias, 59 empates, 0 derrotas em 72 |
| normalização | sem normalização | 0,790 | referência |
| | padronização | 0,831 | 22 vitórias, 14 empates, 0 derrotas em 36 |
| | escala por intervalo | 0,827 | 23 vitórias, 13 empates, 0 derrotas em 36 |
| | escala robusta | 0,828 | 23 vitórias, 13 empates, 0 derrotas em 36 |
| redução | sem redução | 0,827 | referência |
| | PCA | 0,809 | 0 vitórias, 36 empates, 12 derrotas em 48 |
| | seleção de dez colunas | 0,821 | 0 vitórias, 43 empates, 5 derrotas em 48 |
| balanceamento | sem balanceamento | 0,822 | referência |
| | subamostragem | 0,821 | 0 vitórias, 44 empates, 4 derrotas em 48 |
| | SMOTE | 0,814 | 1 vitória, 41 empates, 6 derrotas em 48 |

**A normalização é a única etapa que decide o resultado.** As três técnicas somam 68 vitórias, 40
empates e nenhuma derrota em 108 comparações pareadas, perfil que nenhuma outra etapa tem, com
ganho médio entre 0,036 e 0,041. A explicação está na métrica do classificador: a distância
euclidiana soma diferenças sem normalizar unidades, e aqui a contagem de filmes anteriores da
distribuidora varia de zero a 179 enquanto os indicadores de fomento variam de zero a um. Sem
correção, dois filmes são próximos quando têm distribuidoras de porte parecido, e o resto é
arredondamento. As três técnicas empatam entre si, com diferença máxima de 0,004 contra desvio
típico de 0,014 entre folds: o que importa é normalizar, não qual escala escolher.

**A redução nunca ganhou.** Nem o PCA nem a seleção venceram a ausência de redução em um único
contexto, e o PCA perdeu em doze. A H13 da E1 sobrevive, agora testada com o modelo sensível à
dimensão que era a nossa objeção contra ela. Há, porém, um achado de engenharia: a seleção empata
com a matriz completa em 43 dos 48 contextos, e nesses casos o kNN decide com dez colunas em vez
das cerca de cinquenta que chegam sem redução. Não se ganha AUC reduzindo, mas se pode pagar
menos por ela.

**O encoding pelo alvo tem vantagem pequena e consistente.** A diferença média, 0,007, é menor que
o desvio entre folds, e portanto é empate pela nossa regra. O pareamento, contudo, mostra 13
vitórias e nenhuma derrota em 72 contextos, padrão difícil de atribuir ao acaso: a leitura honesta
é que o efeito existe e é pequeno. O mecanismo é dimensional, porque o encoding pelo alvo entrega
dezoito colunas ao classificador contra cerca de 84 do one-hot, e em dimensão menor as distâncias
discriminam melhor.

**A indicadora de ausência não acrescentou nada**, e isso refuta a hipótese da §3.1: zero
vitórias e quatro derrotas em 72 contextos. A explicação mais plausível é que a informação já
estava na base, porque a falta de histórico coincide com a contagem de filmes anteriores igual a
zero em quase todos os casos, e essa contagem é um atributo numérico que o kNN já usa. A
indicadora repete em sete colunas novas aquilo que três colunas antigas diziam, e em dimensão as
colunas repetidas custam sem informar. O critério que fica é verificar, antes de criar indicadora
de ausência, se algum atributo existente já mede o mesmo fenômeno.

**O balanceamento não move a AUC**, como a §4 previu, e é por isso que a discussão dele precisa
de outra métrica. É também onde a nossa hipótese se confirma de forma mais nítida em todo o
trabalho.

| métrica | sem balanceamento | subamostragem | SMOTE | pareado contra não balancear |
|---|---|---|---|---|
| revocação | 0,548 | 0,741 | 0,736 | 48 vitórias em 48, para as duas técnicas |
| precisão | 0,692 | 0,543 | 0,530 | 48 derrotas em 48, para as duas |
| acurácia | 0,825 | 0,774 | 0,767 | 48 derrotas em 48, para as duas |
| F1 | 0,609 | 0,625 | 0,615 | subamostragem: 15 vitórias, 33 empates, 0 derrotas |
| AUC | 0,822 | 0,821 | 0,814 | subamostragem: 0 vitórias, 44 empates, 4 derrotas |

Balancear aumenta a revocação em cerca de 0,19 em todos os 48 contextos, sem uma única exceção, e
cobra por isso 0,15 de precisão e 0,05 de acurácia, também sem exceção. O F1 sobe pouco e a AUC
não se move, que é exatamente o que o mecanismo prevê: a AUC avalia a ordenação dos filmes, que o
balanceamento não altera, enquanto revocação e precisão avaliam a decisão tomada no corte de
quatro votos em sete, que é o que a mudança de proporção no treino desloca.

Entre as duas técnicas, a subamostragem domina o SMOTE: ganha em F1 em quinze contextos sem nunca
perder, enquanto o SMOTE perde em sete. É contraintuitivo, porque a subamostragem descarta cerca
de metade dos filmes de cada treino e o SMOTE não descarta nada. A explicação provável está no
espaço em que o SMOTE opera: ele interpola entre sucessos vizinhos numa matriz que contém colunas
de indicadores, e a interpolação produz valores fracionários em colunas que só deveriam valer zero
ou um, isto é, filmes com meia distribuidora, que entram na votação dos sete como se fossem reais.

A decisão prática depende do uso. Para ordenar filmes por risco, balancear não traz nada. Para
decidir quais filmes merecem atenção, a subamostragem troca precisão por revocação numa proporção
que compensa quando deixar de ver um sucesso custa mais do que examinar um fracasso à toa, o que é
plausível no contexto de política de fomento que motiva o trabalho.
