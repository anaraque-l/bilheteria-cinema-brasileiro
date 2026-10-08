# 5.1 · Visão geral, baseline, melhores e piores

> Dona: Ana Laura · Orçamento: parte das 4,0 páginas da §5

As 144 combinações executaram sem nenhuma falha, de modo que a coluna de erro da tabela do anexo
está vazia nas 144 linhas e não há combinação a reportar como inviável.

| | combinação | AUC |
|---|---|---|
| melhor | mediana e moda, encoding pelo alvo, padronização, PCA e subamostragem | 0,853 ± 0,016 |
| baseline | sem nenhuma transformação opcional | 0,827 ± 0,014 |
| pior | indicadora, one-hot, sem normalização, PCA e subamostragem | 0,731 ± 0,015 |

A primeira leitura é a amplitude. Com o modelo fixo em sete vizinhos e os mesmos cinco folds em
todas as linhas, a escolha do pré-processamento move a AUC em 0,122. É mais do que qualquer
ganho que a Entrega 1 obteve trocando de modelo, e justifica o recorte desta entrega: o
pré-processamento não é preparação para o aprendizado, é parte dele.

A segunda leitura vem da regra de empate e é mais incômoda. O baseline ocupa a 61ª posição entre
144, mas **105 das 144 combinações empatam com ele** e apenas dez o superam de forma que a
variabilidade entre folds sustente; 22 empatam com a melhor. O ranking existe, mas boa parte dele
é ruído: relatar apenas médias teria anunciado como descoberta uma ordenação que cinco folds não
autorizam. O que a grade permite afirmar com segurança não é qual pipeline é o melhor, e sim
quais opções nunca prejudicam e quais podem destruir o resultado. A §6 qualifica esse empate, ao
mostrar que parte dele é consequência do próprio protocolo de validação.

Vale notar a composição das pontas. As seis piores combinações da grade são exatamente as seis
que aplicam PCA sem normalização, e em todas elas chegam 2,0 colunas ao classificador. As
melhores têm em comum o encoding pelo alvo e alguma normalização, em qualquer das três. A §5.2
separa esses efeitos e a §5.3 mostra por que eles não são independentes.
