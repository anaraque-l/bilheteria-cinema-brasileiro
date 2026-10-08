# 3.1 · Técnicas — valores ausentes

> Dona: Ana Raquel · Orçamento: parte das 2,0 páginas da §3

O tratamento é obrigatório, porque o kNN não define distância com valor ausente. A ausência que
importa é a dos três históricos, e é estrutural: indica que a entidade nunca lançou filme. Falta o
histórico da direção em 67,88% dos filmes, o da produtora em 59,61% e o da distribuidora em
20,81%; nos outros quinze atributos a maior ausência é de 0,46%.

| opção | o que faz | característica dos dados que a motiva |
|---|---|---|
| mediana e moda | imputa mediana nas numéricas e moda nas categóricas; compõe o baseline | a cauda das contagens de fomento pede mediana; nos históricos, já em logaritmo, mediana e média coincidem |
| indicadora de ausência | imputa mediana e acrescenta sete colunas que marcam o que faltava | a E1 classificou a ausência em quatro naturezas e achou dois casos em que ela carrega informação |

A hipótese é que as duas empatem: a falta de histórico coincide com a inexistência de filme
anterior registrado em mais de 99,8% dos casos, informação que já está em outras colunas. Imputar
a partir de filmes semelhantes foi descartado, porque não há o que recuperar numa ausência
estrutural.
