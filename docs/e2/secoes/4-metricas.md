# 4 · Protocolo — parágrafo das métricas

> Dona: Laura · Entra na §4 da Ana Raquel, na montagem.

O filme de sucesso é a classe positiva. Reportamos as cinco métricas pedidas, acurácia, F1,
precisão, revocação e AUC, mais a precisão média, cada uma como média e desvio-padrão amostral dos
cinco folds. A acurácia sozinha engana aqui: com 25,3% de sucessos, um modelo que sempre responde
fracasso acerta 74,7% das vezes e nunca encontra um sucesso. A AUC é a métrica principal, a mesma
da E1, porque mede se o modelo coloca os sucessos acima dos fracassos ao ordenar, sem depender de
corte. F1, precisão e revocação medem a decisão final, tomada no corte de quatro votos em sete, e
é aí que esperamos o efeito do balanceamento.
