# 6 · Robustez: temporal, P50/P90, por gênero

> Dona: Laura · Orçamento: 0,75 página

Doze combinações passaram por três checagens: o baseline, as cinco melhores, as cinco piores e a
melhor de cada opção de balanceamento.

**Validação temporal.** Treino até 2017, teste de 2018 em diante, a validação defendida pela E1.

| combinação | AUC em cinco folds | AUC temporal | otimismo |
|---|---|---|---|
| baseline | 0,827 | 0,588 | 0,239 |
| alvo, padronização e subamostragem, três variantes | 0,847 a 0,853 | 0,790 a 0,799 | 0,049 a 0,060 |
| alvo e escala por intervalo, três variantes | 0,842 a 0,850 | 0,738 a 0,749 | 0,098 a 0,113 |
| PCA sem normalização, cinco variantes | 0,731 a 0,750 | 0,531 a 0,556 | 0,176 a 0,219 |

![AUC em cinco folds contra AUC no teste de 2018 em diante; abaixo da diagonal, a divisão aleatória é otimista](../../../reports/figuras/e2/fig-lf-auc-5fold-temporal.png)

Todas são otimistas na divisão aleatória, mas o baseline é o mais otimista e cai para 0,588, quase o
acaso, enquanto as com padronização perdem no máximo 0,060. O pré-processamento muda o que o modelo
aprende. Sem escala, a distância é decidida pelo ano e pela contagem de filmes da distribuidora, e
as duas crescem com o tempo: todo filme do teste é de um ano que o treino não tem, e as
distribuidoras chegam ao teste com mais filmes acumulados. As combinações de PCA sem normalização,
que guardam só essas duas colunas, têm otimismo próximo ao do baseline; a escala por intervalo fica
no meio por depender do máximo do treino, que o teste ultrapassa. E as seis com normalização
empatam com a melhor em cinco folds e se separam no futuro, de 0,738 a 0,799: empate sob um
protocolo não é equivalência sob outro.

**Troca do corte do alvo.** Entre os rankings em P50, P75 e P90 a correlação de Spearman é de 0,825
entre P50 e P75, 0,867 entre P75 e P90 e 0,664 entre os extremos, todas significativas. Nos três
cortes as combinações com normalização e encoding pelo alvo ficam entre 0,770 e 0,880, e as de PCA
sem normalização entre 0,711 e 0,750.

**Desempenho por gênero.**

| gênero | filmes | prevalência | AUC no baseline | AUC na melhor | revocação na melhor |
|---|---|---|---|---|---|
| ficção | 1.627 | 35,6% | 0,813 | 0,832 | 0,826 |
| documentário | 908 | 5,6% | 0,699 | 0,693 | 0,118 |

O agregado esconde a limitação mais séria: em documentário a AUC cai cerca de 0,13 e a melhor
combinação encontra menos de um em cada oito sucessos. Com prevalência de 5,6%, menos de um dos
sete vizinhos de um documentário típico é sucesso, e o corte de quatro votos fica inalcançável;
balancear o conjunto não resolve, porque iguala a proporção global, não a da vizinhança.
