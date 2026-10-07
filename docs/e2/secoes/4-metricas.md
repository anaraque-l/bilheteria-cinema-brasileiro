# 4 · Protocolo — parágrafo das métricas

> Dona: Laura · Entra na §4 da Ana Raquel, na montagem.

Consideramos o filme de sucesso como a classe positiva. Reportamos as cinco métricas
pedidas, que são acurácia, F1, precisão, revocação e AUC, e acrescentamos a precisão média.
Cada uma aparece como média e desvio-padrão amostral dos 5 folds. A acurácia sozinha
engana neste problema: como 25,3% dos filmes são sucesso, um modelo que sempre responde
"fracasso" acerta 74,7% das vezes e nunca encontra um sucesso. Por isso usamos a AUC como
métrica principal, a mesma da Entrega 1. Ela mede se o modelo coloca os sucessos acima dos
fracassos quando ordena os filmes, sem depender de um ponto de corte. F1, precisão e
revocação medem a decisão final, tomada com o corte padrão de 0,5. No kNN com 7 vizinhos,
esse corte significa que o filme é previsto como sucesso quando pelo menos 4 dos 7
vizinhos são sucesso. Como há três fracassos para cada sucesso, poucos filmes alcançam
esses 4 votos. Por isso esperamos que o efeito do balanceamento apareça no F1 e na
revocação mais do que na AUC.
