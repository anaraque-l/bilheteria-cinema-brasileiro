# 4 · Protocolo executado

> Dona: Ana Raquel; parágrafo de métricas: Laura · Orçamento: 0,75 página

As 144 combinações foram avaliadas com os mesmos cinco folds, pela mesma semente e na mesma ordem
de etapas. É essa uniformidade que autoriza comparar duas linhas da tabela e atribuir a diferença
ao pré-processamento.

**Validação.** Divisão estratificada em cinco folds, embaralhada, semente 42, gerada uma única vez
e gravada com o fold de cada um dos 2.590 filmes; a grade e a robustez recebem essa lista e não
reconstroem a partição. Todos os folds ficam perto de 25,3% de positivos. A E1 defendeu partição
temporal e o enunciado fixa cinco folds: seguimos o enunciado, e a partição temporal entra na §6.

**Ajuste apenas no treino.** As cinco etapas vivem dentro de um pipeline construído de novo para
cada combinação e cada fold, de modo que medianas, categorias e médias dos encodings, parâmetros de
escala e eixos do PCA são estimados no treino do fold e aplicados ao teste. Usamos o pipeline da
biblioteca de reamostragem por ser o único que aceita um reamostrador no meio da sequência e o
aciona apenas no ajuste, de modo que o fold de teste nunca é reamostrado.

**Ordem das etapas dentro de cada fold.**

```
ausentes → encoding → normalização → redução → balanceamento → kNN de 7 vizinhos
```

Ausentes primeiro porque o codificador não aceita valor ausente. Normalização depois do encoding
porque o kNN mede distância na matriz inteira. Redução antes do balanceamento para que os eixos
sejam ajustados só com filmes reais. Balanceamento por último porque o SMOTE interpola no mesmo
espaço em que o kNN vai medir distância. O classificador tem sete vizinhos, pesos uniformes e
distância euclidiana, fixado pelo enunciado.

**Métricas.** *[parágrafo da Laura, ver `4-metricas.md`]*

**Regra de empate.** Duas combinações empatam numa métrica quando a diferença entre as médias é
menor que o maior dos dois desvios entre folds. A regra atende à exigência do enunciado de que
diferença menor que a variabilidade entre folds não sustente conclusão, tem uma única implementação
no código e é conservadora, porque gera mais empates do que um teste pareado geraria. A §5.2
acrescenta um Wilcoxon pareado como verificação independente.

**Reprodutibilidade.** Rodar a grade duas vezes no mesmo ambiente produz as mesmas métricas em
todos os folds, o que confirma que nenhum transformador ficou sem semente. As versões das
bibliotecas estão no anexo, gravadas pela própria execução, e nenhum número deste relatório foi
digitado à mão.

**O teste de que o histórico não vaza.** Os três históricos são o único ponto em que informação de
um filme passa por outro, e por isso recebem verificação própria em vez de argumento. O teste
multiplica por mil o público de todos os filmes de um ano e confere que nenhum histórico daquele ano
ou anterior muda, o que falharia se o histórico olhasse para o próprio ano, e que algum histórico de
ano posterior muda, o que garante que o teste toca a coluna.

Resta uma limitação, que declaramos: com divisão aleatória, o público de um filme do fold de teste
pode compor o histórico de um filme posterior do fold de treino. O rótulo do próprio filme de teste
nunca entra nos atributos dele, mas essa contaminação indireta existe, decorre de o enunciado fixar
partição aleatória, e é o que a validação temporal da §6 mede.
