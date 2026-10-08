# Pré-processamento e pipelines na previsão de sucesso de bilheteria do cinema brasileiro

**Entrega 2 · CIN0144 — Aprendizado de Máquina e Ciência de Dados · Grupo 11**
Ana Laura, Ana Raquel e Laura Virginia

---

# 1 · Contexto: o problema, o que a E1 deixou, o alvo P75


**O problema.** Queremos prever se um filme brasileiro vai ter público acima do comum usando
apenas informações disponíveis antes da estreia. A base é a listagem oficial da ANCINE de 1995 a
2024, com os dados de fomento público ligados a cada filme. A decisão de financiar um filme
acontece antes de ele existir, e por isso a pergunta que motiva o trabalho continua a mesma da
Entrega 1: o dinheiro público está indo para filmes que encontram plateia?

**O que a E1 deixou.** Medimos três atalhos que inflam o resultado sem ensinar nada ao modelo:
usar a renda como atributo somava 0,161 à AUC, usar o número máximo de salas somava 0,108, e
validar com divisão aleatória em vez de separar por ano somava 0,087. Somados a um alvo que
dependia do ano de lançamento, levavam a AUC de 0,725 a 0,995. Auditamos também o alvo: o público
dos filmes brasileiros não forma um grupo único, e sim dois, os de circuito limitado e os de
lançamento comercial, com fronteira perto do percentil 69. A mediana cai dentro do primeiro
grupo, e por isso separava filmes pequenos bons de filmes pequenos ruins.

**Por que o percentil 75 do ano anterior.** Ele resolve os três problemas do alvo anterior: não
embute o ano, já está publicado quando o filme estreia, e cai perto da fronteira entre as duas
populações. Com ele, 2.590 filmes têm alvo e 25,3% são sucesso. Os cortes em P50 e P90 entram
como teste de robustez na §6, como a E1 recomendou.

**O que muda nesta entrega.** O modelo é fixo, um kNN de sete vizinhos, e comparamos 144 formas
de preparar os dados para ele. Duas conclusões da E1 entram em revisão por consequência direta
disso. A primeira recomendava não balancear, mas foi medida num alvo que era meio a meio por
construção; com um sucesso para cada três fracassos, o balanceamento volta a ser aplicável. A
segunda recomendava não aplicar PCA, mas foi medida com floresta aleatória, que não é afetada
pela escala nem pelo número de atributos. O kNN é afetado pelos dois, e é essa diferença que a
grade mede.

# 2 · Base, alvo e atributos da E2


A base é a mesma da Entrega 1: 2.626 longas brasileiros lançados em sala entre 1995 e 2024,
montados a partir dos dados abertos da ANCINE, do IBGE e do Banco Central. O módulo que a monta
não foi alterado, porque é o entregável congelado da E1.

**A definição de sucesso.** Público acima do percentil 75 dos filmes brasileiros do ano anterior.
A auditoria da E1 mediu três problemas no alvo antigo, que era a mediana global dos trinta anos.
Um limiar global embute o ano, porque o número de lançamentos cresceu catorze vezes entre 1995 e
2024 enquanto o público mediano por filme caiu quinze vezes, de modo que um filme de 1997 e um de
2023 seriam julgados pela mesma régua. A mediana do próprio ano só é conhecida depois que todos os
filmes do ano estrearam, o que a torna indisponível para prever antes da estreia. E a mediana cai
dentro da população de circuito limitado, separando filmes que o mercado não distingue.

| | valor |
|---|---|
| filmes com alvo definido | 2.590 |
| filmes sem alvo | 36, dos quais 22 sem público informado e 14 de 1995, que não têm ano anterior |
| prevalência de sucesso | 25,3%, razão de um para três |
| prevalência por década | 26,7% · 25,2% · 23,0% · 29,1% |

A prevalência é estável entre as décadas porque o limiar acompanha o ano, condição para que a
comparação entre pipelines não dependa do período.

**Os atributos de histórico.** Três atributos novos medem a reputação da direção, da distribuidora
e da produtora: o logaritmo da mediana do público dos filmes da mesma entidade lançados em anos
estritamente anteriores, com ausência quando não há nenhum. A mediana e o logaritmo vêm da
distribuição do público, que é lei de potência com Gini de 0,92, de modo que a média de três filmes
de um diretor ficaria próxima do maior deles. Esses três atributos carregam o sinal das colunas de
identidade que ficaram fora, sem o custo de dimensão que as 1.738 categorias de direção imporiam
ao kNN.

**Os dezoito atributos.** Nove numéricas, três de histórico, quatro nominais e duas ordinais; o
anexo A traz a lista e o motivo de cada exclusão, todas aplicando decisões já tomadas na E1. Saem
do conjunto as colunas que só se conhecem depois da estreia, os identificadores, as colunas
malformadas, as de alta cardinalidade cujo sinal entra pelos históricos e as que são função do
ano. Uma verificação no código interrompe a execução se qualquer coluna proibida aparecer entre os
atributos, de modo que a garantia não depende de alguém lembrar de conferir.

# 3.1 · Técnicas — valores ausentes


O tratamento é obrigatório nas 144 combinações: o kNN decide por distância euclidiana, e não há
distância definida com valor ausente. O que varia é a forma do tratamento.

A ausência relevante é a dos três históricos, e é estrutural, porque indica que a entidade nunca
lançou filme. Falta o histórico da direção em 67,88% dos filmes, o da produtora em 59,61% e o da
distribuidora em 20,81%; entre os outros quinze atributos a maior ausência é de 0,46%. É essa
última linha que explica por que a etapa só passou a ter conteúdo com a entrada dos históricos.

| opção | o que faz | característica dos dados que a motiva |
|---|---|---|
| mediana e moda | imputa mediana nas numéricas e moda nas categóricas; compõe o baseline | a cauda das contagens de fomento pede mediana, não média; nos históricos, já em logaritmo e com assimetria entre −0,02 e 0,56, as duas coincidem |
| indicadora de ausência | imputa mediana e acrescenta sete colunas que marcam o que faltava | a E1 classificou a ausência desta base em quatro naturezas e achou dois casos em que ela carrega informação |

A primeira posiciona o estreante no meio da nuvem dos veteranos típicos, região de maior densidade
de vizinhos; a segunda deixa o kNN distinguir o estreante em vez de lhe atribuir reputação mediana.

A hipótese é que as duas empatem, e a razão está medida: a falta de histórico coincide com a
inexistência de filme anterior registrado em mais de 99,8% dos casos. Essa informação já consta de
outras colunas, então três das sete indicadoras repetem o que a base diz, e todas diluem as demais
dimensões no cálculo da distância. Estimar o valor ausente a partir de filmes semelhantes foi
descartado por não haver o que recuperar numa ausência estrutural, e por pôr um kNN no
pré-processamento de um kNN.

# 3.2 · Técnicas — encoding


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

# 3.3 · Técnicas — normalização


A distância euclidiana soma as diferenças de todas as colunas sem distinguir o que cada uma mede,
e nesta base as escalas são incomparáveis: o ano vai de 1996 a 2024, a contagem de filmes
anteriores da distribuidora vai de zero a 179 com mediana 9,5, os indicadores de fomento valem
zero ou um, e os históricos, em logaritmo, ficam entre zero e cerca de sete. Sem correção, as duas
colunas de maior amplitude decidem sozinhas quem é vizinho de quem.

A etapa age na matriz inteira, depois do encoding, porque é nela que o kNN mede distância; escalar
só as numéricas esconderia a interação com o encoding que a §5.3 discute.

| opção | o que faz | característica dos dados que a motiva |
|---|---|---|
| sem normalização | preserva as escalas cruas; compõe o baseline | testa se as escalas cruas já servem |
| padronização | centra em zero e divide pelo desvio-padrão | é o tratamento direto do problema de amplitude acima |
| escala por intervalo | comprime cada coluna para zero a um | as binárias do one-hot já vivem nesse intervalo e ficam intactas; o custo é depender do máximo, e numa coluna de cauda longa a maioria dos filmes fica perto de zero |
| escala robusta | centra na mediana e divide pelo intervalo interquartil | a E1 documentou assimetria de 2,0 a 3,8 nos históricos, e essas são as medidas adequadas a essa cauda |

A hipótese não é a de que normalizar ajuda, que seria trivial, mas a de que a melhor normalização
depende do encoding. O argumento é aritmético: numa coluna binária em que um por cento dos filmes
vale um, o desvio-padrão é cerca de 0,0995, e dividir por ele transforma o valor um em
aproximadamente 9,9, de modo que uma categoria com um punhado de filmes pesaria dez vezes mais na
distância que uma numérica. Daí a previsão de que a padronização renderia menos no espaço dos
indicadores e que a escala por intervalo seria a mais segura ali; a §5.3 mostra que o efeito medido
tem outra forma. Uma transformação de potência antes da escala ficou fora para manter o espaço em
144 combinações, embora a S5 da E1 tenha medido com ela 0,024 de ganho no modelo linear.

# 3.4 · Técnicas — redução de dimensionalidade


Com o encoding por indicadores a matriz chega a cerca de 84 colunas, boa parte quase vazia. Em
dimensão alta as distâncias se concentram: o vizinho mais próximo deixa de ser significativamente
mais próximo que o mais distante, e o voto dos sete perde o sentido que tem num espaço de poucas
dimensões. A H13 da E1 concluiu que não valia aplicar PCA, mas foi medida com floresta aleatória,
modelo indiferente a escala e a dimensão. O kNN não é, e é essa diferença que a etapa põe à prova.

| opção | estratégia | característica dos dados que a motiva |
|---|---|---|
| sem redução | preserva todas as colunas; compõe o baseline | é a H13 da E1, agora testada num modelo sensível a dimensão |
| PCA retendo 95% da variância | troca as colunas por combinações delas | as 84 colunas do one-hot são em boa parte esparsas, e é o caso em que a concentração de distâncias morde |
| seleção das dez melhores por informação mútua | mantém colunas originais e descarta o resto | a E1 achou redundância entre atributos, e na distância um atributo ruidoso pesa tanto quanto um útil |

As duas técnicas atacam o mesmo problema por lados opostos, e é essa oposição que torna a
comparação informativa: o PCA preserva a variância mas entrega eixos que não correspondem a
atributo nenhum, de modo que se perde a leitura de qual característica decidiu; a seleção preserva
essa leitura e descarta informação de forma irreversível. A informação mútua foi escolhida em vez
do teste F porque o kNN é não paramétrico, e a relação que lhe interessa não precisa ser linear. O
orçamento de dez colunas é absoluto, e não proporcional, porque ao seletor chegam cerca de vinte
colunas com o encoding pelo alvo e cerca de 84 com o de indicadores: só um número igual mantém a
frase "as dez melhores colunas" com o mesmo significado nos dois casos.

A etapa fica antes do balanceamento porque o PCA e a seleção precisam ser ajustados só com filmes
reais. A hipótese é que a redução só seja inofensiva na presença da normalização, e o caso crítico
é o PCA: sem correção de escala a variância é quase toda de duas colunas, de modo que o corte de
95% sairia em um ou dois componentes que carregam apenas elas.

# 3.5 · Técnicas — balanceamento


Com 25,3% de sucessos há um para cada três fracassos. A E1 decidiu não balancear, mas com o alvo na
mediana, que divide os filmes ao meio; com o novo alvo a classe de sucesso é minoritária e o
balanceamento entrou na grade, com a opção de não balancear preservada para testar se a decisão da
E1 ainda vale.

O kNN prevê sucesso quando pelo menos quatro dos sete vizinhos são sucesso. Como a maioria dos
vizinhos costuma ser fracasso, esse limite raramente é atingido. Outros modelos permitem dar mais
peso à classe rara; o kNN não, e a única forma de mudar a votação é mudar a proporção de sucessos
no treino.

| opção | o que faz | vantagem e custo |
|---|---|---|
| sem balanceamento | mantém a base | serve de referência |
| subamostragem | remove fracassos ao acaso até igualar as classes | equilibra o voto, mas descarta cerca de 1.020 dos 2.070 filmes de cada treino, e o kNN depende de densidade de vizinhos |
| SMOTE | cria sucessos entre dois sucessos parecidos, usando os cinco mais próximos | não descarta nada, mas no espaço dos indicadores cria filmes impossíveis, com metade de uma distribuidora e metade de outra |

A biblioteca de reamostragem garante que o balanceamento aconteça apenas no treino: os filmes de
teste são avaliados como estão, sem remoção nem criação de exemplos.

Duplicar sucessos ao acaso ficou fora porque um mesmo filme copiado pode ocupar vários dos sete
vizinhos e decidir o voto sozinho; a versão do SMOTE para categóricas precisa das colunas
originais, e aqui o balanceamento vem depois do encoding. A hipótese, registrada antes de rodar a
grade, é que o balanceamento aumente a revocação e o F1, diminua a precisão e a acurácia, e quase
não mexa na AUC, que não depende de ponto de corte.

# 4 · Protocolo executado


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



O filme de sucesso é a classe positiva. Reportamos as cinco métricas pedidas, acurácia, F1,
precisão, revocação e AUC, mais a precisão média, cada uma como média e desvio-padrão amostral dos
cinco folds. A acurácia sozinha engana aqui: com 25,3% de sucessos, um modelo que sempre responde
fracasso acerta 74,7% das vezes e nunca encontra um sucesso. A AUC é a métrica principal, a mesma
da E1, porque mede se o modelo coloca os sucessos acima dos fracassos ao ordenar, sem depender de
corte. F1, precisão e revocação medem a decisão final, tomada no corte de quatro votos em sete, e
é aí que esperamos o efeito do balanceamento.

# 5.1 · Visão geral, baseline, melhores e piores


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

# 5.2 · Efeito isolado de cada etapa


A tabela traz as duas leituras do módulo de análise. A primeira é a que o enunciado pede, a média
das combinações agrupadas pela opção, e tem o defeito de misturar contextos. A segunda corrige
isso por pareamento: fixa as outras quatro etapas e compara a opção com a de referência dentro de
cada contexto, com vitória, empate ou derrota decididos pela regra da §4. É a contagem pareada que
sustenta afirmação, e é ela que autoriza dizer que uma técnica nunca piorou.

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
| | seleção de dez colunas | 0,821 | 0 vitórias, 43 empates, 5 derrotas em 48 |
| balanceamento | sem balanceamento | 0,822 | referência |
| | subamostragem | 0,821 | 0 vitórias, 44 empates, 4 derrotas em 48 |
| | SMOTE | 0,814 | 1 vitória, 41 empates, 6 derrotas em 48 |

**A normalização é a única etapa que decide o resultado.** As três técnicas somam 68 vitórias, 40
empates e nenhuma derrota em 108 comparações pareadas, com ganho médio entre 0,036 e 0,041. A
explicação está na métrica do classificador: a distância euclidiana soma diferenças sem normalizar
unidades, e aqui a contagem de filmes anteriores da distribuidora varia de zero a 179 enquanto os
indicadores de fomento variam de zero a um. Sem correção, dois filmes são próximos quando têm
distribuidoras de porte parecido, e o resto é arredondamento. As três escalas empatam entre si,
com diferença máxima de 0,004 contra desvio típico de 0,014 entre folds: o que importa é
normalizar, não qual escala escolher.

**A redução nunca ganhou.** Nem o PCA nem a seleção venceram em um único contexto, e o PCA perdeu
em doze. A H13 da E1 sobrevive, agora testada com o modelo sensível à dimensão que era a nossa
objeção contra ela. Há, porém, um achado de engenharia: a seleção empata com a matriz completa em
43 dos 48 contextos, e nesses casos o kNN decide com dez colunas em vez de cerca de cinquenta.

**O encoding pelo alvo tem vantagem pequena e consistente.** A diferença média, 0,007, é menor que
o desvio entre folds e portanto é empate pela nossa regra; o pareamento mostra 13 vitórias e
nenhuma derrota em 72 contextos, padrão difícil de atribuir ao acaso. A leitura honesta é que o
efeito existe e é pequeno. O mecanismo é dimensional: dezoito colunas contra cerca de 84, e em
dimensão menor as distâncias discriminam melhor.

**A indicadora de ausência não acrescentou nada**, o que refuta a hipótese da §3.1: zero vitórias e
quatro derrotas em 72 contextos. A informação já estava na base, porque a falta de histórico
coincide com a contagem de filmes anteriores igual a zero em quase todos os casos, e essa contagem
é um atributo numérico que o kNN já usa. A indicadora repete em sete colunas novas o que três
colunas antigas diziam, e colunas repetidas custam dimensão sem informar.

**O balanceamento não move a AUC e muda a decisão**, como a §4 previu.

| métrica | sem | subamostragem | SMOTE | pareado contra não balancear |
|---|---|---|---|---|
| revocação | 0,548 | 0,741 | 0,736 | 48 vitórias em 48, para as duas |
| precisão | 0,692 | 0,543 | 0,530 | 48 derrotas em 48, para as duas |
| acurácia | 0,825 | 0,774 | 0,767 | 48 derrotas em 48, para as duas |
| F1 | 0,609 | 0,625 | 0,615 | subamostragem: 15 vitórias, 33 empates |
| AUC | 0,822 | 0,821 | 0,814 | subamostragem: 44 empates, 4 derrotas |

Balancear aumenta a revocação em cerca de 0,19 em todos os 48 contextos e cobra 0,15 de precisão e
0,05 de acurácia, também sem exceção. É o que o mecanismo prevê: a AUC avalia a ordenação, que o
balanceamento não altera, enquanto revocação e precisão avaliam a decisão tomada no corte de quatro
votos em sete. Entre as duas técnicas a subamostragem domina o SMOTE, ganhando em F1 em quinze
contextos sem nunca perder, enquanto o SMOTE perde em sete. É contraintuitivo, porque a
subamostragem descarta metade dos filmes de cada treino; a explicação provável é o espaço em que o
SMOTE opera, interpolando numa matriz com colunas de indicadores e produzindo filmes com meia
distribuidora, que entram na votação como se fossem reais.

**Verificação independente.** A regra de empate é o critério do enunciado, e é por ela que o
relatório decide. Como checagem, aplicamos também o teste de Wilcoxon pareado sobre as diferenças
por fold, aproveitando que os folds são idênticos em todas as combinações.

| afirmação | n | diferença média | p |
|---|---|---|---|
| padronização contra não normalizar | 180 | +0,041 | 3 · 10⁻²⁸ |
| escala por intervalo contra não normalizar | 180 | +0,036 | 1 · 10⁻²⁴ |
| escala robusta contra não normalizar | 180 | +0,038 | 7 · 10⁻²⁷ |
| subamostragem em revocação | 240 | +0,194 | 4 · 10⁻⁴¹ |
| subamostragem em precisão | 240 | −0,150 | 4 · 10⁻⁴¹ |
| subamostragem em AUC | 240 | −0,001 | 0,26 |

As afirmações fortes passam com margem larga, e a única comparação não significativa é justamente
a que afirmamos ser nula, o efeito do balanceamento na AUC.

# 5.3 · Interações


O enunciado define interação como a técnica que só se mostra benéfica na presença de outra. O
módulo de análise procura isso sem intervenção: compara cada opção com a sua referência dentro de
cada recorte da outra etapa e marca interação quando o veredito muda de recorte para recorte. Dois
pares foram marcados.

**A redução depende da normalização.**

| PCA contra não reduzir, por normalização | vitórias, empates, derrotas | ganho médio | veredito |
|---|---|---|---|
| com padronização | 0, 12, 0 | +0,000 | empate |
| com escala por intervalo | 0, 12, 0 | −0,003 | empate |
| com escala robusta | 0, 12, 0 | −0,003 | empate |
| sem normalização | 0, 0, 12 | **−0,065** | perde |

O PCA empata com não reduzir nos 36 contextos em que há normalização e perde nos 12 em que não há.
A causa não é conjetura: a grade registra quantas colunas chegam ao classificador, e nas
combinações de PCA sem normalização esse número é 2,0. O corte de 95% da variância sai em dois
componentes, o que faz sentido, porque sem correção de escala a variância total é quase toda da
contagem de filmes anteriores da distribuidora e do ano; dois componentes bastam para reproduzir
essas duas colunas, e os demais atributos cabem nos 5% descartados. O classificador recebe um
espaço de duas dimensões que sabe apenas o porte da distribuidora e o ano, e as seis piores
combinações do ranking são exatamente essas.

O teste pareado acrescenta uma leitura. Sem normalização, a perda de 0,065 tem p = 2 · 10⁻¹¹ em
sessenta pares; com normalização, a perda média cai a 0,002 e o teste ainda acusa p = 0,003, porque
o efeito é minúsculo mas sistemático. É o caso didático da diferença entre as duas leituras:
significativo não quer dizer relevante, e 0,002 de AUC está sete vezes abaixo do desvio entre
folds. Pela regra do enunciado, que é o critério adotado, isso é empate.

A consequência é uma regra de ordem, não uma preferência de técnica: num pipeline com kNN, a
redução por componentes principais precisa vir depois de uma escala, e um pipeline que inverta essa
ordem não é subótimo, é um erro de construção. A seleção por informação mútua não apresenta esse
comportamento, porque escolhe colunas por associação com o alvo, e associação não depende da
unidade em que a coluna está medida.

**A normalização rende mais com o encoding pelo alvo.**

| normalização contra não normalizar | com encoding pelo alvo | com one-hot |
|---|---|---|
| padronização | 15, 3, 0 · ganho +0,047 · vence | 7, 11, 0 · ganho +0,035 · empate |
| escala por intervalo | 17, 1, 0 · ganho +0,049 · vence | 6, 12, 0 · ganho +0,024 · empate |
| escala robusta | 15, 3, 0 · ganho +0,042 · vence | 8, 10, 0 · ganho +0,033 · empate |

As três vencem no espaço do encoding pelo alvo e apenas empatam no do one-hot, e é essa mudança de
veredito que caracteriza a interação. Nenhuma chega a perder em qualquer recorte, de modo que a
recomendação de normalizar não muda; o que muda é quanto se ganha.

O resultado tem forma diferente da prevista na §3.3. Esperávamos que a padronização sofresse no
one-hot pelo fator 9,9 das binárias raras, e que a escala por intervalo fosse a mais segura ali. O
medido mostra o contrário: a escala por intervalo é a que mais perde ao sair do encoding pelo alvo
para o one-hot, de 0,049 para 0,024, enquanto a padronização cai menos, de 0,047 para 0,035.

A explicação inverte o nosso próprio argumento. A escala por intervalo não mexe nas colunas
binárias, mas comprime as numéricas de cauda longa para uma faixa estreita perto de zero, já que
são governadas pelo máximo; as cerca de 84 colunas de indicadores passam a ter amplitude efetiva
maior que as numéricas e dominam a distância. A padronização iguala a dispersão de todas as
colunas, inclusive as binárias, e impede que qualquer grupo domine. Quanto ao fator 9,9, a
explicação provável para a sua ausência está numa decisão da etapa anterior: o one-hot agrupa as
categorias com menos de dez filmes, de modo que as colunas raríssimas das quais o argumento
dependia não chegam a existir. É hipótese compatível com o medido, não efeito isolado; isolá-lo
exigiria rodar a grade sem esse agrupamento, o que fica como extensão na §7.

O par balanceamento e normalização não foi marcado como interação: as duas técnicas empatam com não
balancear em todos os recortes, e só a magnitude muda. Ainda assim, a subamostragem tem ganho médio
de −0,013 sem normalização e de +0,007 com padronização, pelo mesmo mecanismo: ela descarta metade
dos filmes e a densidade de vizinhos cai, o que agrava um espaço já decidido por duas colunas e se
paga num espaço escalado.

# 5.4 · Custo


A grade inteira levou 3,9 minutos de ajuste e predição somados, com mediana de 0,92 segundo por
combinação e máximo de 3,99 segundos.

| etapa | opção mais barata | opção mais cara |
|---|---|---|
| ausentes | mediana e moda, 1,54 s | indicadora, 1,69 s |
| encoding | pelo alvo, 1,02 s | one-hot, 2,21 s |
| normalização | sem normalização, 1,33 s | padronização, 1,74 s |
| redução | sem redução, 0,76 s | seleção de dez colunas, 2,60 s |
| balanceamento | subamostragem, 1,56 s | SMOTE, 1,69 s |

Três leituras. A normalização, que domina o resultado, é praticamente de graça: 0,41 segundo
separa a mais barata da mais cara, e as três escalas custam o mesmo entre si, com diferença de
0,07 segundo. A etapa de maior efeito é a de menor custo relativo da grade.

O custo se concentra em duas escolhas, o one-hot e a seleção por informação mútua, e as dez
combinações mais caras são todas interseção das duas, todas com imputação por indicadora. A mais
cara leva 3,99 segundos, mais de quatro vezes a mediana.

A terceira leitura é a interessante. A correlação de Spearman entre o tempo total e o número de
colunas que chegam ao classificador é negativa, de −0,144: combinações com mais colunas tendem a
ser mais rápidas, o que parece absurdo e não é. As dez mais caras entregam exatamente dez colunas
ao kNN, porque todas usam a seleção; o custo não está em medir distância em muitas dimensões, está
em estimar informação mútua entre 84 colunas e o alvo, cinco vezes, uma por fold, antes de o
classificador existir. Nesta grade o gargalo é o ajuste do pré-processamento, não a predição, e é
por isso que a dimensão final não prediz o tempo.

A consequência de projeto é que a seleção, que custa mais que o triplo de não reduzir e não ganha
em nenhum contexto, só se paga quando o objetivo é um modelo final mais enxuto: compra-se uma
matriz cinco vezes menor com um ajuste mais caro, pago uma única vez.

# 6 · Robustez: temporal, P50/P90, por gênero


A §5 mede tudo sob um único arranjo. Esta seção pergunta o que sobrevive quando ele muda. Doze
combinações passaram pelas três checagens: o baseline, as cinco melhores, as cinco piores e a
melhor de cada opção de balanceamento.

**Validação temporal.** Treino até 2017, teste de 2018 em diante, que é a validação defendida pela
E1 e substituída pelo enunciado desta entrega.

| combinação | AUC em cinco folds | AUC temporal | otimismo |
|---|---|---|---|
| baseline, sem transformação opcional | 0,827 | 0,588 | 0,239 |
| indicadora, alvo, padronização, PCA, subamostragem | 0,847 | 0,799 | 0,049 |
| alvo, padronização, PCA, subamostragem | 0,853 | 0,793 | 0,060 |
| alvo, padronização, subamostragem | 0,848 | 0,790 | 0,058 |
| alvo, escala por intervalo, PCA | 0,850 | 0,738 | 0,113 |
| PCA sem normalização, quatro variantes | 0,731 a 0,750 | 0,531 a 0,556 | 0,176 a 0,219 |

Todas as doze são otimistas na divisão aleatória, o que a §4 já declarava. O que não esperávamos é
a distribuição desse otimismo: o baseline é o mais otimista de todos e cai para 0,588, quase o
acaso, enquanto as três melhores, todas com normalização e encoding pelo alvo, perdem entre 0,049 e
0,060 e seguem acima de 0,79.

O pré-processamento, portanto, não melhora apenas o número do relatório: muda o que o modelo
aprende. Sem normalização e com one-hot, as 455 colunas de distribuidora deixam o kNN reconhecer o
filme pela identidade de quem o distribui, atalho que funciona dentro do mesmo período e não
transfere para anos em que as distribuidoras são outras. Isso qualifica a §5.1: parte dos 105
empates com o baseline é artefato da divisão aleatória, porque pipelines indistinguíveis em cinco
folds se separam em mais de 0,20 de AUC quando o teste é o futuro.

**Troca do corte do alvo.** Nos percentis 50, 75 e 90 do ano anterior, a correlação de Spearman
entre as ordenações é de 0,825 entre P50 e P75, de 0,867 entre P75 e P90 e de 0,664 entre P50 e
P90, todas significativas: a ordenação é estável e menos estável nos extremos, o que é natural
porque P50 e P90 definem problemas diferentes. A separação qualitativa não muda: nos três cortes as
combinações com normalização e encoding pelo alvo ficam entre 0,770 e 0,881, e as de PCA sem
normalização entre 0,711 e 0,750.

**Desempenho por gênero.** A terceira checagem revela a limitação mais séria do modelo.

| gênero | filmes | prevalência | AUC no baseline | AUC na melhor | revocação na melhor |
|---|---|---|---|---|---|
| ficção | 1.627 | 35,6% | 0,813 | 0,832 | 0,826 |
| documentário | 908 | 5,6% | 0,699 | 0,693 | 0,118 |

O agregado esconde dois problemas: a AUC cai cerca de 0,13 em documentário, o que indica que os
atributos descrevem mal o que faz um documentário encontrar plateia, e a revocação em documentário
é de 0,118 na melhor combinação, contra 0,826 em ficção. Mesmo o melhor pipeline encontra menos de
um em cada oito documentários de sucesso. O mecanismo é o do balanceamento levado ao extremo:
com prevalência de 5,6%, menos de um dos sete vizinhos de um documentário típico é sucesso, e o
corte de quatro votos em sete fica inalcançável. Balancear o conjunto inteiro não resolve, porque
equaliza a proporção global e não a da vizinhança em que o documentário vive.

# 7 · Lições, limitações e conclusão


**Uma etapa decide, e as outras quatro são empate.** Normalizar move a AUC em cerca de 0,04 e nunca
prejudicou em 108 comparações pareadas; as demais etapas, lidas isoladamente, empatam na maioria dos
contextos. Para um classificador que decide por distância isso é coerente, porque a única etapa que
altera diretamente a métrica de distância é a que mexe na escala.

**O perigo não está nas técnicas ruins, está nas combinações incoerentes.** A pior configuração da
grade não usa nenhuma técnica desaconselhada: aplica PCA, que é padrão, sobre uma matriz não
escalada, e sobram dois componentes que descrevem duas colunas, com perda de 0,065 de AUC. A lição
vale para qualquer pipeline em que uma etapa pressuponha o trabalho de outra, e é o argumento mais
forte a favor de examinar o espaço de combinações em vez de ajustar uma etapa por vez.

**Reduzir não melhora, mas pode baratear.** Nenhuma opção de redução venceu em um único contexto, e
ainda assim a seleção empata com a matriz completa em 43 dos 48, o que significa que quatro quintos
das colunas podem ser descartados sem custo mensurável em AUC.

**A regra de empate mudou o relatório, e a validação temporal mudou a regra de empate.** Com 105 das
144 combinações empatando com o baseline, quase nada do que um ranking por média sugeriria sobrevive
à variabilidade entre cinco folds. A §6 mostrou o outro lado: parte daqueles empates é artefato do
protocolo, e o baseline é o que menos sobrevive ao futuro, caindo de 0,827 para 0,588. Empate sob um
protocolo não é equivalência, e vale pouco sem uma segunda forma de validar.

**O pré-processamento não melhora o modelo, muda o que ele aprende.** Sem normalização e com
one-hot, as colunas de distribuidora permitem ao kNN reconhecer o filme por quem o distribui, atalho
que não transfere para outros anos; trocar essa identidade por uma coluna de reputação e corrigir a
escala produz um modelo que perde 0,05 ao prever o futuro, em vez de 0,24.

**Limitações.** A contaminação indireta entre folds, descrita na §4, decorre de o enunciado fixar
divisão aleatória e é o que a validação temporal mede. O desempenho em documentário, com revocação
de 0,118, mostra que o modelo não serve para esse segmento e que nenhuma opção da grade corrige
isso. E o número de vizinhos, fixado em sete, interage com o balanceamento de forma que não pudemos
explorar, porque o limite de quatro votos em sete é parte da razão pela qual a classe minoritária
raramente é prevista.

**O que faríamos a seguir.** Uma transformação de potência antes da escala, deixada fora para manter
o espaço em 144 combinações. Rodar a grade sem o agrupamento de categorias raras do one-hot, que é o
teste capaz de isolar o efeito que a §5.3 só pôde conjeturar. E ajustar o número de vizinhos dentro
de cada fold, com limiar próprio por gênero, que é a forma de atacar a limitação do documentário.

# Anexo · Tabela das 144, versões, folds


## A · Tabela completa das 144 combinações

A tabela está em `reports/e2/anexo_144.md`, gerada por `python src/e2/anexo.py` a partir do
arquivo de resultados, e tem uma linha por combinação com o identificador, a opção adotada em cada
uma das cinco etapas, média e desvio das seis métricas, o número de colunas que chegaram ao
classificador, o tempo de execução e a coluna de erro. A mesma tabela em valores separados por
vírgula, no mesmo diretório, serve para importar no documento final sem digitação. A coluna de
erro está vazia nas 144 linhas: nenhuma combinação falhou.

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
execução gravada no repositório.

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

