# 5.2 · Efeito isolado de cada etapa

> Dona: cada uma as suas etapas, com as tabelas da Ana Laura · Orçamento: parte das 4,0 páginas da §5

A tabela traz as duas leituras do módulo de análise. A primeira é a que o enunciado pede, a média
das combinações agrupadas pela opção, e tem o defeito de misturar contextos. A segunda corrige
isso por pareamento: fixa as outras quatro etapas e compara a opção com a de referência dentro de
cada contexto, com vitória, empate ou derrota decididos pela regra da §4. É a contagem pareada que
sustenta afirmação, e é ela que autoriza dizer que uma técnica nunca piorou.

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
empates e nenhuma derrota em 108 comparações pareadas, com ganho médio entre 0,036 e 0,041. A
explicação está na métrica do classificador: a distância euclidiana soma diferenças sem normalizar
unidades, e aqui a contagem de filmes anteriores da distribuidora varia de zero a 179 enquanto os
indicadores de fomento variam de zero a um. Sem correção, dois filmes são próximos quando têm
distribuidoras de porte parecido, e o resto é arredondamento. As três escalas empatam entre si,
com diferença máxima de 0,004 contra desvio típico de 0,014 entre folds: o que importa é
normalizar, não qual escala escolher.

**A redução nunca ganhou.** Nem o PCA nem a seleção venceram em um único contexto, e o PCA perdeu
em doze. A H13 da E1 sobrevive, agora testada com o modelo sensível à dimensão que era a nossa
objeção contra ela. Há, porém, um achado de engenharia: a seleção empata com a matriz completa em
43 dos 48 contextos, e nesses casos o kNN decide com dez colunas em vez de cerca de cinquenta.

**O encoding pelo alvo tem vantagem pequena e consistente.** A diferença média, 0,007, é menor que
o desvio entre folds e portanto é empate pela nossa regra; o pareamento mostra 13 vitórias e
nenhuma derrota em 72 contextos, padrão difícil de atribuir ao acaso. A leitura honesta é que o
efeito existe e é pequeno. O mecanismo é dimensional: 18 colunas contra cerca de 76 com mediana e
moda, 25 contra cerca de 84 com a indicadora, e em dimensão menor as distâncias discriminam melhor.

**A indicadora de ausência não acrescentou nada**, o que refuta a hipótese da §3.1: zero vitórias e
quatro derrotas em 72 contextos. A informação já estava na base, porque a falta de histórico
coincide com a contagem de filmes anteriores igual a zero em quase todos os casos, e essa contagem
é um atributo numérico que o kNN já usa. A indicadora repete em sete colunas novas o que três
colunas antigas diziam, e colunas repetidas custam dimensão sem informar.

**O balanceamento não move a AUC e muda a decisão**, como a §4 previu.

| métrica | sem | subamostragem | SMOTE | pareado contra não balancear |
|---|---|---|---|---|
| revocação | 0,547 | 0,741 | 0,736 | 48 vitórias em 48, para as duas |
| precisão | 0,692 | 0,543 | 0,530 | 48 derrotas em 48, para as duas |
| acurácia | 0,825 | 0,774 | 0,767 | 48 derrotas em 48, para as duas |
| F1 | 0,609 | 0,625 | 0,615 | subamostragem: 15 vitórias, 33 empates |
| AUC | 0,822 | 0,821 | 0,814 | subamostragem: 44 empates, 4 derrotas |

Balancear aumenta a revocação em cerca de 0,19 em todos os 48 contextos e cobra 0,15 de precisão e
0,05 de acurácia, também sem exceção. É o que o mecanismo prevê: a AUC avalia a ordenação, que o
balanceamento não altera, enquanto revocação e precisão avaliam a decisão tomada no corte de quatro
votos em sete. Entre as duas técnicas a subamostragem é a mais segura: contra não balancear, ganha
em F1 em quinze contextos e não perde em nenhum, enquanto o SMOTE ganha em nove e perde em sete. É
contraintuitivo, porque a subamostragem descarta metade dos filmes de cada treino; a explicação
provável é o espaço em que o SMOTE opera, interpolando numa matriz com colunas de indicadores e
produzindo filmes com meia distribuidora, que entram na votação como se fossem reais.

**Verificação independente.** A regra de empate é o critério do enunciado, e é por ela que o
relatório decide. Como checagem, aplicamos também o teste de Wilcoxon pareado sobre as diferenças
por fold, aproveitando que os folds são idênticos em todas as combinações.

| afirmação | n | diferença média | p |
|---|---|---|---|
| padronização contra não normalizar | 180 | +0,041 | 3 · 10⁻²⁸ |
| escala por intervalo contra não normalizar | 180 | +0,036 | 1 · 10⁻²⁴ |
| escala robusta contra não normalizar | 180 | +0,038 | 7 · 10⁻²⁷ |
| subamostragem em revocação | 240 | +0,194 | 4 · 10⁻⁴¹ |
| subamostragem em precisão | 240 | −0,150 | 4 · 10⁻⁴¹ |
| subamostragem em AUC | 240 | −0,001 | 0,26 |

As afirmações fortes passam com margem larga, e a única comparação não significativa é justamente
a que afirmamos ser nula, o efeito do balanceamento na AUC. Os pares não são independentes, porque
contextos vizinhos compartilham etapas e os cinco folds são os mesmos, e por isso os valores de p
são otimistas; servem para confirmar a direção, não para medir a força do efeito.
