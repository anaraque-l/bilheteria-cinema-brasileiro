# 3.2 · Técnicas — encoding

> Dona: Ana Raquel · Orçamento: parte das 2,0 páginas da §3

O encoding é obrigatório pela mesma razão do tratamento de ausentes: o kNN não calcula distância
sobre texto. A pergunta é específica deste modelo, porque cada coluna criada aqui é uma dimensão a
mais na distância euclidiana e pesa mais do que pesaria numa árvore. O atributo que determina o
tamanho do problema é a distribuidora, com 455 categorias, 278 delas com um único filme.

Os dois atributos ordinais não variam entre as combinações: recebem sempre código inteiro na ordem
natural das faixas. Tratá-los como nominais destruiria essa ordem e gastaria oito dimensões para
dizer o que duas dizem.

| opção | nominais | colunas no kNN | característica dos dados que a motiva |
|---|---|---|---|
| por indicadores | uma coluna por categoria, agrupando as com menos de dez filmes | 78, média de 76 | a S4 da E1 mediu a faixa de cinco a quinze e achou custo de 0,009 de AUC pela remoção de cerca de 380 colunas |
| pelo alvo | uma coluna por nominal, com a média do alvo na categoria | 18, exatas | 455 categorias viram 455 direções em que dois filmes podem diferir; aqui as quatro nominais ocupam quatro dimensões em vez de 64 |

A contagem do one-hot oscila entre os folds porque o corte de frequência é reajustado em cada
treino. Com a imputação por indicadora, o encoding pelo alvo sobe para 25 colunas e o de
indicadores para até 86, média de 84.

O encoding pelo alvo tem duas barreiras independentes contra vazamento: validação cruzada interna,
que impede o filme de ser codificado com o próprio rótulo, e o ajuste restrito ao treino de cada
fold. Não é técnica vista em sala, e o enunciado aceita técnica adicional mediante justificativa:
num classificador que decide por distância, trocar 64 dimensões por quatro é intervenção de
natureza diferente da das outras etapas. O substituto, se o grupo preferisse ficar restrito ao
programa, seria a codificação por frequência.
