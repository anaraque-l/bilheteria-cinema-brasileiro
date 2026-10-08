# 3.2 · Técnicas — encoding

> Dona: Ana Raquel · Orçamento: parte das 2,0 páginas da §3

O kNN não calcula distância sobre texto, e cada coluna criada aqui é uma dimensão a mais na
distância euclidiana. O atributo que decide o tamanho do problema é a distribuidora, com 455
categorias, 278 delas com um único filme. As duas ordinais recebem sempre código inteiro na ordem
natural das faixas.

| opção | nominais | colunas no kNN | característica dos dados que a motiva |
|---|---|---|---|
| por indicadores | uma coluna por categoria, agrupando as com menos de dez filmes | média de 76, até 78; com indicadoras de ausência, 84, até 86 | a S4 da E1 mediu o agrupamento de cinco a quinze filmes e achou custo de 0,009 de AUC para cerca de 380 colunas a menos |
| pelo alvo | uma coluna por nominal, com a média do alvo na categoria | 18; com indicadoras de ausência, 25 | as quatro nominais ocupam quatro dimensões em vez de dezenas |

O encoding pelo alvo tem duas barreiras contra vazamento: validação cruzada interna, que impede o
filme de ser codificado com o próprio rótulo, e ajuste restrito ao treino de cada fold. Não é
técnica vista em sala; entra porque, num classificador que decide por distância, trocar dezenas de
dimensões por quatro é intervenção de natureza diferente das outras.
