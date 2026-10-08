# 5.2 · Efeito isolado de cada etapa

> Dona: cada uma as suas etapas, com as tabelas da Ana Laura · Orçamento: parte das 4,0 páginas da §5

A média por opção, pedida no enunciado, mistura contextos. Por isso cada opção também é comparada
com a de referência dentro de cada contexto das outras quatro etapas, com vitória, empate ou
derrota pela regra da §4. É a contagem pareada que autoriza dizer que uma técnica nunca piorou.

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
| | dez melhores colunas | 0,821 | 0 vitórias, 43 empates, 5 derrotas em 48 |
| balanceamento | sem balanceamento | 0,822 | referência |
| | subamostragem | 0,821 | 0 vitórias, 44 empates, 4 derrotas em 48 |
| | SMOTE | 0,814 | 1 vitória, 41 empates, 6 derrotas em 48 |

**A normalização é a única etapa que decide o resultado.** As três técnicas somam 68 vitórias, 40
empates e nenhuma derrota em 108 comparações, com ganho médio de 0,036 a 0,041, acima do desvio
típico de 0,014 entre folds. Sem escala, a contagem de filmes da distribuidora, de zero a 179, e o
ano decidem a distância, e os indicadores de zero a um viram arredondamento. As três escalas
empatam entre si, com diferença máxima de 0,004: importa normalizar, não qual escala.

**A redução nunca ganhou.** Nem o PCA nem a seleção venceram em um único contexto, e o PCA perdeu
em doze, todos sem normalização (§5.3). A H13 da E1 sobrevive no modelo sensível a dimensão. A
seleção empata com a matriz completa em 43 dos 48 contextos, decidindo com dez colunas em vez de
cerca de cinquenta.

**O encoding pelo alvo tem vantagem pequena e consistente.** O ganho médio, 0,007, é empate pela
regra, mas o pareamento mostra 13 vitórias e nenhuma derrota em 72 contextos. O mecanismo é
dimensional: 18 colunas contra cerca de 76, ou 25 contra 84 com a indicadora.

**A indicadora de ausência não acrescentou nada**, como a §3.1 previa: zero vitórias e quatro
derrotas em 72. A falta de histórico coincide com a contagem de filmes anteriores igual a zero, que
o kNN já usa; as sete colunas novas custam dimensão sem informar.

**O balanceamento não move a AUC e muda a decisão.**

| métrica | sem | subamostragem | SMOTE | pareado contra não balancear |
|---|---|---|---|---|
| revocação | 0,547 | 0,741 | 0,736 | 48 vitórias em 48, para as duas |
| precisão | 0,692 | 0,543 | 0,530 | 48 derrotas em 48, para as duas |
| acurácia | 0,825 | 0,774 | 0,767 | 48 derrotas em 48, para as duas |
| F1 | 0,609 | 0,625 | 0,615 | subamostragem 15 vitórias e 0 derrotas; SMOTE 9 e 7 |

Balancear sobe a revocação em cerca de 0,19 nos 48 contextos e cobra 0,15 de precisão e 0,05 de
acurácia, sem exceção: a AUC avalia a ordenação, que o balanceamento não altera, e as outras
métricas avaliam a decisão no corte de quatro votos em sete. A subamostragem é a opção mais segura
em F1, apesar de descartar metade de cada treino; a explicação provável é que o SMOTE interpola
numa matriz de indicadores e cria filmes com meia distribuidora.

**Verificação independente.** Um Wilcoxon pareado sobre as diferenças por fold confirma as
afirmações fortes, com p entre 10⁻²⁴ e 10⁻⁴¹, e não acusa diferença onde dizemos haver nenhuma, o
balanceamento na AUC, com p = 0,26 (anexo G). Os pares não são independentes, porque contextos
vizinhos compartilham etapas e folds, e por isso os valores de p são otimistas: confirmam a
direção, não medem a força do efeito.
