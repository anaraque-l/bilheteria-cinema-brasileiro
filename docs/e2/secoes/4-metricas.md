# 4 · Protocolo — parágrafo das métricas

> Dona: Laura · Entra na §4 da Ana Raquel, na montagem.

<!-- Rascunho. 25,3% e 0,747 conferir com base.carregar_xy antes de fechar. -->

A classe positiva é `sucesso` = 1. Reportamos as cinco métricas pedidas — acurácia, F1,
precisão, revocação e AUC — e a precisão média (AP) como complemento, todas como média e
desvio-padrão amostral entre os 5 folds. Com 25,3% de positivos, um classificador que
responde sempre "fracasso" tem acurácia 0,747 e F1 zero; por isso a acurácia não ranqueia
nada aqui. A **AUC**, métrica principal e a mesma da Entrega 1, mede se o modelo **ordena**
bem os filmes, independente de limiar. **F1**, precisão e revocação medem o que acontece
**no limiar padrão de 0,5** — que, num kNN com k = 7, quer dizer "pelo menos 4 dos 7
vizinhos são sucesso". A probabilidade desse kNN só assume oito valores, de 0 a 7/7; num
bairro típico há três fracassos para cada sucesso, e chegar a 4 de 7 é difícil. É nessa
segunda família de métricas, e não na AUC, que o balanceamento deve aparecer.
