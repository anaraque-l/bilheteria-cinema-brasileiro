# 6 · Robustez: temporal, P50/P90, por gênero

> Dona: Laura · Orçamento: 0,75 página

A §5 mede tudo sob um único arranjo, divisão aleatória em cinco folds e alvo no percentil 75.
Esta seção pergunta o que das conclusões sobrevive quando o arranjo muda. Doze combinações
passaram pelas três checagens: o baseline, as cinco melhores, as cinco piores e a melhor de cada
opção de balanceamento, contadas uma vez quando coincidem.

**Validação temporal.** Treinamos com os filmes até 2017 e testamos nos de 2018 em diante, que é
a validação defendida pela E1 e substituída pelo enunciado desta entrega.

| combinação | AUC em cinco folds | AUC temporal | otimismo |
|---|---|---|---|
| baseline, sem transformação opcional | 0,827 | 0,588 | 0,239 |
| indicadora, alvo, padronização, PCA, subamostragem | 0,847 | 0,799 | 0,049 |
| alvo, padronização, PCA, subamostragem | 0,853 | 0,793 | 0,060 |
| alvo, padronização, subamostragem | 0,848 | 0,790 | 0,058 |
| alvo, escala por intervalo, PCA | 0,850 | 0,738 | 0,113 |
| PCA sem normalização, quatro variantes | 0,731 a 0,750 | 0,531 a 0,556 | 0,176 a 0,219 |

Todas as doze são otimistas na divisão aleatória, o que a §4 já declarava como limitação, porque
com folds aleatórios o público de um filme do fold de teste pode compor o histórico de um filme
posterior do fold de treino. O que não esperávamos é a distribuição desse otimismo. O baseline é
o mais otimista de todos, com 0,239, e ao prever o futuro cai para 0,588, isto é, quase o acaso.
As três melhores combinações, todas com normalização e encoding pelo alvo, perdem entre 0,049 e
0,060 e seguem acima de 0,79.

A leitura é que o pré-processamento não melhora apenas o número do relatório: muda o que o modelo
aprende. Sem normalização e com one-hot, as 455 colunas de distribuidora deixam o kNN reconhecer
o filme pela identidade de quem o distribui, atalho que funciona dentro do mesmo período e não
transfere para anos em que as distribuidoras são outras. O encoding pelo alvo substitui essa
identidade por uma única coluna de reputação, que é número comparável entre períodos, e a
normalização impede que duas colunas dominem a vizinhança. Isso qualifica a §5.1: parte dos 105
empates com o baseline é artefato da divisão aleatória, porque pipelines indistinguíveis em cinco
folds se separam em mais de 0,20 de AUC quando o teste é o futuro.

**Troca do corte do alvo.** Repetimos as doze combinações nos percentis 50, 75 e 90 do ano
anterior. A correlação de Spearman entre as ordenações é de 0,825 entre P50 e P75, de 0,867 entre
P75 e P90 e de 0,664 entre P50 e P90, todas significativas. A ordenação é estável em relação ao
corte e menos estável nos extremos, o que é natural, porque P50 e P90 definem problemas
diferentes. Mais importante do que a correlação, a separação qualitativa não muda: nos três
cortes as combinações com normalização e encoding pelo alvo ficam entre 0,770 e 0,881, e as de
PCA sem normalização entre 0,711 e 0,750. A recomendação da §7 não depende, portanto, de onde se
coloque a fronteira do sucesso.

**Desempenho por gênero.** A terceira checagem revela a limitação mais séria do modelo.

| gênero | filmes | prevalência | AUC no baseline | AUC na melhor | revocação na melhor |
|---|---|---|---|---|---|
| ficção | 1.627 | 35,6% | 0,813 | 0,832 | 0,826 |
| documentário | 908 | 5,6% | 0,699 | 0,693 | 0,118 |

O número agregado esconde dois problemas distintos. A AUC cai cerca de 0,13 em documentário, o
que indica que os atributos disponíveis descrevem mal o que faz um documentário encontrar
plateia. E a revocação em documentário é de 0,118 na melhor combinação, contra 0,826 em ficção:
mesmo o melhor pipeline encontra menos de um em cada oito documentários de sucesso. O mecanismo é
o do balanceamento levado ao extremo, porque com prevalência de 5,6% menos de um dos sete
vizinhos de um documentário típico é sucesso, e o corte de quatro votos em sete fica inalcançável
em praticamente toda essa parte da base. Balancear o conjunto inteiro não resolve, porque
equaliza a proporção global e não a da vizinhança em que o documentário vive. Para uso real,
documentário e ficção precisariam de limiar próprio, ou de modelos próprios.
