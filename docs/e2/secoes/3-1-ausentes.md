# 3.1 · Técnicas — valores ausentes

> Dona: Ana Raquel · Orçamento: parte das 2,0 páginas da §3

O tratamento é obrigatório nas 144 combinações: o kNN decide por distância euclidiana, e não há
distância definida com valor ausente. O que varia é a forma do tratamento.

A ausência relevante é a dos três históricos, e é estrutural, porque indica que a entidade nunca
lançou filme. Falta o histórico da direção em 67,88% dos filmes, o da produtora em 59,61% e o da
distribuidora em 20,81%; entre os outros quinze atributos a maior ausência é de 0,46%. É essa
última linha que explica por que a etapa só passou a ter conteúdo com a entrada dos históricos.

| opção | o que faz | característica dos dados que a motiva |
|---|---|---|
| mediana e moda | imputa mediana nas numéricas e moda nas categóricas; compõe o baseline | a cauda das contagens de fomento pede mediana, não média; nos históricos, já em logaritmo e com assimetria entre −0,02 e 0,56, as duas coincidem |
| indicadora de ausência | imputa mediana e acrescenta sete colunas que marcam o que faltava | a E1 classificou a ausência desta base em quatro naturezas e achou dois casos em que ela carrega informação |

A primeira posiciona o estreante no meio da nuvem dos veteranos típicos, região de maior densidade
de vizinhos; a segunda deixa o kNN distinguir o estreante em vez de lhe atribuir reputação mediana.

A hipótese é que as duas empatem, e a razão está medida: a falta de histórico coincide com a
inexistência de filme anterior registrado em mais de 99,8% dos casos. Essa informação já consta de
outras colunas, então três das sete indicadoras repetem o que a base diz, e todas diluem as demais
dimensões no cálculo da distância. Estimar o valor ausente a partir de filmes semelhantes foi
descartado por não haver o que recuperar numa ausência estrutural, e por pôr um kNN no
pré-processamento de um kNN.
