# Pré-processamento e pipelines na previsão de sucesso de bilheteria do cinema brasileiro

**Entrega 2 · CIN0144 — Aprendizado de Máquina e Ciência de Dados · Grupo 11**
Ana Laura, Ana Raquel e Laura Virginia

---

# Resumo


Este trabalho avalia sistematicamente o efeito do pré-processamento sobre o desempenho de um
classificador k-Nearest Neighbors na previsão de sucesso de bilheteria do cinema brasileiro.
Partindo da base de 2.626 filmes analisada na Entrega 1, construímos um pipeline de cinco etapas e
avaliamos as 144 combinações possíveis das opções escolhidas, sempre com o mesmo modelo, sete
vizinhos, e a mesma partição em cinco folds.

Consideramos sucesso o público acima do percentil 75 dos filmes do ano anterior, limiar conhecido
antes da estreia. Restam 2.590 filmes, dos quais 25,3% são sucesso.

As 144 combinações executaram sem falha. Com o modelo fixo, a escolha do pré-processamento move a
AUC em 0,122, de 0,731 a 0,853. Três resultados sustentam a discussão. A normalização é a única
etapa que decide o desempenho, com 68 vitórias e nenhuma derrota em 108 comparações pareadas. A
aplicação de PCA sobre uma matriz não escalada reduz o espaço a dois componentes e custa 0,065 de
AUC. E o balanceamento não altera a AUC, mas eleva a revocação em 0,19 em todos os contextos, ao
custo de 0,15 de precisão.

Adotamos a regra de empate exigida pelo enunciado, segundo a qual diferença menor que a
variabilidade entre folds não sustenta conclusão. Por ela, 104 das outras 143 combinações empatam
com a configuração de referência. A validação temporal qualifica esse resultado: a configuração sem
nenhuma transformação opcional cai de 0,827 para 0,588 ao prever anos futuros, enquanto as
combinações com padronização e encoding pelo alvo permanecem acima de 0,79.

# 1 · Contexto: o problema, o que a E1 deixou, o alvo P75


**O problema.** Queremos prever se um filme brasileiro vai ter público acima do comum usando
apenas informações disponíveis antes da estreia, com a listagem da ANCINE de 1995 a 2024 e os
dados de fomento público de cada filme. A pergunta é a da Entrega 1: o dinheiro público está indo
para filmes que encontram plateia?

**O que a E1 deixou.** Medimos três atalhos que inflam o resultado sem ensinar nada ao modelo: a
renda como atributo somava 0,161 à AUC, o número máximo de salas 0,108, e a divisão aleatória em
vez de separar por ano 0,087. A auditoria do alvo mostrou ainda que o público forma duas
populações, a de circuito limitado e a de lançamento comercial, com fronteira perto do percentil
69, e que a mediana cai dentro da primeira.

**O alvo P75.** O percentil 75 do ano anterior não embute o ano, já está publicado quando o filme
estreia e cai perto da fronteira entre as duas populações. Com ele, 2.590 filmes têm alvo e 25,3%
são sucesso; os cortes em P50 e P90 entram na §6.

**O que muda.** O modelo é fixo, um kNN de sete vizinhos, e comparamos 144 formas de preparar os
dados para ele. Duas conclusões da E1 voltam à prova: não balancear, medida num alvo meio a meio,
e não aplicar PCA, medida com floresta aleatória, que não sente escala nem dimensão. O kNN sente
as duas.

# 2 · Base, alvo e atributos da E2


A base é a mesma da Entrega 1: 2.626 longas brasileiros lançados em sala entre 1995 e 2024, a
partir dos dados abertos da ANCINE, do IBGE e do Banco Central, sem alteração no módulo que a
monta.

**A definição de sucesso.** Público acima do percentil 75 dos filmes brasileiros do ano anterior.
O alvo antigo, a mediana global dos trinta anos, embutia o ano: os lançamentos cresceram catorze
vezes entre 1995 e 2024 e o público mediano por filme caiu quinze vezes. A mediana do próprio ano
só se conhece depois de todas as estreias. Ficam sem alvo 36 filmes, 22 sem público informado e 14
de 1995, que não têm ano anterior. A prevalência de sucesso fica entre 23,0% e 29,1% nas quatro
décadas, porque o limiar acompanha o ano.

**Os atributos de histórico.** Três atributos novos medem a reputação da direção, da distribuidora
e da produtora: o logaritmo da mediana do público dos filmes da mesma entidade em anos estritamente
anteriores, ausente quando não há nenhum. Mediana e logaritmo porque o público é lei de potência,
com Gini de 0,92. Eles carregam o sinal das colunas de identidade sem o custo de dimensão que as
1.738 categorias de direção imporiam ao kNN.

**Os dezoito atributos.** Nove numéricas, três de histórico, quatro nominais e duas ordinais; o
anexo F traz a lista e o motivo de cada exclusão, todas decisões já tomadas na E1. Uma verificação
no código interrompe a execução se qualquer coluna conhecida só depois da estreia aparecer entre os
atributos.

# 3.1 · Técnicas — valores ausentes


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

# 3.2 · Técnicas — encoding


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

# 3.3 · Técnicas — normalização


A distância euclidiana soma as diferenças de todas as colunas sem distinguir o que cada uma mede,
e aqui as escalas são incomparáveis: o ano vai de 1996 a 2024, a contagem de filmes anteriores da
distribuidora de zero a 179 com mediana 10, os indicadores de fomento valem zero ou um. Sem
correção, as colunas de maior amplitude decidem quem é vizinho. A etapa age na matriz inteira,
depois do encoding, porque é nela que o kNN mede distância.

| opção | o que faz | característica dos dados que a motiva |
|---|---|---|
| sem normalização | preserva as escalas cruas; compõe o baseline | testa se as escalas cruas já servem |
| padronização | centra em zero e divide pelo desvio-padrão | é o tratamento direto do problema de amplitude |
| escala por intervalo | leva cada coluna a zero a um | as binárias ficam intactas; o custo é depender do máximo, e numa cauda longa a maioria dos filmes fica perto de zero |
| escala robusta | centra na mediana e divide pelo intervalo interquartil | as contagens de filmes anteriores têm assimetria de 2,0 a 3,8, e mediana e intervalo interquartil são as medidas dessa cauda |

A hipótese é que a melhor normalização dependa do encoding: numa binária em que 1% dos filmes vale
um, o desvio-padrão é cerca de 0,0995, e a padronização leva o valor um a cerca de 9,9. Previmos
que ela renderia menos no one-hot; a §5.3 mostra outra forma. Uma transformação de potência ficou
fora para manter o espaço em 144 combinações.

# 3.4 · Técnicas — redução de dimensionalidade


Com o one-hot chegam ao kNN de 76 a 84 colunas, boa parte quase vazia, e em dimensão alta o
vizinho mais próximo deixa de ser muito mais próximo que o mais distante. A H13 da E1 concluiu que
não valia aplicar PCA, mas foi medida com floresta aleatória, indiferente a escala e dimensão.

| opção | estratégia | característica dos dados que a motiva |
|---|---|---|
| sem redução | preserva todas as colunas; compõe o baseline | é a H13 da E1, agora num modelo sensível a dimensão |
| PCA retendo 95% da variância | troca as colunas por combinações delas | as colunas do one-hot são em boa parte esparsas, o caso em que a concentração de distâncias pesa |
| dez melhores por informação mútua | mantém colunas originais e descarta o resto | a E1 achou atributos redundantes, e na distância um atributo ruidoso pesa tanto quanto um útil |

Informação mútua em vez de teste F porque a relação que interessa ao kNN não precisa ser linear. O
orçamento de dez colunas é absoluto porque ao seletor chegam de 18 a 84 colunas, conforme o
encoding, e só um número fixo mantém "as dez melhores" com o mesmo sentido. A etapa vem antes do
balanceamento para ser ajustada só com filmes reais. A hipótese é que a redução só seja inofensiva
com normalização: sem ela, a variância é quase toda de duas colunas, e o corte de 95% sairia em um
ou dois componentes.

# 3.5 · Técnicas — balanceamento


Com 25,3% de sucessos há um para cada três fracassos. A E1 decidiu não balancear com o alvo na
mediana, meio a meio; com o novo alvo a classe de sucesso é minoritária. O kNN prevê sucesso quando
pelo menos quatro dos sete vizinhos são sucesso, e não tem peso por classe: a única forma de mudar a
votação é mudar a proporção de sucessos no treino.

| opção | o que faz | vantagem e custo |
|---|---|---|
| sem balanceamento | mantém a base | referência |
| subamostragem | remove fracassos ao acaso até igualar as classes | equilibra o voto, mas descarta cerca de 1.020 dos 2.070 filmes de cada treino, e o kNN depende de densidade |
| SMOTE | cria sucessos entre dois sucessos parecidos, entre os cinco mais próximos | não descarta nada, mas no espaço do one-hot cria filmes com metade de uma distribuidora e metade de outra |

O balanceamento acontece só no treino. Duplicar sucessos ao acaso ficou fora porque um filme
copiado pode ocupar vários dos sete vizinhos. A hipótese, registrada antes da grade, é que
balancear aumente a revocação e o F1, diminua a precisão e a acurácia e quase não mexa na AUC, que
não depende de ponto de corte.

# 4 · Protocolo executado


**Validação.** As 144 combinações usam os mesmos cinco folds estratificados, embaralhados com
semente 42, gerados uma única vez e gravados com o fold de cada filme; todos ficam perto de 25,3% de
positivos. Assim, duas linhas da tabela diferem só pelo pré-processamento. A E1 defendeu partição
temporal; seguimos o enunciado, e a temporal entra na §6.

**Ajuste só no treino e ordem das etapas.** As cinco etapas vivem num pipeline do
`imbalanced-learn` construído de novo a cada combinação e fold, o único que aceita um reamostrador
no meio da sequência e o aciona só no ajuste. A ordem é

```
ausentes → encoding → normalização → redução → balanceamento → kNN de 7 vizinhos
```

Ausentes primeiro porque o codificador não aceita valor ausente; normalização depois do encoding
porque o kNN mede distância na matriz inteira; redução antes do balanceamento para que os eixos
saiam só de filmes reais; balanceamento por último porque o SMOTE interpola no espaço em que o kNN
mede distância. O kNN usa pesos uniformes e distância euclidiana.

**Métricas.** *[parágrafo da Laura, ver `4-metricas.md`]*

**Regra de empate.** Duas combinações empatam numa métrica quando a diferença entre as médias é
menor que o maior dos dois desvios entre folds. A regra tem uma única implementação e é
conservadora; a §5.2 acrescenta um Wilcoxon pareado como verificação.

**Reprodutibilidade e vazamento.** Rodar a grade duas vezes dá as mesmas métricas em todos os
folds; versões no anexo B. Os históricos têm teste próprio: multiplicar por mil o público de um ano
não pode mudar nenhum histórico daquele ano ou anterior. Resta uma limitação: com divisão aleatória,
o público de um filme de teste pode compor o histórico de um filme posterior do treino. É o que a
validação temporal da §6 mede.



O filme de sucesso é a classe positiva. Reportamos acurácia, F1, precisão, revocação e AUC, mais a
precisão média, como média e desvio-padrão amostral dos cinco folds. Com 25,3% de sucessos, quem
sempre responde fracasso acerta 74,7% e nunca encontra um sucesso, por isso a acurácia não decide.
A AUC é a métrica principal, como na E1, porque mede a ordenação sem depender de corte; F1,
precisão e revocação medem a decisão no corte de quatro votos em sete, onde esperamos o efeito do
balanceamento.

# 5.1 · Visão geral, baseline, melhores e piores


As 144 combinações executaram sem nenhuma falha; a tabela completa está no anexo A.

| | combinação | AUC |
|---|---|---|
| melhor | mediana e moda, encoding pelo alvo, padronização, PCA e subamostragem | 0,853 ± 0,016 |
| baseline | sem nenhuma transformação opcional | 0,827 ± 0,014 |
| pior | indicadora, one-hot, sem normalização, PCA e subamostragem | 0,731 ± 0,015 |

Com o modelo fixo e os mesmos folds, o pré-processamento move a AUC em 0,122, mais do que a E1
ganhou trocando de modelo. Mas a regra de empate cobra o seu preço: o baseline ocupa a 61ª posição
e **104 das outras 143 combinações empatam com ele**; só dez o superam de forma que a variabilidade
entre folds sustente, e 21 empatam com a melhor. O que a grade autoriza afirmar não é qual pipeline
é o melhor, e sim quais opções nunca prejudicam e quais podem destruir o resultado.

![As 144 combinações em ordem de AUC, com o desvio entre folds; em azul as que empatam com a melhor](../../reports/figuras/e2/fig-al-ranking.png)

As doze piores, da 133ª à 144ª, são exatamente as doze que aplicam PCA sem normalização, todas com
2,0 colunas chegando ao classificador: são os pontos depois do salto na figura. As melhores têm em
comum o encoding pelo alvo e alguma normalização.

A combinação do topo aplica PCA, e a §5.2 conclui que a redução não venceu em nenhum contexto. As
duas coisas convivem porque a posição no ranking vem da média e o veredito vem do pareado: a mesma
combinação sem o PCA fica em 0,848, dentro do desvio. Ocupar o primeiro lugar não é o mesmo que ter
chegado lá por causa de uma etapa.

# 5.2 · Efeito isolado de cada etapa


A média por opção, pedida no enunciado, mistura contextos. Por isso cada opção também é comparada
com a de referência dentro de cada contexto das outras quatro etapas, com vitória, empate ou
derrota pela regra da §4. É a contagem pareada que autoriza dizer que uma técnica nunca piorou.

| etapa | opção | AUC média | pareado contra a referência |
|---|---|---|---|
| ausentes | mediana e moda | 0,820 | referência |
| | indicadora de ausência | 0,818 | 0 vitórias, 68 empates, 4 derrotas em 72 |
| encoding | one-hot | 0,815 | referência |
| | pelo alvo | 0,823 | 13 vitórias, 59 empates, 0 derrotas em 72 |
| normalização | sem normalização | 0,790 | referência |
| | padronização | 0,831 | 22 vitórias, 14 empates, 0 derrotas em 36 |
| | escala por intervalo | 0,827 | 23 vitórias, 13 empates, 0 derrotas em 36 |
| | escala robusta | 0,828 | 23 vitórias, 13 empates, 0 derrotas em 36 |
| redução | sem redução | 0,827 | referência |
| | PCA | 0,809 | 0 vitórias, 36 empates, 12 derrotas em 48 |
| | dez melhores colunas | 0,821 | 0 vitórias, 43 empates, 5 derrotas em 48 |
| balanceamento | sem balanceamento | 0,822 | referência |
| | subamostragem | 0,821 | 0 vitórias, 44 empates, 4 derrotas em 48 |
| | SMOTE | 0,814 | 1 vitória, 41 empates, 6 derrotas em 48 |

**A normalização é a única etapa que decide o resultado.** As três técnicas somam 68 vitórias, 40
empates e nenhuma derrota em 108 comparações, com ganho médio de 0,036 a 0,041, acima do desvio
típico de 0,014 entre folds. Sem escala, a contagem de filmes da distribuidora, de zero a 179, e o
ano decidem a distância, e os indicadores de zero a um viram arredondamento. As três escalas
empatam entre si, com diferença máxima de 0,004: importa normalizar, não qual escala.

**A redução nunca ganhou.** Nem o PCA nem a seleção venceram em um único contexto, e o PCA perdeu
em doze, todos sem normalização (§5.3). A H13 da E1 sobrevive no modelo sensível a dimensão. A
seleção empata com a matriz completa em 43 dos 48 contextos, decidindo com dez colunas em vez de
cerca de cinquenta.

**O encoding pelo alvo tem vantagem pequena e consistente.** O ganho médio, 0,007, é empate pela
regra, mas o pareamento mostra 13 vitórias e nenhuma derrota em 72 contextos. O mecanismo é
dimensional: 18 colunas contra cerca de 76, ou 25 contra 84 com a indicadora.

**A indicadora de ausência não acrescentou nada**, como a §3.1 previa: zero vitórias e quatro
derrotas em 72. A falta de histórico coincide com a contagem de filmes anteriores igual a zero, que
o kNN já usa; as sete colunas novas custam dimensão sem informar.

**O balanceamento não move a AUC e muda a decisão.**

| métrica | sem | subamostragem | SMOTE | pareado contra não balancear |
|---|---|---|---|---|
| revocação | 0,547 | 0,741 | 0,736 | 48 vitórias em 48, para as duas |
| precisão | 0,692 | 0,543 | 0,530 | 48 derrotas em 48, para as duas |
| acurácia | 0,825 | 0,774 | 0,767 | 48 derrotas em 48, para as duas |
| F1 | 0,609 | 0,625 | 0,615 | subamostragem 15 vitórias e 0 derrotas; SMOTE 9 e 7 |

Balancear sobe a revocação em cerca de 0,19 nos 48 contextos e cobra 0,15 de precisão e 0,05 de
acurácia, sem exceção: a AUC avalia a ordenação, que o balanceamento não altera, e as outras
métricas avaliam a decisão no corte de quatro votos em sete. A subamostragem é a opção mais segura
em F1, apesar de descartar metade de cada treino; a explicação provável é que o SMOTE interpola
numa matriz de indicadores e cria filmes com meia distribuidora.

**Verificação independente.** Um Wilcoxon pareado sobre as diferenças por fold confirma as
afirmações fortes, com p entre 10⁻²⁴ e 10⁻⁴¹, e não acusa diferença onde dizemos haver nenhuma, o
balanceamento na AUC, com p = 0,26 (anexo G). Os pares não são independentes, porque contextos
vizinhos compartilham etapas e folds, e por isso os valores de p são otimistas: confirmam a
direção, não medem a força do efeito.

# 5.3 · Interações


O enunciado define interação como a técnica que só se mostra benéfica na presença de outra. A
análise compara cada opção com a sua referência dentro de cada recorte da outra etapa e marca
interação quando o veredito muda de recorte para recorte. Na AUC, dois pares foram marcados.

![AUC média em cada cruzamento de duas etapas](../../reports/figuras/e2/fig-al-interacoes.png)

**A redução depende da normalização.**

| PCA contra não reduzir | vitórias, empates, derrotas | ganho médio | veredito |
|---|---|---|---|
| com qualquer das três escalas | 0, 36, 0 | de −0,003 a +0,000 | empate |
| sem normalização | 0, 0, 12 | **−0,065** | perde |

Nas combinações de PCA sem normalização chegam 2,0 colunas ao classificador. Sem escala, a
variância é quase toda da contagem de filmes da distribuidora e do ano, dois componentes bastam
para os 95%, e o kNN recebe um espaço que só sabe o porte da distribuidora e o ano. Com
normalização a perda cai a 0,002, sete vezes abaixo do desvio entre folds: empate pela regra,
embora o Wilcoxon a acuse com p = 0,003, porque é pequena e sistemática. A lição é de ordem: num
pipeline com kNN, o PCA precisa vir depois de uma escala. A seleção por informação mútua não tem
esse problema, porque associação com o alvo não depende da unidade da coluna.

**A normalização rende mais com o encoding pelo alvo.**

| contra não normalizar | com encoding pelo alvo | com one-hot |
|---|---|---|
| padronização | 15, 3, 0 · +0,047 · vence | 7, 11, 0 · +0,035 · empate |
| escala por intervalo | 17, 1, 0 · +0,049 · vence | 6, 12, 0 · +0,024 · empate |
| escala robusta | 15, 3, 0 · +0,042 · vence | 8, 10, 0 · +0,033 · empate |

As três vencem com o encoding pelo alvo e só empatam com o one-hot, sem perder em nenhum recorte.
O formato contraria a §3.3: esperávamos que a padronização sofresse no one-hot e a escala por
intervalo fosse a mais segura ali, e é a escala por intervalo que mais perde ao passar para o
one-hot, de 0,049 para 0,024. Ela não mexe nas binárias, mas comprime as contagens de cauda longa
perto de zero, e as dezenas de binárias passam a dominar a distância. O fator 9,9 não apareceu,
provavelmente porque o one-hot agrupa as categorias com menos de dez filmes e as colunas raríssimas
de que o argumento dependia não chegam a existir; é hipótese, não efeito isolado.

**Balanceamento e normalização interagem no F1, não na AUC.** Sem normalização, balancear vence em
F1, a subamostragem em oito dos doze contextos e o SMOTE em nove; com qualquer escala, o veredito
passa a empate. O kNN sem escala é o que mais deixa de alcançar quatro votos de sucesso, e é ali que
inflar a classe rara mais rende. Na AUC sobra só magnitude: a subamostragem perde 0,013 em média
sem normalização, com quatro derrotas, e ganha 0,007 com padronização, porque descartar metade dos
filmes rarefaz a vizinhança num espaço já decidido por duas colunas.

# 5.4 · Custo


A grade inteira levou 3,9 minutos de ajuste e predição, com mediana de 0,92 segundo por combinação
e máximo de 3,99; o tempo de cada opção está no anexo G. A normalização, que decide o resultado, é
quase de graça: 0,42 segundo separa a opção mais barata da mais cara. O custo se concentra no
one-hot, 2,21 segundos em média contra 1,02 do encoding pelo alvo, e na seleção por informação
mútua, 2,60 contra 0,76 sem redução; as dez combinações mais caras são todas one-hot, seleção e
indicadora.

A correlação de Spearman entre o tempo e o número de colunas que chegam ao kNN é de −0,144, fraca e
não significativa (p = 0,09). As combinações mais caras entregam exatamente dez colunas, porque
usam a seleção: o custo não está em medir distância em muitas dimensões, está em estimar
informação mútua entre até 84 colunas e o alvo em cada fold. Nessas combinações o ajuste custa três
vezes a predição. A seleção, que custa mais que o triplo de não reduzir e não ganha em nenhum
contexto, só se paga quando o objetivo é um modelo final mais enxuto.

# 6 · Robustez: temporal, P50/P90, por gênero


Doze combinações passaram por três checagens: o baseline, as cinco melhores, as cinco piores e a
melhor de cada opção de balanceamento.

**Validação temporal.** Treino até 2017, teste de 2018 em diante, a validação defendida pela E1.

| combinação | AUC em cinco folds | AUC temporal | otimismo |
|---|---|---|---|
| baseline | 0,827 | 0,588 | 0,239 |
| alvo, padronização e subamostragem, três variantes | 0,847 a 0,853 | 0,790 a 0,799 | 0,049 a 0,060 |
| alvo e escala por intervalo, três variantes | 0,842 a 0,850 | 0,738 a 0,749 | 0,098 a 0,113 |
| PCA sem normalização, cinco variantes | 0,731 a 0,750 | 0,531 a 0,556 | 0,176 a 0,219 |

![AUC em cinco folds contra AUC no teste de 2018 em diante; abaixo da diagonal, a divisão aleatória é otimista](../../reports/figuras/e2/fig-lf-auc-5fold-temporal.png)

Todas são otimistas na divisão aleatória, mas o baseline é o mais otimista e cai para 0,588, quase o
acaso, enquanto as com padronização perdem no máximo 0,060. O pré-processamento muda o que o modelo
aprende. Sem escala, a distância é decidida pelo ano e pela contagem de filmes da distribuidora, e
as duas crescem com o tempo: todo filme do teste é de um ano que o treino não tem, e as
distribuidoras chegam ao teste com mais filmes acumulados. As combinações de PCA sem normalização,
que guardam só essas duas colunas, têm otimismo próximo ao do baseline; a escala por intervalo fica
no meio por depender do máximo do treino, que o teste ultrapassa. E as seis com normalização
empatam com a melhor em cinco folds e se separam no futuro, de 0,738 a 0,799: empate sob um
protocolo não é equivalência sob outro.

**Troca do corte do alvo.** Entre os rankings destas doze em P50, P75 e P90 a correlação de Spearman
é de 0,825 entre P50 e P75, 0,867 entre P75 e P90 e 0,664 entre os extremos, todas significativas.
Nos três cortes as combinações com normalização e encoding pelo alvo ficam entre 0,770 e 0,880, e as
de PCA sem normalização entre 0,711 e 0,750. São doze pontos, então a conclusão é sobre a separação
entre esses grupos, não sobre a ordem das 144.

**Desempenho por gênero.**

| gênero | filmes | prevalência | AUC no baseline | AUC na melhor | revocação na melhor |
|---|---|---|---|---|---|
| ficção | 1.627 | 35,6% | 0,813 | 0,832 | 0,826 |
| documentário | 908 | 5,6% | 0,699 | 0,693 | 0,118 |

Os dois gêneros cobrem 2.535 dos 2.590 filmes; os 55 restantes são 54 de animação e um videomusical,
pouco para medir separado.

O agregado esconde a limitação mais séria: em documentário a AUC cai cerca de 0,13 e a melhor
combinação encontra menos de um em cada oito sucessos. Com prevalência de 5,6%, menos de um dos
sete vizinhos de um documentário típico é sucesso, e o corte de quatro votos fica inalcançável;
balancear o conjunto não resolve, porque iguala a proporção global, não a da vizinhança.

# 7 · Lições, limitações e conclusão


**Uma etapa decide, e as outras quatro empatam.** Normalizar move a AUC em cerca de 0,04 e nunca
prejudicou em 108 comparações pareadas. Para um classificador que decide por distância é coerente:
a única etapa que mexe diretamente na métrica de distância é a de escala.

**O perigo está nas combinações incoerentes.** As piores configurações não usam técnica
desaconselhada: aplicam PCA, que é padrão, a uma matriz não escalada, e sobram dois componentes; nas
doze vezes em que isso ocorre, o PCA perde em média 0,065 contra não reduzir. É o argumento a favor
de examinar combinações em vez de ajustar uma etapa por vez.

**Reduzir não melhora, mas pode baratear.** A seleção empata com a matriz completa em 43 dos 48
contextos com dez colunas.

**Empate sob um protocolo não é equivalência.** Pela regra de empate quase nada do que um ranking
por média sugeriria sobrevive aos cinco folds, e a validação temporal mostrou o outro lado: seis
combinações que empatam com a melhor se separam em cerca de 0,06 no futuro, e o baseline cai de
0,827 para 0,588. Com padronização e encoding pelo alvo o modelo perde cerca de 0,05 ao prever o futuro, em vez de
0,24, porque deixa de escolher vizinhos pelo ano e pelas contagens acumuladas.

**Limitações.** A contaminação indireta dos históricos entre folds decorre da divisão aleatória e é
o que a validação temporal mede. Em documentário a revocação é de 0,118; entre as doze combinações
verificadas, só as de PCA sem normalização com subamostragem passam de 0,47, marcando mais filmes
como sucesso e com AUC de 0,64 nesse gênero, contra 0,69 da melhor. E os sete vizinhos, fixados pelo
enunciado, são parte da razão de a classe rara quase nunca ser prevista.

**O que faríamos a seguir.** Uma transformação de potência antes da escala; a grade sem o
agrupamento de categorias raras do one-hot, que isolaria o efeito que a §5.3 só pôde conjeturar; e
o número de vizinhos ajustado em cada fold, com limiar próprio por gênero.

# Anexo · Tabela das 144, ambiente, folds, atributos e tabelas de apoio


## A · Tabela completa das 144 combinações

A tabela está em `reports/e2/anexo_144.md`, gerada por `python src/e2/anexo.py` a partir do
arquivo de resultados, e tem uma linha por combinação com o identificador, a opção adotada em cada
uma das cinco etapas, média e desvio das seis métricas, o número de colunas que chegaram ao
classificador, o tempo de execução e a coluna de erro. A mesma tabela em valores separados por
vírgula, no mesmo diretório, serve para importar no documento final sem digitação. A coluna de
erro está vazia nas 144 linhas: nenhuma combinação falhou.

| id | ausentes | encoding | normalizacao | reducao | balanceamento | acurácia | F1 | precisão | revocação | AUC | AP | atributos | tempo (s) | erro |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 (base) | mediana_moda | onehot | sem | sem | sem | 0,807 ± 0,013 | 0,543 ± 0,035 | 0,673 ± 0,036 | 0,456 ± 0,036 | 0,827 ± 0,014 | 0,585 ± 0,023 | 76 | 0,9 |  |
| 2 | mediana_moda | onehot | sem | sem | subamostragem | 0,741 ± 0,030 | 0,588 ± 0,039 | 0,492 ± 0,038 | 0,731 ± 0,041 | 0,807 ± 0,029 | 0,536 ± 0,025 | 76 | 0,8 |  |
| 3 | mediana_moda | onehot | sem | sem | smote | 0,756 ± 0,013 | 0,612 ± 0,016 | 0,512 ± 0,016 | 0,763 ± 0,020 | 0,819 ± 0,013 | 0,568 ± 0,030 | 76 | 0,9 |  |
| 4 | mediana_moda | onehot | sem | pca | sem | 0,779 ± 0,011 | 0,464 ± 0,013 | 0,600 ± 0,044 | 0,379 ± 0,010 | 0,751 ± 0,012 | 0,502 ± 0,023 | 2 | 0,7 |  |
| 5 | mediana_moda | onehot | sem | pca | subamostragem | 0,671 ± 0,016 | 0,516 ± 0,010 | 0,411 ± 0,014 | 0,694 ± 0,025 | 0,732 ± 0,015 | 0,459 ± 0,022 | 2 | 0,7 |  |
| 6 | mediana_moda | onehot | sem | pca | smote | 0,735 ± 0,016 | 0,538 ± 0,030 | 0,481 ± 0,025 | 0,610 ± 0,038 | 0,762 ± 0,017 | 0,520 ± 0,026 | 2 | 0,7 |  |
| 7 | mediana_moda | onehot | sem | kbest | sem | 0,820 ± 0,007 | 0,597 ± 0,020 | 0,687 ± 0,016 | 0,527 ± 0,026 | 0,813 ± 0,007 | 0,606 ± 0,008 | 10 | 3,4 |  |
| 8 | mediana_moda | onehot | sem | kbest | subamostragem | 0,766 ± 0,028 | 0,619 ± 0,033 | 0,527 ± 0,042 | 0,751 ± 0,031 | 0,812 ± 0,016 | 0,587 ± 0,020 | 10 | 3,3 |  |
| 9 | mediana_moda | onehot | sem | kbest | smote | 0,770 ± 0,012 | 0,612 ± 0,016 | 0,533 ± 0,018 | 0,717 ± 0,012 | 0,809 ± 0,010 | 0,573 ± 0,024 | 10 | 3,4 |  |
| 10 | mediana_moda | onehot | padrao | sem | sem | 0,833 ± 0,009 | 0,639 ± 0,020 | 0,703 ± 0,024 | 0,587 ± 0,027 | 0,833 ± 0,020 | 0,632 ± 0,007 | 76 | 0,7 |  |
| 11 | mediana_moda | onehot | padrao | sem | subamostragem | 0,796 ± 0,005 | 0,650 ± 0,017 | 0,574 ± 0,006 | 0,751 ± 0,039 | 0,836 ± 0,016 | 0,629 ± 0,010 | 76 | 0,7 |  |
| 12 | mediana_moda | onehot | padrao | sem | smote | 0,779 ± 0,009 | 0,635 ± 0,010 | 0,545 ± 0,013 | 0,761 ± 0,022 | 0,827 ± 0,018 | 0,600 ± 0,022 | 76 | 0,8 |  |
| 13 | mediana_moda | onehot | padrao | pca | sem | 0,837 ± 0,008 | 0,650 ± 0,026 | 0,712 ± 0,012 | 0,598 ± 0,040 | 0,830 ± 0,019 | 0,636 ± 0,015 | 59 | 2,1 |  |
| 14 | mediana_moda | onehot | padrao | pca | subamostragem | 0,790 ± 0,004 | 0,647 ± 0,013 | 0,563 ± 0,007 | 0,763 ± 0,035 | 0,835 ± 0,016 | 0,632 ± 0,015 | 59 | 2,4 |  |
| 15 | mediana_moda | onehot | padrao | pca | smote | 0,778 ± 0,012 | 0,636 ± 0,018 | 0,542 ± 0,016 | 0,771 ± 0,029 | 0,825 ± 0,018 | 0,602 ± 0,023 | 59 | 3,0 |  |
| 16 | mediana_moda | onehot | padrao | kbest | sem | 0,821 ± 0,012 | 0,609 ± 0,016 | 0,683 ± 0,042 | 0,550 ± 0,016 | 0,820 ± 0,016 | 0,623 ± 0,029 | 10 | 3,6 |  |
| 17 | mediana_moda | onehot | padrao | kbest | subamostragem | 0,796 ± 0,025 | 0,652 ± 0,028 | 0,575 ± 0,040 | 0,754 ± 0,016 | 0,828 ± 0,017 | 0,619 ± 0,028 | 10 | 3,6 |  |
| 18 | mediana_moda | onehot | padrao | kbest | smote | 0,780 ± 0,017 | 0,619 ± 0,020 | 0,551 ± 0,028 | 0,706 ± 0,021 | 0,807 ± 0,016 | 0,575 ± 0,020 | 10 | 3,5 |  |
| 19 | mediana_moda | onehot | minmax | sem | sem | 0,832 ± 0,011 | 0,640 ± 0,029 | 0,699 ± 0,020 | 0,590 ± 0,039 | 0,832 ± 0,015 | 0,638 ± 0,016 | 76 | 0,7 |  |
| 20 | mediana_moda | onehot | minmax | sem | subamostragem | 0,766 ± 0,010 | 0,622 ± 0,014 | 0,526 ± 0,014 | 0,763 ± 0,028 | 0,826 ± 0,014 | 0,604 ± 0,023 | 76 | 0,7 |  |
| 21 | mediana_moda | onehot | minmax | sem | smote | 0,721 ± 0,017 | 0,586 ± 0,015 | 0,470 ± 0,020 | 0,780 ± 0,025 | 0,805 ± 0,003 | 0,559 ± 0,019 | 76 | 0,9 |  |
| 22 | mediana_moda | onehot | minmax | pca | sem | 0,830 ± 0,011 | 0,614 ± 0,031 | 0,720 ± 0,029 | 0,535 ± 0,036 | 0,824 ± 0,016 | 0,629 ± 0,024 | 41 | 2,5 |  |
| 23 | mediana_moda | onehot | minmax | pca | subamostragem | 0,756 ± 0,013 | 0,607 ± 0,015 | 0,513 ± 0,018 | 0,745 ± 0,025 | 0,815 ± 0,014 | 0,585 ± 0,020 | 41 | 3,1 |  |
| 24 | mediana_moda | onehot | minmax | pca | smote | 0,751 ± 0,013 | 0,601 ± 0,020 | 0,506 ± 0,018 | 0,742 ± 0,043 | 0,810 ± 0,008 | 0,572 ± 0,020 | 41 | 3,0 |  |
| 25 | mediana_moda | onehot | minmax | kbest | sem | 0,824 ± 0,009 | 0,613 ± 0,013 | 0,693 ± 0,035 | 0,550 ± 0,018 | 0,820 ± 0,015 | 0,619 ± 0,017 | 10 | 3,5 |  |
| 26 | mediana_moda | onehot | minmax | kbest | subamostragem | 0,793 ± 0,024 | 0,642 ± 0,028 | 0,574 ± 0,042 | 0,729 ± 0,011 | 0,825 ± 0,017 | 0,617 ± 0,026 | 10 | 3,4 |  |
| 27 | mediana_moda | onehot | minmax | kbest | smote | 0,780 ± 0,017 | 0,622 ± 0,023 | 0,550 ± 0,028 | 0,716 ± 0,026 | 0,809 ± 0,016 | 0,575 ± 0,015 | 10 | 3,6 |  |
| 28 | mediana_moda | onehot | robusto | sem | sem | 0,829 ± 0,011 | 0,622 ± 0,019 | 0,704 ± 0,044 | 0,560 ± 0,031 | 0,835 ± 0,014 | 0,632 ± 0,027 | 76 | 0,8 |  |
| 29 | mediana_moda | onehot | robusto | sem | subamostragem | 0,781 ± 0,019 | 0,641 ± 0,023 | 0,547 ± 0,030 | 0,775 ± 0,020 | 0,837 ± 0,020 | 0,610 ± 0,034 | 76 | 0,8 |  |
| 30 | mediana_moda | onehot | robusto | sem | smote | 0,752 ± 0,014 | 0,613 ± 0,014 | 0,506 ± 0,017 | 0,777 ± 0,023 | 0,814 ± 0,013 | 0,569 ± 0,036 | 76 | 0,9 |  |
| 31 | mediana_moda | onehot | robusto | pca | sem | 0,819 ± 0,010 | 0,601 ± 0,034 | 0,677 ± 0,022 | 0,543 ± 0,053 | 0,826 ± 0,011 | 0,624 ± 0,014 | 20 | 2,1 |  |
| 32 | mediana_moda | onehot | robusto | pca | subamostragem | 0,778 ± 0,016 | 0,636 ± 0,021 | 0,543 ± 0,024 | 0,768 ± 0,027 | 0,832 ± 0,018 | 0,602 ± 0,023 | 20 | 2,4 |  |
| 33 | mediana_moda | onehot | robusto | pca | smote | 0,764 ± 0,014 | 0,624 ± 0,014 | 0,523 ± 0,021 | 0,774 ± 0,014 | 0,818 ± 0,009 | 0,573 ± 0,014 | 20 | 2,4 |  |
| 34 | mediana_moda | onehot | robusto | kbest | sem | 0,822 ± 0,013 | 0,615 ± 0,027 | 0,679 ± 0,035 | 0,563 ± 0,036 | 0,824 ± 0,016 | 0,625 ± 0,019 | 10 | 3,5 |  |
| 35 | mediana_moda | onehot | robusto | kbest | subamostragem | 0,787 ± 0,026 | 0,636 ± 0,032 | 0,563 ± 0,043 | 0,732 ± 0,031 | 0,823 ± 0,020 | 0,600 ± 0,027 | 10 | 3,6 |  |
| 36 | mediana_moda | onehot | robusto | kbest | smote | 0,778 ± 0,018 | 0,623 ± 0,023 | 0,546 ± 0,028 | 0,726 ± 0,030 | 0,811 ± 0,019 | 0,580 ± 0,027 | 10 | 3,6 |  |
| 37 | mediana_moda | alvo | sem | sem | sem | 0,807 ± 0,012 | 0,532 ± 0,033 | 0,685 ± 0,044 | 0,436 ± 0,037 | 0,821 ± 0,017 | 0,578 ± 0,029 | 18 | 0,8 |  |
| 38 | mediana_moda | alvo | sem | sem | subamostragem | 0,745 ± 0,028 | 0,584 ± 0,035 | 0,497 ± 0,037 | 0,708 ± 0,034 | 0,800 ± 0,027 | 0,528 ± 0,030 | 18 | 0,6 |  |
| 39 | mediana_moda | alvo | sem | sem | smote | 0,763 ± 0,013 | 0,609 ± 0,027 | 0,522 ± 0,017 | 0,731 ± 0,051 | 0,817 ± 0,016 | 0,569 ± 0,033 | 18 | 0,8 |  |
| 40 | mediana_moda | alvo | sem | pca | sem | 0,781 ± 0,015 | 0,470 ± 0,023 | 0,609 ± 0,054 | 0,384 ± 0,012 | 0,752 ± 0,014 | 0,510 ± 0,025 | 2 | 0,6 |  |
| 41 | mediana_moda | alvo | sem | pca | subamostragem | 0,670 ± 0,013 | 0,515 ± 0,012 | 0,410 ± 0,013 | 0,693 ± 0,023 | 0,733 ± 0,015 | 0,461 ± 0,024 | 2 | 0,7 |  |
| 42 | mediana_moda | alvo | sem | pca | smote | 0,738 ± 0,014 | 0,547 ± 0,028 | 0,486 ± 0,023 | 0,625 ± 0,038 | 0,763 ± 0,013 | 0,525 ± 0,023 | 2 | 0,6 |  |
| 43 | mediana_moda | alvo | sem | kbest | sem | 0,816 ± 0,006 | 0,580 ± 0,020 | 0,686 ± 0,018 | 0,503 ± 0,030 | 0,803 ± 0,012 | 0,584 ± 0,013 | 10 | 1,3 |  |
| 44 | mediana_moda | alvo | sem | kbest | subamostragem | 0,770 ± 0,024 | 0,609 ± 0,033 | 0,535 ± 0,039 | 0,708 ± 0,032 | 0,805 ± 0,018 | 0,587 ± 0,019 | 10 | 1,3 |  |
| 45 | mediana_moda | alvo | sem | kbest | smote | 0,768 ± 0,017 | 0,604 ± 0,014 | 0,532 ± 0,030 | 0,702 ± 0,042 | 0,797 ± 0,016 | 0,555 ± 0,018 | 10 | 1,3 |  |
| 46 | mediana_moda | alvo | padrao | sem | sem | 0,841 ± 0,012 | 0,659 ± 0,025 | 0,721 ± 0,042 | 0,609 ± 0,041 | 0,835 ± 0,009 | 0,648 ± 0,017 | 18 | 0,7 |  |
| 47 | mediana_moda | alvo | padrao | sem | subamostragem | 0,796 ± 0,018 | 0,650 ± 0,027 | 0,575 ± 0,028 | 0,748 ± 0,035 | 0,848 ± 0,017 | 0,649 ± 0,026 | 18 | 0,7 |  |
| 48 | mediana_moda | alvo | padrao | sem | smote | 0,778 ± 0,008 | 0,632 ± 0,008 | 0,544 ± 0,013 | 0,755 ± 0,027 | 0,824 ± 0,008 | 0,596 ± 0,017 | 18 | 0,7 |  |
| 49 | mediana_moda | alvo | padrao | pca | sem | 0,841 ± 0,010 | 0,661 ± 0,023 | 0,718 ± 0,037 | 0,615 ± 0,040 | 0,841 ± 0,015 | 0,651 ± 0,016 | 12 | 0,8 |  |
| 50 | mediana_moda | alvo | padrao | pca | subamostragem | 0,794 ± 0,015 | 0,652 ± 0,021 | 0,570 ± 0,024 | 0,763 ± 0,029 | 0,853 ± 0,016 | 0,652 ± 0,025 | 12 | 0,8 |  |
| 51 | mediana_moda | alvo | padrao | pca | smote | 0,776 ± 0,016 | 0,628 ± 0,016 | 0,542 ± 0,026 | 0,749 ± 0,035 | 0,831 ± 0,008 | 0,605 ± 0,019 | 12 | 1,0 |  |
| 52 | mediana_moda | alvo | padrao | kbest | sem | 0,843 ± 0,010 | 0,668 ± 0,019 | 0,719 ± 0,028 | 0,624 ± 0,023 | 0,829 ± 0,010 | 0,648 ± 0,022 | 10 | 1,5 |  |
| 53 | mediana_moda | alvo | padrao | kbest | subamostragem | 0,804 ± 0,015 | 0,657 ± 0,016 | 0,590 ± 0,030 | 0,743 ± 0,016 | 0,836 ± 0,008 | 0,638 ± 0,024 | 10 | 1,3 |  |
| 54 | mediana_moda | alvo | padrao | kbest | smote | 0,778 ± 0,016 | 0,626 ± 0,012 | 0,547 ± 0,030 | 0,735 ± 0,020 | 0,816 ± 0,018 | 0,597 ± 0,035 | 10 | 1,6 |  |
| 55 | mediana_moda | alvo | minmax | sem | sem | 0,839 ± 0,011 | 0,645 ± 0,029 | 0,725 ± 0,027 | 0,581 ± 0,035 | 0,848 ± 0,014 | 0,649 ± 0,026 | 18 | 0,7 |  |
| 56 | mediana_moda | alvo | minmax | sem | subamostragem | 0,797 ± 0,009 | 0,648 ± 0,011 | 0,577 ± 0,016 | 0,739 ± 0,011 | 0,846 ± 0,013 | 0,641 ± 0,022 | 18 | 0,6 |  |
| 57 | mediana_moda | alvo | minmax | sem | smote | 0,785 ± 0,012 | 0,642 ± 0,011 | 0,555 ± 0,019 | 0,761 ± 0,014 | 0,839 ± 0,013 | 0,612 ± 0,033 | 18 | 0,7 |  |
| 58 | mediana_moda | alvo | minmax | pca | sem | 0,839 ± 0,009 | 0,654 ± 0,022 | 0,716 ± 0,024 | 0,602 ± 0,030 | 0,850 ± 0,010 | 0,642 ± 0,021 | 9 | 0,7 |  |
| 59 | mediana_moda | alvo | minmax | pca | subamostragem | 0,791 ± 0,010 | 0,646 ± 0,015 | 0,564 ± 0,015 | 0,755 ± 0,028 | 0,843 ± 0,017 | 0,627 ± 0,018 | 9 | 0,7 |  |
| 60 | mediana_moda | alvo | minmax | pca | smote | 0,788 ± 0,011 | 0,642 ± 0,009 | 0,561 ± 0,020 | 0,752 ± 0,015 | 0,842 ± 0,011 | 0,624 ± 0,026 | 9 | 0,7 |  |
| 61 | mediana_moda | alvo | minmax | kbest | sem | 0,845 ± 0,008 | 0,664 ± 0,013 | 0,737 ± 0,034 | 0,606 ± 0,025 | 0,834 ± 0,004 | 0,652 ± 0,018 | 10 | 1,4 |  |
| 62 | mediana_moda | alvo | minmax | kbest | subamostragem | 0,806 ± 0,014 | 0,655 ± 0,018 | 0,596 ± 0,029 | 0,726 ± 0,019 | 0,838 ± 0,009 | 0,644 ± 0,014 | 10 | 1,3 |  |
| 63 | mediana_moda | alvo | minmax | kbest | smote | 0,793 ± 0,019 | 0,647 ± 0,020 | 0,570 ± 0,035 | 0,749 ± 0,015 | 0,829 ± 0,011 | 0,613 ± 0,030 | 10 | 1,4 |  |
| 64 | mediana_moda | alvo | robusto | sem | sem | 0,830 ± 0,005 | 0,632 ± 0,014 | 0,697 ± 0,026 | 0,580 ± 0,033 | 0,836 ± 0,013 | 0,636 ± 0,018 | 18 | 0,7 |  |
| 65 | mediana_moda | alvo | robusto | sem | subamostragem | 0,802 ± 0,009 | 0,657 ± 0,012 | 0,583 ± 0,017 | 0,751 ± 0,011 | 0,842 ± 0,012 | 0,626 ± 0,020 | 18 | 0,6 |  |
| 66 | mediana_moda | alvo | robusto | sem | smote | 0,771 ± 0,010 | 0,627 ± 0,008 | 0,533 ± 0,016 | 0,763 ± 0,022 | 0,823 ± 0,010 | 0,590 ± 0,026 | 18 | 0,8 |  |
| 67 | mediana_moda | alvo | robusto | pca | sem | 0,834 ± 0,009 | 0,642 ± 0,027 | 0,707 ± 0,025 | 0,590 ± 0,049 | 0,835 ± 0,011 | 0,636 ± 0,023 | 10 | 0,8 |  |
| 68 | mediana_moda | alvo | robusto | pca | subamostragem | 0,793 ± 0,016 | 0,643 ± 0,017 | 0,570 ± 0,031 | 0,739 ± 0,022 | 0,835 ± 0,018 | 0,616 ± 0,024 | 10 | 0,8 |  |
| 69 | mediana_moda | alvo | robusto | pca | smote | 0,785 ± 0,013 | 0,641 ± 0,020 | 0,555 ± 0,019 | 0,758 ± 0,036 | 0,824 ± 0,007 | 0,593 ± 0,016 | 10 | 0,8 |  |
| 70 | mediana_moda | alvo | robusto | kbest | sem | 0,835 ± 0,010 | 0,650 ± 0,023 | 0,700 ± 0,026 | 0,607 ± 0,033 | 0,830 ± 0,012 | 0,632 ± 0,032 | 10 | 1,4 |  |
| 71 | mediana_moda | alvo | robusto | kbest | subamostragem | 0,791 ± 0,020 | 0,643 ± 0,023 | 0,566 ± 0,035 | 0,746 ± 0,019 | 0,834 ± 0,010 | 0,620 ± 0,030 | 10 | 1,4 |  |
| 72 | mediana_moda | alvo | robusto | kbest | smote | 0,770 ± 0,032 | 0,623 ± 0,034 | 0,535 ± 0,047 | 0,746 ± 0,011 | 0,818 ± 0,017 | 0,588 ± 0,035 | 10 | 1,6 |  |
| 73 | mediana_indicadora | onehot | sem | sem | sem | 0,806 ± 0,013 | 0,539 ± 0,039 | 0,672 ± 0,035 | 0,451 ± 0,043 | 0,826 ± 0,013 | 0,583 ± 0,022 | 84 | 0,8 |  |
| 74 | mediana_indicadora | onehot | sem | sem | subamostragem | 0,738 ± 0,025 | 0,583 ± 0,031 | 0,488 ± 0,031 | 0,725 ± 0,033 | 0,804 ± 0,027 | 0,537 ± 0,021 | 84 | 0,8 |  |
| 75 | mediana_indicadora | onehot | sem | sem | smote | 0,749 ± 0,012 | 0,605 ± 0,014 | 0,503 ± 0,016 | 0,758 ± 0,024 | 0,818 ± 0,011 | 0,568 ± 0,025 | 84 | 0,9 |  |
| 76 | mediana_indicadora | onehot | sem | pca | sem | 0,781 ± 0,012 | 0,465 ± 0,011 | 0,613 ± 0,050 | 0,376 ± 0,009 | 0,750 ± 0,016 | 0,503 ± 0,023 | 2 | 0,8 |  |
| 77 | mediana_indicadora | onehot | sem | pca | subamostragem | 0,670 ± 0,017 | 0,515 ± 0,011 | 0,410 ± 0,014 | 0,694 ± 0,025 | 0,731 ± 0,015 | 0,459 ± 0,024 | 2 | 0,8 |  |
| 78 | mediana_indicadora | onehot | sem | pca | smote | 0,736 ± 0,018 | 0,539 ± 0,032 | 0,482 ± 0,028 | 0,612 ± 0,040 | 0,762 ± 0,017 | 0,524 ± 0,027 | 2 | 0,8 |  |
| 79 | mediana_indicadora | onehot | sem | kbest | sem | 0,827 ± 0,015 | 0,612 ± 0,037 | 0,706 ± 0,036 | 0,541 ± 0,046 | 0,814 ± 0,013 | 0,610 ± 0,024 | 10 | 3,7 |  |
| 80 | mediana_indicadora | onehot | sem | kbest | subamostragem | 0,772 ± 0,027 | 0,624 ± 0,031 | 0,537 ± 0,041 | 0,746 ± 0,030 | 0,813 ± 0,018 | 0,591 ± 0,021 | 10 | 3,6 |  |
| 81 | mediana_indicadora | onehot | sem | kbest | smote | 0,776 ± 0,023 | 0,615 ± 0,025 | 0,545 ± 0,036 | 0,706 ± 0,010 | 0,812 ± 0,013 | 0,581 ± 0,008 | 10 | 3,8 |  |
| 82 | mediana_indicadora | onehot | padrao | sem | sem | 0,833 ± 0,008 | 0,642 ± 0,015 | 0,701 ± 0,027 | 0,593 ± 0,023 | 0,833 ± 0,019 | 0,633 ± 0,007 | 84 | 0,8 |  |
| 83 | mediana_indicadora | onehot | padrao | sem | subamostragem | 0,795 ± 0,006 | 0,648 ± 0,016 | 0,571 ± 0,007 | 0,751 ± 0,036 | 0,837 ± 0,013 | 0,628 ± 0,011 | 84 | 0,7 |  |
| 84 | mediana_indicadora | onehot | padrao | sem | smote | 0,769 ± 0,024 | 0,626 ± 0,024 | 0,531 ± 0,033 | 0,763 ± 0,025 | 0,825 ± 0,016 | 0,597 ± 0,019 | 84 | 0,8 |  |
| 85 | mediana_indicadora | onehot | padrao | pca | sem | 0,832 ± 0,005 | 0,642 ± 0,016 | 0,696 ± 0,022 | 0,598 ± 0,035 | 0,827 ± 0,022 | 0,626 ± 0,007 | 61 | 2,9 |  |
| 86 | mediana_indicadora | onehot | padrao | pca | subamostragem | 0,785 ± 0,012 | 0,640 ± 0,019 | 0,555 ± 0,017 | 0,757 ± 0,031 | 0,833 ± 0,015 | 0,623 ± 0,015 | 61 | 2,2 |  |
| 87 | mediana_indicadora | onehot | padrao | pca | smote | 0,766 ± 0,021 | 0,617 ± 0,025 | 0,528 ± 0,029 | 0,745 ± 0,035 | 0,820 ± 0,020 | 0,597 ± 0,026 | 61 | 3,3 |  |
| 88 | mediana_indicadora | onehot | padrao | kbest | sem | 0,827 ± 0,007 | 0,627 ± 0,015 | 0,692 ± 0,032 | 0,575 ± 0,032 | 0,824 ± 0,010 | 0,625 ± 0,022 | 10 | 3,9 |  |
| 89 | mediana_indicadora | onehot | padrao | kbest | subamostragem | 0,799 ± 0,016 | 0,651 ± 0,022 | 0,580 ± 0,026 | 0,743 ± 0,034 | 0,828 ± 0,018 | 0,620 ± 0,033 | 10 | 3,9 |  |
| 90 | mediana_indicadora | onehot | padrao | kbest | smote | 0,779 ± 0,014 | 0,622 ± 0,013 | 0,548 ± 0,024 | 0,719 ± 0,023 | 0,812 ± 0,009 | 0,574 ± 0,024 | 10 | 3,9 |  |
| 91 | mediana_indicadora | onehot | minmax | sem | sem | 0,825 ± 0,004 | 0,624 ± 0,012 | 0,681 ± 0,010 | 0,576 ± 0,022 | 0,823 ± 0,024 | 0,617 ± 0,026 | 84 | 0,7 |  |
| 92 | mediana_indicadora | onehot | minmax | sem | subamostragem | 0,754 ± 0,018 | 0,611 ± 0,029 | 0,509 ± 0,023 | 0,765 ± 0,039 | 0,818 ± 0,018 | 0,584 ± 0,028 | 84 | 0,7 |  |
| 93 | mediana_indicadora | onehot | minmax | sem | smote | 0,724 ± 0,017 | 0,587 ± 0,026 | 0,471 ± 0,020 | 0,778 ± 0,046 | 0,804 ± 0,021 | 0,561 ± 0,025 | 84 | 0,8 |  |
| 94 | mediana_indicadora | onehot | minmax | pca | sem | 0,819 ± 0,015 | 0,591 ± 0,030 | 0,687 ± 0,043 | 0,518 ± 0,028 | 0,809 ± 0,020 | 0,596 ± 0,032 | 41 | 2,7 |  |
| 95 | mediana_indicadora | onehot | minmax | pca | subamostragem | 0,747 ± 0,017 | 0,603 ± 0,023 | 0,500 ± 0,021 | 0,762 ± 0,032 | 0,812 ± 0,020 | 0,571 ± 0,021 | 41 | 2,2 |  |
| 96 | mediana_indicadora | onehot | minmax | pca | smote | 0,737 ± 0,019 | 0,591 ± 0,033 | 0,486 ± 0,023 | 0,752 ± 0,054 | 0,799 ± 0,021 | 0,562 ± 0,024 | 41 | 2,6 |  |
| 97 | mediana_indicadora | onehot | minmax | kbest | sem | 0,822 ± 0,005 | 0,607 ± 0,024 | 0,686 ± 0,019 | 0,546 ± 0,042 | 0,825 ± 0,013 | 0,621 ± 0,031 | 10 | 3,8 |  |
| 98 | mediana_indicadora | onehot | minmax | kbest | subamostragem | 0,799 ± 0,019 | 0,646 ± 0,028 | 0,582 ± 0,031 | 0,728 ± 0,035 | 0,827 ± 0,021 | 0,614 ± 0,037 | 10 | 3,6 |  |
| 99 | mediana_indicadora | onehot | minmax | kbest | smote | 0,778 ± 0,018 | 0,621 ± 0,020 | 0,548 ± 0,030 | 0,719 ± 0,022 | 0,813 ± 0,007 | 0,578 ± 0,024 | 10 | 4,0 |  |
| 100 | mediana_indicadora | onehot | robusto | sem | sem | 0,827 ± 0,011 | 0,624 ± 0,019 | 0,695 ± 0,040 | 0,567 ± 0,028 | 0,838 ± 0,016 | 0,632 ± 0,029 | 84 | 0,8 |  |
| 101 | mediana_indicadora | onehot | robusto | sem | subamostragem | 0,777 ± 0,020 | 0,639 ± 0,026 | 0,541 ± 0,028 | 0,780 ± 0,021 | 0,835 ± 0,018 | 0,607 ± 0,031 | 84 | 0,8 |  |
| 102 | mediana_indicadora | onehot | robusto | sem | smote | 0,747 ± 0,013 | 0,611 ± 0,018 | 0,500 ± 0,016 | 0,786 ± 0,028 | 0,821 ± 0,014 | 0,574 ± 0,032 | 84 | 0,9 |  |
| 103 | mediana_indicadora | onehot | robusto | pca | sem | 0,818 ± 0,012 | 0,600 ± 0,032 | 0,676 ± 0,033 | 0,541 ± 0,048 | 0,830 ± 0,009 | 0,616 ± 0,021 | 22 | 2,8 |  |
| 104 | mediana_indicadora | onehot | robusto | pca | subamostragem | 0,771 ± 0,018 | 0,630 ± 0,022 | 0,534 ± 0,025 | 0,769 ± 0,028 | 0,830 ± 0,019 | 0,604 ± 0,029 | 22 | 2,7 |  |
| 105 | mediana_indicadora | onehot | robusto | pca | smote | 0,761 ± 0,017 | 0,621 ± 0,018 | 0,519 ± 0,022 | 0,775 ± 0,014 | 0,818 ± 0,011 | 0,567 ± 0,021 | 22 | 3,0 |  |
| 106 | mediana_indicadora | onehot | robusto | kbest | sem | 0,825 ± 0,006 | 0,622 ± 0,028 | 0,684 ± 0,008 | 0,572 ± 0,051 | 0,822 ± 0,014 | 0,630 ± 0,029 | 10 | 3,9 |  |
| 107 | mediana_indicadora | onehot | robusto | kbest | subamostragem | 0,784 ± 0,021 | 0,631 ± 0,022 | 0,557 ± 0,035 | 0,729 ± 0,022 | 0,821 ± 0,015 | 0,607 ± 0,033 | 10 | 3,7 |  |
| 108 | mediana_indicadora | onehot | robusto | kbest | smote | 0,778 ± 0,019 | 0,623 ± 0,020 | 0,547 ± 0,032 | 0,725 ± 0,030 | 0,813 ± 0,011 | 0,580 ± 0,025 | 10 | 3,9 |  |
| 109 | mediana_indicadora | alvo | sem | sem | sem | 0,803 ± 0,009 | 0,518 ± 0,030 | 0,677 ± 0,032 | 0,420 ± 0,037 | 0,816 ± 0,015 | 0,570 ± 0,026 | 25 | 0,7 |  |
| 110 | mediana_indicadora | alvo | sem | sem | subamostragem | 0,746 ± 0,030 | 0,586 ± 0,039 | 0,499 ± 0,039 | 0,711 ± 0,038 | 0,800 ± 0,028 | 0,528 ± 0,030 | 25 | 0,7 |  |
| 111 | mediana_indicadora | alvo | sem | sem | smote | 0,761 ± 0,012 | 0,605 ± 0,023 | 0,519 ± 0,016 | 0,728 ± 0,044 | 0,815 ± 0,013 | 0,569 ± 0,027 | 25 | 0,8 |  |
| 112 | mediana_indicadora | alvo | sem | pca | sem | 0,783 ± 0,016 | 0,471 ± 0,022 | 0,615 ± 0,062 | 0,382 ± 0,010 | 0,753 ± 0,014 | 0,509 ± 0,027 | 2 | 0,6 |  |
| 113 | mediana_indicadora | alvo | sem | pca | subamostragem | 0,670 ± 0,013 | 0,514 ± 0,012 | 0,410 ± 0,012 | 0,690 ± 0,028 | 0,732 ± 0,016 | 0,460 ± 0,025 | 2 | 0,6 |  |
| 114 | mediana_indicadora | alvo | sem | pca | smote | 0,741 ± 0,015 | 0,550 ± 0,027 | 0,490 ± 0,023 | 0,625 ± 0,036 | 0,768 ± 0,012 | 0,531 ± 0,021 | 2 | 0,7 |  |
| 115 | mediana_indicadora | alvo | sem | kbest | sem | 0,817 ± 0,005 | 0,582 ± 0,022 | 0,686 ± 0,016 | 0,506 ± 0,035 | 0,804 ± 0,013 | 0,592 ± 0,018 | 10 | 1,6 |  |
| 116 | mediana_indicadora | alvo | sem | kbest | subamostragem | 0,769 ± 0,023 | 0,610 ± 0,033 | 0,534 ± 0,037 | 0,714 ± 0,035 | 0,806 ± 0,020 | 0,590 ± 0,019 | 10 | 1,5 |  |
| 117 | mediana_indicadora | alvo | sem | kbest | smote | 0,765 ± 0,030 | 0,603 ± 0,026 | 0,531 ± 0,045 | 0,702 ± 0,031 | 0,799 ± 0,018 | 0,561 ± 0,011 | 10 | 1,7 |  |
| 118 | mediana_indicadora | alvo | padrao | sem | sem | 0,840 ± 0,005 | 0,656 ± 0,018 | 0,717 ± 0,022 | 0,607 ± 0,039 | 0,835 ± 0,011 | 0,647 ± 0,021 | 25 | 0,7 |  |
| 119 | mediana_indicadora | alvo | padrao | sem | subamostragem | 0,805 ± 0,013 | 0,663 ± 0,018 | 0,589 ± 0,022 | 0,758 ± 0,023 | 0,846 ± 0,016 | 0,646 ± 0,010 | 25 | 0,9 |  |
| 120 | mediana_indicadora | alvo | padrao | sem | smote | 0,772 ± 0,014 | 0,623 ± 0,009 | 0,536 ± 0,023 | 0,746 ± 0,023 | 0,825 ± 0,009 | 0,602 ± 0,021 | 25 | 0,8 |  |
| 121 | mediana_indicadora | alvo | padrao | pca | sem | 0,838 ± 0,003 | 0,648 ± 0,011 | 0,720 ± 0,017 | 0,590 ± 0,026 | 0,837 ± 0,010 | 0,648 ± 0,021 | 14 | 1,1 |  |
| 122 | mediana_indicadora | alvo | padrao | pca | subamostragem | 0,798 ± 0,016 | 0,655 ± 0,023 | 0,577 ± 0,025 | 0,758 ± 0,024 | 0,847 ± 0,016 | 0,654 ± 0,009 | 14 | 0,9 |  |
| 123 | mediana_indicadora | alvo | padrao | pca | smote | 0,778 ± 0,016 | 0,634 ± 0,021 | 0,545 ± 0,025 | 0,760 ± 0,044 | 0,827 ± 0,009 | 0,608 ± 0,027 | 14 | 1,1 |  |
| 124 | mediana_indicadora | alvo | padrao | kbest | sem | 0,835 ± 0,008 | 0,648 ± 0,025 | 0,701 ± 0,019 | 0,602 ± 0,040 | 0,834 ± 0,009 | 0,651 ± 0,016 | 10 | 1,7 |  |
| 125 | mediana_indicadora | alvo | padrao | kbest | subamostragem | 0,808 ± 0,015 | 0,662 ± 0,014 | 0,599 ± 0,030 | 0,740 ± 0,018 | 0,838 ± 0,008 | 0,631 ± 0,018 | 10 | 1,6 |  |
| 126 | mediana_indicadora | alvo | padrao | kbest | smote | 0,781 ± 0,023 | 0,631 ± 0,021 | 0,552 ± 0,040 | 0,740 ± 0,015 | 0,821 ± 0,018 | 0,600 ± 0,035 | 10 | 1,8 |  |
| 127 | mediana_indicadora | alvo | minmax | sem | sem | 0,841 ± 0,004 | 0,648 ± 0,017 | 0,736 ± 0,008 | 0,580 ± 0,028 | 0,833 ± 0,011 | 0,640 ± 0,018 | 25 | 0,7 |  |
| 128 | mediana_indicadora | alvo | minmax | sem | subamostragem | 0,787 ± 0,010 | 0,640 ± 0,017 | 0,558 ± 0,014 | 0,751 ± 0,025 | 0,832 ± 0,013 | 0,616 ± 0,016 | 25 | 0,7 |  |
| 129 | mediana_indicadora | alvo | minmax | sem | smote | 0,782 ± 0,014 | 0,631 ± 0,020 | 0,551 ± 0,023 | 0,740 ± 0,037 | 0,825 ± 0,013 | 0,605 ± 0,027 | 25 | 0,7 |  |
| 130 | mediana_indicadora | alvo | minmax | pca | sem | 0,836 ± 0,008 | 0,638 ± 0,023 | 0,718 ± 0,019 | 0,575 ± 0,035 | 0,835 ± 0,013 | 0,634 ± 0,031 | 10 | 0,7 |  |
| 131 | mediana_indicadora | alvo | minmax | pca | subamostragem | 0,780 ± 0,012 | 0,630 ± 0,016 | 0,548 ± 0,018 | 0,743 ± 0,019 | 0,827 ± 0,013 | 0,605 ± 0,017 | 10 | 0,7 |  |
| 132 | mediana_indicadora | alvo | minmax | pca | smote | 0,791 ± 0,019 | 0,640 ± 0,023 | 0,568 ± 0,032 | 0,734 ± 0,024 | 0,828 ± 0,018 | 0,608 ± 0,036 | 10 | 0,8 |  |
| 133 | mediana_indicadora | alvo | minmax | kbest | sem | 0,838 ± 0,001 | 0,648 ± 0,014 | 0,719 ± 0,019 | 0,592 ± 0,033 | 0,839 ± 0,008 | 0,664 ± 0,025 | 10 | 1,7 |  |
| 134 | mediana_indicadora | alvo | minmax | kbest | subamostragem | 0,813 ± 0,009 | 0,663 ± 0,013 | 0,609 ± 0,018 | 0,729 ± 0,022 | 0,843 ± 0,007 | 0,644 ± 0,015 | 10 | 1,6 |  |
| 135 | mediana_indicadora | alvo | minmax | kbest | smote | 0,798 ± 0,015 | 0,653 ± 0,015 | 0,578 ± 0,026 | 0,751 ± 0,022 | 0,831 ± 0,012 | 0,618 ± 0,031 | 10 | 1,7 |  |
| 136 | mediana_indicadora | alvo | robusto | sem | sem | 0,839 ± 0,006 | 0,650 ± 0,023 | 0,721 ± 0,019 | 0,593 ± 0,044 | 0,837 ± 0,017 | 0,639 ± 0,025 | 25 | 0,7 |  |
| 137 | mediana_indicadora | alvo | robusto | sem | subamostragem | 0,799 ± 0,007 | 0,657 ± 0,011 | 0,577 ± 0,012 | 0,762 ± 0,021 | 0,841 ± 0,015 | 0,625 ± 0,021 | 25 | 0,7 |  |
| 138 | mediana_indicadora | alvo | robusto | sem | smote | 0,770 ± 0,015 | 0,628 ± 0,016 | 0,531 ± 0,023 | 0,769 ± 0,021 | 0,821 ± 0,012 | 0,583 ± 0,025 | 25 | 0,8 |  |
| 139 | mediana_indicadora | alvo | robusto | pca | sem | 0,832 ± 0,009 | 0,644 ± 0,019 | 0,695 ± 0,027 | 0,601 ± 0,027 | 0,833 ± 0,013 | 0,630 ± 0,023 | 11 | 0,9 |  |
| 140 | mediana_indicadora | alvo | robusto | pca | subamostragem | 0,796 ± 0,005 | 0,649 ± 0,005 | 0,575 ± 0,012 | 0,746 ± 0,023 | 0,838 ± 0,017 | 0,622 ± 0,024 | 11 | 0,9 |  |
| 141 | mediana_indicadora | alvo | robusto | pca | smote | 0,770 ± 0,018 | 0,628 ± 0,019 | 0,532 ± 0,025 | 0,768 ± 0,033 | 0,823 ± 0,012 | 0,590 ± 0,013 | 11 | 1,0 |  |
| 142 | mediana_indicadora | alvo | robusto | kbest | sem | 0,830 ± 0,011 | 0,640 ± 0,023 | 0,690 ± 0,036 | 0,598 ± 0,032 | 0,829 ± 0,009 | 0,637 ± 0,028 | 10 | 1,8 |  |
| 143 | mediana_indicadora | alvo | robusto | kbest | subamostragem | 0,793 ± 0,020 | 0,645 ± 0,020 | 0,571 ± 0,034 | 0,743 ± 0,009 | 0,831 ± 0,007 | 0,618 ± 0,026 | 10 | 1,7 |  |
| 144 | mediana_indicadora | alvo | robusto | kbest | smote | 0,779 ± 0,019 | 0,630 ± 0,020 | 0,548 ± 0,030 | 0,743 ± 0,016 | 0,818 ± 0,015 | 0,588 ± 0,029 | 10 | 1,8 |  |

## B · Ambiente de execução

| item | valor |
|---|---|
| Python | 3.13.16 |
| scikit-learn | 1.9.1 |
| imbalanced-learn | 0.14.2 |
| pandas | 3.0.5 |
| numpy | 2.5.3 |
| sistema | Linux 6.18 |
| semente | 42 |
| validação | `StratifiedKFold` de 5 folds, embaralhado, semente 42 |
| vizinhos do kNN | 7 |

Gravado pela própria execução em `reports/e2/ambiente.json`. Executar a grade duas vezes neste
mesmo ambiente produz as mesmas métricas em todos os folds, o que confirma que nenhum
transformador ficou sem semente.

Uma observação de reprodutibilidade que vale registrar. A grade também foi executada num segundo
ambiente, Windows com Python 3.12 e scikit-learn 1.9.0. As conclusões não mudam: a melhor e a pior
combinação são as mesmas, o baseline fica na mesma faixa e todas as contagens pareadas da §5.2
mudam, no máximo, uma unidade. As métricas de corte, porém, diferem na terceira decimal, com
diferença máxima de 0,015 em precisão. A causa é a ordem de soma em ponto flutuante no cálculo das
distâncias, que desempata de forma diferente quando dois vizinhos estão à mesma distância do
filme avaliado. Os números deste relatório são todos do ambiente da tabela acima, que é o da
execução gravada no repositório, e o notebook entregue foi executado nele: refaz as 144
combinações e reproduz o `resultados.csv` com diferença máxima de 2 · 10⁻¹⁶.

## C · Partição em folds

O fold de cada um dos 2.590 filmes está em `reports/e2/folds.csv`, gerado uma única vez por
`python src/e2/base.py`. As 144 combinações e as três checagens de robustez recebem essa lista de
índices e não reconstroem a partição, de modo que qualquer diferença entre duas linhas da tabela
vem do pré-processamento e não da divisão dos dados.

## D · Arquivos gerados pela execução

| arquivo | conteúdo |
|---|---|
| `resultados.csv` | uma linha por combinação, com média e desvio de cada métrica |
| `resultados_por_fold.csv` | 720 linhas, uma por combinação e fold, base da leitura pareada |
| `folds.csv` | o fold de cada filme |
| `ambiente.json` | versões, semente, ordem das etapas e data da execução |
| `anexo_144.md` e `anexo_144.csv` | a tabela deste anexo |
| `analise_ranking.csv` | as 144 ordenadas, com as colunas de empate |
| `analise_efeitos.csv` | as duas leituras do efeito de cada etapa |
| `analise_interacoes.csv` | as tabelas de interação da §5.3 |
| `analise_custo_por_opcao.csv` e `analise_custo_mais_caras.csv` | a §5.4 |
| `robustez_temporal.csv`, `robustez_limiar.csv`, `robustez_limiar_spearman.csv`, `robustez_genero.csv` | as três checagens da §6 |

## E · Onde está cada coisa no código

| conteúdo | caminho |
|---|---|
| base, alvo e folds da E2 | `src/e2/base.py` |
| espaço das 144 combinações e montagem do pipeline | `src/e2/espaco.py` |
| uma etapa por módulo | `src/e2/etapas/` |
| métricas | `src/e2/metricas.py` |
| execução da grade | `src/executar_e2.py` |
| leitura dos resultados e regra de empate | `src/e2/analise.py` |
| robustez | `src/e2/robustez.py` |
| tabela deste anexo | `src/e2/anexo.py` |
| testes | `tests/test_e1.py` e `tests/test_e2.py` |

## F · Os 18 atributos e o que ficou fora

| grupo | colunas | n |
|---|---|---|
| numéricas | `ano`, `filmes_diretor_antes`, `filmes_distribuidora_antes`, `filmes_produtora_antes`, `coproducao`, `recebeu_fsa`, `recebeu_incentivo`, `contratos_fsa`, `projetos_incentivo` | 9 |
| numéricas de histórico | `hist_diretor`, `hist_distribuidora`, `hist_produtora` | 3 |
| nominais | `genero`, `uf_maj`, `distribuidora`, `origem_do_fomento` | 4 |
| ordinais | `experiencia_da_direcao`, `porte_da_distribuidora` | 2 |

Cada exclusão aplica uma decisão já tomada na E1:

| fora | motivo | origem |
|---|---|---|
| `publico`, `renda_*`, `max_salas`, `mediana_publico_do_ano`, `filmes_no_ano` | vazamento: só se conhecem depois da estreia | `build_dataset.COLUNAS_PROIBIDAS` |
| `cpb`, `titulo` | identificador | idem |
| `n_ufs` | moda em 97,1% dos filmes, efeito medido de 0,000 | H8 e S6 |
| `uf_bruto`, `uf2_bruto` | malformadas, substituídas por `uf_maj` | H6 e P7 |
| `direcao`, `produtora_maj`, `produtora_min` | 1.738, 1.502 e 714 categorias; o sinal entra pelos históricos | P5 |
| `decada`, `deflator`, `populacao_br` | função do `ano`; `populacao_br` tem 23% de falha de junção | P8 |
| `estreia_do_diretor` | redundante com `experiencia_da_direcao` | — |

## G · Tabelas de apoio da §5

Wilcoxon pareado sobre as diferenças por fold, contra a opção de referência, no mesmo contexto das
outras quatro etapas e no mesmo fold. Calculado no notebook da Entrega 2.

| afirmação | n | diferença média | p |
|---|---|---|---|
| padronização contra não normalizar, AUC | 180 | +0,041 | 3 · 10⁻²⁸ |
| escala por intervalo contra não normalizar, AUC | 180 | +0,036 | 1 · 10⁻²⁴ |
| escala robusta contra não normalizar, AUC | 180 | +0,038 | 7 · 10⁻²⁷ |
| subamostragem, revocação | 240 | +0,194 | 4 · 10⁻⁴¹ |
| subamostragem, precisão | 240 | −0,150 | 4 · 10⁻⁴¹ |
| subamostragem, AUC | 240 | −0,001 | 0,26 |
| PCA contra não reduzir sem normalização, AUC | 60 | −0,065 | 2 · 10⁻¹¹ |
| PCA contra não reduzir com normalização, AUC | 180 | −0,002 | 0,003 |

Tempo médio por combinação, ajuste e predição nos cinco folds, em `analise_custo_por_opcao.csv`.

| etapa | opção mais barata | opção mais cara |
|---|---|---|
| ausentes | mediana e moda, 1,54 s | indicadora, 1,69 s |
| encoding | pelo alvo, 1,02 s | one-hot, 2,21 s |
| normalização | sem normalização, 1,33 s | padronização, 1,74 s |
| redução | sem redução, 0,76 s | seleção de dez colunas, 2,60 s |
| balanceamento | subamostragem, 1,56 s | SMOTE, 1,69 s |

