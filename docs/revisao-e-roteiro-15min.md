# Revisão crítica dos slides + roteiro de fala (15 min)

**Entrega 1 — AMCD · CIn/UFPE · Grupo 11**
Slides analisados: **1 a 17** do `AMCD_ENTREGA_1.pdf`. As páginas 18+ (template) foram ignoradas.
Tudo aqui foi conferido contra este repositório: `notebooks/Entrega_1_...ipynb`,
`docs/relatorio-entrega1.md`, `reports/sensibilidades_s1.csv` e `data/processed/filmes.csv`.

---

## Mapa dos 17 slides

| # | O que está na tela | Tipo |
|---|---|---|
| 1 | Capa — título + 3 autoras | texto |
| 2 | "É possível prever o sucesso antes da estreia" + restrição | texto |
| 3 | O mercado mudou — tabela 1995 / 2024 | tabela |
| 4 | Lançamentos por ano + público mediano por ano (log) | figura |
| 5 | "A definição de sucesso muda tudo" | texto |
| 6 | Taxa de positivos por década + correlação do ano (−0,364 → +0,002) | figura |
| 7 | Quais atributos carregam informação — 3 números | texto |
| 8 | Spearman com o alvo + V de Cramér com o alvo | figura |
| 9 | Diagnóstico: 4 naturezas de ausência | texto |
| 10 | Ausência por atributo | figura |
| 11 | Outliers e balanceamento | texto |
| 12 | Balanceamento, cardinalidade e redundância | texto |
| 13 | **Repetição exata da figura do slide 6** | figura |
| 14 | Vazamento — antes × depois da estreia | texto |
| 15 | Hipóteses de pré-processamento (tabela) | tabela |
| 16 | Conclusão — AUC 0,995 × 0,696 | texto |
| 17 | Obrigada! | texto |

---

# PARTE 1 — AVALIAÇÃO DOS SLIDES

## 1.1 O problema mais grave: um número que o repositório não sustenta

**O slide 16 afirma AUC 0,696 para o cenário honesto. Esse número não existe em lugar nenhum deste repositório.**

O que o notebook executado (célula S3) de fato imprime:

| cenário | alvo | partição | AUC |
|---|---|---|---|
| caminho fácil (alvo global + `renda` + `max_salas`, 5-fold aleatório) | global | aleatória | **0,995** |
| honesto, alvo global, partição temporal | global | temporal | 0,745 |
| honesto, alvo relativo, 5-fold aleatório | no ano | aleatória | 0,770 |
| **honesto, alvo relativo, partição temporal** | **no ano** | **temporal** | **0,725** |

Os três marcadores do lado direito do slide 16 — `sucesso_no_ano`, só informação
pré-estreia, validação temporal — descrevem **exatamente** a última linha. O número
correspondente é **0,725**, e é o número que o `README.md`, o `docs/relatorio-entrega1.md`
e o `docs/roteiro-apresentacao.md` usam.

**Risco real:** o professor abre o notebook (que vocês vão entregar junto) e encontra
0,725 onde o slide diz 0,696. Isso não parece erro de digitação — parece número escolhido.
É o tipo de coisa que derruba a credibilidade de uma apresentação inteira que é,
justamente, sobre rigor metodológico.

**Correção:** ou trocar para **0,725**, ou, se 0,696 veio de uma execução nova (semente
diferente, conjunto de atributos diferente), incluir essa execução no notebook antes de
apresentar. Não existe terceira opção.

> Efeito colateral bom: a diferença 0,995 → 0,725 é **0,27 de AUC**, um número mais
> redondo e mais impressionante do que 0,299.

## 1.2 Clareza da história

**O que funciona.** A espinha dorsal está certa e é rara em trabalho de graduação: o
deck não é um checklist de EDA, é um **argumento** — "a definição de sucesso decide se o
problema é sobre cinema ou sobre calendário". Os slides 3 → 4 → 5 → 6 constroem isso em
sequência e o slide 6 entrega a prova. Essa é a melhor parte da apresentação.

**Onde a narrativa quebra.**

1. **O slide 2 pergunta e não responde.** Ele enuncia "é possível prever o sucesso antes
   da estreia?" e o slide 16 fecha com uma lição de método — sem nunca voltar à pergunta.
   O público sai sem saber a resposta. **Falta uma frase no slide 16**: "sim, parcialmente:
   AUC 0,725, bem acima do acaso e longe da certeza."

2. **"Sucesso" nunca é definido positivamente em tela.** O slide 5 diz o que a definição
   errada faz, mas em nenhum momento aparece escrito *sucesso = público acima da mediana
   do próprio ano de lançamento*. O público só descobre isso pela legenda `sucesso_no_ano`
   de um gráfico. Isso precisa estar em texto, no slide 2 ou no 5.

3. **A base nunca é apresentada.** Não há um único slide dizendo **2.626 filmes, 1995–2024,
   35 atributos, cinco fontes públicas** (listagem da ANCINE, FSA, fomento indireto, IPCA
   do BCB, IBGE). Numa banca de Computação, "de onde vieram os dados e quantos são" é a
   segunda pergunta que alguém faz. Hoje ela não tem resposta na tela.

4. **O slide 13 repete a figura do slide 6, idêntica**, sete slides depois e fora de
   contexto — entre "cardinalidade" e "vazamento". Quem estiver prestando atenção vai
   achar que perdeu alguma coisa.

5. **A ordem dos blocos 9–14 é frouxa.** Ausentes (9–10) → outliers (11) → balanceamento
   e cardinalidade (12) → vazamento (14) é uma lista de tópicos, não uma progressão.
   Funciona, mas perde energia depois do pico do slide 6. **O vazamento (14) é o segundo
   achado mais forte do trabalho e está enterrado no fim.**

## 1.3 Conteúdo técnico

**Correto.** Não há erro conceitual de Machine Learning nos slides. Os quatro pontos
mais delicados estão certos:

- vazamento definido como disponibilidade temporal, não como correlação alta;
- classes equilibradas **por construção** do alvo, logo balancear seria ritual;
- cauda de uma lei de potência não é anomalia;
- validação temporal porque o uso real é prever filme não estreado.

**O que está tecnicamente frágil.**

- **Slide 7 compara V de Cramér com rho de Spearman como se fossem a mesma escala.**
  "Gênero 0,338 / origem do fomento 0,320 / projetos de incentivo 0,274" sugere um ranking
  único. Mas V de Cramér mora em [0, 1] e mede associação entre categóricas; Spearman mora
  em [−1, 1] e mede monotonicidade. Um V de 0,338 **não** é "maior" que um rho de 0,274 —
  são réguas diferentes. O slide 8 faz certo (dois painéis separados, cada um com seu
  eixo). O slide 7 desfaz isso. **Precisa ser dito em voz alta**, obrigatoriamente.

- **`max_salas` é apresentado como vazamento puro, e não é tão simples.** No slide 14 ele
  aparece na coluna "depois da estreia" ao lado de `publico` e `renda`. Mas `renda` é
  literalmente público × preço (rho = 0,99 — é a resposta); `max_salas` é o **máximo
  atingido durante a carreira**, que mistura uma parcela decidida antes (o plano de
  lançamento) com uma parcela que reagiu ao desempenho (distribuidora expande filme que
  vai bem). O repositório trata isso com todo o cuidado (`docs/02-decisoes-e-escopo.md`);
  o slide achata. Não é erro — é simplificação que **vira pergunta certa da banca**. A
  defesa está pronta no roteiro (Parte 3, slide 14).

- **A ausência de `max_salas` como "não aleatória" está sustentada por muito pouco.**
  Rodei em `data/processed/filmes.csv`: entre os filmes que têm alvo, só **37** não têm
  `max_salas`, e a mediana de público desses 37 é **3.400** contra **2.753** dos demais —
  ou seja, *mais alta*, e não mais baixa. É uma diferença pequena, em direção contrária à
  intuição usual, sobre uma amostra minúscula. Chamar de MNAR no slide 9 é defensável
  como hipótese, mas **não afirmem a direção do efeito** se perguntarem. Digam: "a
  ausência não parece aleatória, mas são 37 registros — é indício, não prova."

## 1.4 Qualidade dos dados

Esta é a parte mais completa do deck em conteúdo e a mais fraca em construção.

**Bem resolvido:** a ideia de que "nem todo dado ausente significa a mesma coisa" e a
separação em quatro naturezas (estrutural, de junção, MNAR, alvo faltante) é exatamente
o raciocínio que se espera. Todos os percentuais do slide 9 conferem com a figura e com
a base: 59,9% / 23,3% / 2,13% / 0,84%.

**Problemas:**

1. **O slide 9 e o slide 10 discordam na tela.** O slide 9 abre com 59,9% (produtora
   minoritária) como maior ausência; o slide 10, logo em seguida, mostra `uf2_bruto` com
   **61,50%** no topo do gráfico. Ninguém explicou o que é `uf2_bruto` nem por que ele
   sumiu da lista anterior. Ou incluam, ou digam em voz alta que é o mesmo fenômeno
   (a UF da coprodutora que não existe).

2. **A decisão sobre outliers é afirmada sem a evidência em tela.** O slide 11 diz "a
   cauda faz parte do fenômeno" — e não mostra a cauda. A distribuição de público é o
   achado descritivo mais forte do trabalho (mediana **2.806**, média **148.399**,
   assimetria **10,0**, 1% dos filmes com 36% do público) e **está na figura
   `reports/figuras/fig01-distribuicao-publico.png`, que vocês já têm pronta e não usaram.**
   Sem ela, "não remover outliers" soa como preguiça justificada depois. Com ela, vira
   decisão óbvia. **É a melhora de maior retorno por esforço em todo o deck.**

3. **O critério de Tukey merece uma frase.** 17,4% de outliers é um número grande; ele é
   grande porque o IQR pressupõe simetria e a distribuição é log-normal. Dizer isso em voz
   alta transforma um número suspeito em argumento.

4. **Cardinalidade está tratada, redundância também, mas sem consequência.** O slide 12
   lista 1.738 direções, 467 distribuidoras, rho = 0,86 entre `ano` e `filmes_no_ano`, moda
   de 97,1% em `n_ufs` — e para por aí. Só no slide 15 aparece "agrupar categorias raras".
   O ouvinte precisa segurar quatro fatos por três slides até receber a decisão.

## 1.5 Vazamento de dados — avaliação específica

**A distinção antes/depois da estreia está clara e o enquadramento está certo.** A frase
do slide 14 — *"estar na base ≠ estar disponível antes da estreia"* — é a definição
correta de vazamento e vale mais do que qualquer definição de livro. Um professor de ML
reconhece na hora que o grupo entendeu o conceito, e não só decorou.

**O que falta para o argumento ser convincente, e não só correto:**

- **Não há um único número no slide 14.** A tabela diz *quais* atributos saem; não diz
  *quanto custa* tirá-los. E vocês têm esse número medido, em `reports/sensibilidades_s1.csv`:
  honesto 0,832 → +`max_salas` 0,940 (**+0,108**) → +`renda` 0,993 (**+0,161**) → os dois
  0,995. **Um vazamento sem preço é uma opinião; com preço, é resultado.** Colocar
  "+0,16 de AUC" nesse slide é a segunda melhora de maior retorno do deck.

- **Falta dizer por que `fomento` está do lado limpo.** É o ponto mais inteligente do
  trabalho e está invisível: fomento é **aprovado antes de a obra existir**, então não
  pode carregar desempenho. Sem essa frase, um professor atento pergunta "e por que
  fomento não é vazamento também?" — e a pergunta parece ter pegado vocês.

- **Falta a ressalva honesta:** o indicador de FSA tem **rho = 0,511 com o ano** (o FSA foi
  criado em 2006), então ele é em parte um marcador de filme recente. Vocês sabem disso e
  está no relatório. Dizer isso espontaneamente é o que separa um grupo que analisou de um
  grupo que reportou.

**Veredito da seção:** o argumento é convincente conceitualmente e subdimensionado
empiricamente. Corrigível **inteiramente na fala**, sem editar o slide.

## 1.6 Avaliação do modelo — 0,995 contra 0,696

**A comparação está bem construída visualmente** — duas colunas, X vermelho contra
check, três marcadores em cada lado. A frase-título ("um resultado maior não significa
necessariamente um modelo melhor") é a tese certa.

**Mas o slide não explica *por que*, e sozinho ele não convence.** Um ouvinte que não
acompanhou o slide 6 olha 0,995 contra 0,696 e conclui a coisa errada: que o primeiro
modelo é melhor e o segundo é o modelo "capado". Os três marcadores de cada lado são
rótulos, não explicações — nada na tela liga "alvo global" a "o modelo lê o calendário",
nem "validação aleatória" a "o modelo vê o futuro".

**O que o público precisa ouvir, e não está escrito em lugar nenhum:**

1. que os dois números vêm do **mesmo algoritmo, no mesmo protocolo** — o que muda é só a
   base e a forma de validar;
2. que 0,995 é alto **porque o modelo está lendo a resposta**, não porque acertou;
3. que a diferença é **decomponível em três parcelas medidas**: alvo (−0,062),
   atributos posteriores (−0,163), partição temporal (−0,087);
4. que 0,725 é um resultado **modesto e real** — bem acima de 0,5, longe de 1.

Feito isso, o público entende. Sem isso, metade da sala sai achando que vocês pioraram
o modelo de propósito. **Este é o slide que mais depende da fala em todo o deck.**

**Ressalva conceitual que vale citar e ninguém espera:** os dois AUCs não são estritamente
comparáveis, porque não são o mesmo problema — o da esquerda prevê `sucesso_global`, o da
direita prevê `sucesso_no_ano`. Reconhecer isso em voz alta é sinal de maturidade, e a
resposta é boa: *é justamente esse o ponto — o problema da esquerda é mais fácil porque é
um problema diferente e menos interessante.*

## 1.7 Apresentação visual

**Fortes.**

- **Slide 3** — a tabela é o melhor objeto visual do deck: duas linhas, três colunas,
  e os dois multiplicadores logo abaixo em corpo grande. Lê-se em dois segundos.
- **Slide 6** — figura clara, valores rotulados em cima das barras, linha de 50% de
  referência, e o "−0,364 → +0,002" embaixo em destaque. É o slide mais bem construído.
- **Slide 16** — o contraste em duas colunas funciona; o X e o check dão direção imediata.
- **Slide 15** — tabela objetiva, coluna "Decisão" com os "não" em negrito.

**Fracos, em ordem de gravidade.**

1. **Slide 2 — a linha "Restrição: utilizar apenas informações disponíveis antes da
   estreia" aparece DUAS VEZES, uma no meio e outra embaixo.** É erro visível de edição,
   na tela por quase um minuto, logo no segundo slide. **Corrijam isso antes de qualquer
   outra coisa.** O slide ainda fica com metade da área vazia — é onde entram a definição
   de sucesso e o tamanho da base.

2. **Slide 15 — a tabela é um print com os sublinhados vermelhos de corretor ortográfico
   visíveis** sob `sucesso_no_ano`, `max_salas` e `Cauda`. Passa a impressão de captura de
   tela apressada. Desliguem a verificação ortográfica e recapturem, ou refaçam como
   tabela nativa.

3. **Slide 14 — `renda_deflacionada_2024` quebra no meio** ("renda_deflacio / nada_2024") e
   o X fica órfão em uma linha só. A caixa da direita tem quatro itens e a da esquerda
   também, mas com alturas diferentes. Alarguem as caixas ou usem só `renda`.

4. **Todos os slides de figura (4, 8, 10, 13) são retângulos brancos sobre fundo escuro,
   sem nenhum texto do slide.** O único título é o título interno do gráfico, em corpo
   pequeno. Numa sala de aula, da quinta fileira em diante, ninguém lê "Público MEDIANO
   por ano (log)". **Cada slide de figura precisa de uma frase grande, do próprio slide,
   dizendo a conclusão** — "o número de lançamentos subiu 14×; o público mediano caiu 15×".
   O gráfico prova; a frase é o que fica.

5. **Slide 7 — três números flutuando em uma faixa horizontal, com dois terços da tela
   vazios**, sem hierarquia entre eles e sem indicar que medem coisas diferentes. É o
   slide de pior aproveitamento de área do deck.

6. **Slide 9 — quatro caixas brancas de alturas desiguais**, texto miúdo dentro, e a
   maior informação (o percentual) no mesmo peso visual da explicação. Uniformizem a
   altura e subam o percentual.

7. **Slide 12 — duas colunas desbalanceadas**, quebras de linha infelizes
   ("ρ = / 0,86", "1.738 / categorias"), e a coluna da esquerda com três blocos soltos.

8. **Slide 17 — "OBRIGADA!" sozinho.** Um slide de fechamento deveria manter na tela
   aquilo que vocês querem que sobre durante as perguntas: a pergunta original, o
   0,725, e as fontes.

> **Nota deliberada:** o template preto com ícones de cinema é apropriado e está
> consistente. Não mexam nele. Nenhuma das observações acima é preferência estética —
> todas são legibilidade ou erro factual visível.

---

# PARTE 2 — AVALIAÇÃO PARA 15 MINUTOS

## 2.1 Plano de tempo

| # | Função na história | Tempo | Precisa ser EXPLICADO | Pode só ser MOSTRADO | Risco de estourar |
|---|---|---|---|---|---|
| 1 | Gancho — dois números que definem o problema | 0:40 | os dois extremos (2.806 × 12,2 mi) | nomes das autoras | baixo |
| 2 | Pergunta, restrição, definição de sucesso, base | 1:10 | o que é "sucesso"; por que a restrição | número de atributos | **alto** — é onde se enrola |
| 3 | O mercado mudou de natureza | 0:35 | 14× e 15×, e que é composição | a tabela (autoexplicativa) | baixo |
| 4 | A evidência do mercado | 0:55 | os dois eixos; por que log | a pandemia | médio |
| 5 | Transição para o alvo | 0:30 | nada — é uma ponte | a frase da tela | baixo |
| 6 | **O achado central** | 1:40 | 86% × 26%; o que é o +0,002 | a linha de 50% | **alto — e vale a pena** |
| 7 | O que sobra para prever | 0:45 | que V e rho são escalas diferentes | os três números | médio |
| 8 | A evidência dos atributos | 1:10 | o ano em ~zero; gênero no topo | a lista inteira | **alto** — não leiam 17 barras |
| 9 | Quatro naturezas de ausência | 0:55 | estrutural × junção × MNAR | os quatro percentuais | médio |
| 10 | A evidência da ausência | 0:30 | `uf2_bruto` no topo | as barras pequenas | baixo |
| 11 | Outliers — decisão de NÃO fazer | 0:55 | por que o IQR marca 17,4% | preço do ingresso | médio |
| 12 | Balanceamento, cardinalidade, redundância | 0:55 | 50/50 por construção | as quatro linhas | médio |
| 13 | **cortar** (repetida) | — | — | — | — |
| 14 | **Vazamento** | 1:25 | disponibilidade × correlação; +0,16 | a tabela | **alto — e vale a pena** |
| 15 | Evidência → decisão | 0:45 | que toda linha tem medida | a tabela inteira | médio |
| 16 | **A conclusão** | 1:25 | por que 0,995 engana; decompor a diferença | os marcadores | **alto — e vale a pena** |
| 17 | Fechamento | 0:10 | nada | tudo | baixo |

**Total falado: 14:25.** Com as pausas naturais e as trocas de apresentadora, fecha em
**~15:00**.

## 2.2 Quinze minutos são suficientes?

**Sim — e sobra.** O problema deste deck é o oposto do usual: **os slides estão magros
demais para 15 minutos, não cheios demais.** Lidos como estão, sem acrescentar nada,
dão 6 a 7 minutos e a apresentação acaba pela metade do tempo.

Isso é uma boa notícia e um risco. Bom porque não é preciso cortar quase nada. Risco
porque **a diferença entre 7 e 15 minutos tem que vir da fala, não de improviso** — e
improviso a três vozes quase sempre vira repetição.

**Precisam de mais tempo (e de mais conteúdo falado):** slides **6, 14 e 16**. São os três
que sustentam a nota e os três que hoje têm menos texto de apoio por segundo de fala.

**Podem ser rápidos:** 3 (a tabela se explica), 5 (ponte), 10 (a figura confirma o 9),
15 (não leiam a tabela — comentem duas linhas), 17.

## 2.3 Cortar, combinar, simplificar

| Ação | Slide | Por quê |
|---|---|---|
| **CORTAR** | **13** | Repetição exata do 6. Não acrescenta nada e confunde. |
| **COMBINAR** | 11 + 12 | Os dois são "decisões de não fazer" e hoje dividem o mesmo título ("balanceamento") em telas diferentes. Juntos, viram um slide forte: *três decisões de NÃO fazer*. |
| **SIMPLIFICAR** | 7 | Ou vire capa de uma frase ("gênero é o atributo mais associado ao alvo") ou funda com o 8. Três números soltos não justificam uma tela. |
| **ACRESCENTAR** | novo, entre 10 e 11 | A figura `fig01-distribuicao-publico.png`. É a evidência que falta para a decisão de outliers e o achado descritivo mais forte do trabalho. |
| **ACRESCENTAR** | no 2 | Definição de sucesso + tamanho e fontes da base. Espaço já existe na tela. |
| **ACRESCENTAR** | no 14 | O número **+0,16 de AUC**. |
| **ACRESCENTAR** | no 16 | A resposta à pergunta do slide 2. |

Saldo: −1 slide (o 13), +1 slide (a distribuição), fusão de 11 e 12. Ficam **16 telas**,
que é o número certo para 15 minutos com três apresentadoras.

> **Se não der tempo de mexer nos slides:** corrijam **só duas coisas** — a linha
> duplicada do slide 2 e o **0,696 → 0,725** do slide 16. Todo o resto desta revisão
> é recuperável na fala, e o roteiro da Parte 3 já faz isso.

---

# PARTE 3 — ROTEIRO DE FALA

Escrito para ser estudado e falado. Já incorpora todas as correções da Parte 1: assume
**0,725** no slide 16, assume o slide 13 cortado, e recupera na fala tudo que falta na tela.

**Divisão sugerida** (o deck tem três autoras; cada uma é dona de um ato e responde as
perguntas dele):

| Ato | Slides | Quem | Tempo |
|---|---|---|---|
| 1 — O problema e o alvo | 1–6 | Ana Laura | 5:30 |
| 2 — O que os dados têm e o que falta neles | 7–12 | Ana Raquel | 4:30 |
| 3 — Vazamento, decisões e conclusão | 14–17 | Laura Virgínia | 3:45 |

> **Convenção:** o que está em bloco de citação é **fala**. O que está fora é instrução
> de palco.

---

## ATO 1 — Ana Laura

### Slide 1 — Capa · 0:40

> "Boa tarde. Nós somos a Ana Laura, a Ana Raquel e a Laura Virgínia, e o nosso trabalho
> começa com dois números.
>
> O filme brasileiro **mediano** desta base é visto por **duas mil, oitocentas e seis
> pessoas**. O maior da série foi visto por **doze milhões**. É uma diferença de **quatro
> mil trezentas e quarenta e duas vezes** entre o filme do meio e o filme do topo.
>
> A pergunta que nos interessa é: dá para saber de que lado um filme vai cair — **antes
> de ele estrear**?"

*Não leiam o título. Ele já está na tela.*

### Slide 2 — A pergunta e a restrição · 1:10

> "Formalmente, é um problema de **classificação binária**. E três coisas precisam estar
> definidas antes de qualquer modelo.
>
> **A primeira é o que conta como sucesso.** Nós definimos assim: um filme é sucesso se o
> público dele ficar **acima da mediana do próprio ano de lançamento**. Guardem o 'do
> próprio ano' — daqui a três slides ele vai ser o trabalho inteiro.
>
> **A segunda é a restrição**, que é o que dá sentido ao problema: só podemos usar
> informação que existia **antes da estreia**. Se eu souber a bilheteria, prever a
> bilheteria é trivial e inútil. O cenário real é o de um produtor decidindo se financia
> um projeto — ele não tem número nenhum de desempenho, porque o filme ainda não existe.
>
> **A terceira é a base.** São **dois mil seiscentos e vinte e seis filmes brasileiros**
> lançados comercialmente entre **1995 e 2024**, com **35 atributos**, montados a partir de
> cinco fontes públicas: a listagem oficial da ANCINE, os dois registros de fomento — o
> Fundo Setorial do Audiovisual e as leis de incentivo —, o IPCA do Banco Central para
> deflacionar valores, e o IBGE para contexto populacional. Nenhuma exige cadastro ou
> chave de acesso."

*Se estiverem adiantadas, cabe aqui uma frase: "e a coleta não foi trivial — a URL do
portal devolve a página HTML em vez do arquivo, e os registros de fomento estão num host
que não é linkado em lugar nenhum." Se estiverem no tempo, pulem — está no relatório.*

> 🔗 "Antes de construir qualquer modelo, a gente precisava entender uma coisa sobre esse
> período de trinta anos: ele não é homogêneo."

### Slide 3 — O mercado mudou · 0:35

> "Em 1995 estrearam **catorze** filmes brasileiros, e o público mediano por filme foi de
> **catorze mil duzentos e trinta** espectadores. Em 2024 estrearam **cento e noventa e
> sete**, e o público mediano caiu para **novecentos e trinta e três**.
>
> Quatorze vezes mais lançamentos; quinze vezes menos público por filme.
>
> E é importante entender que isso **não** significa que o cinema brasileiro encolheu. O
> público total não caiu nessa proporção. O que aconteceu é que entrou na sala uma
> quantidade enorme de documentário e de produção de circuito limitado que antes
> simplesmente não chegava a estrear. **A queda da mediana é efeito de composição, não de
> crise.**"

> 🔗 "Isso não é uma tabela de dois pontos — é uma tendência de trinta anos."

### Slide 4 — A evidência da mudança · 0:55

> "À esquerda, os lançamentos por ano: crescimento contínuo até 2019, a queda da pandemia,
> e a recuperação depois — 2024 é o ano de maior número de lançamentos da série inteira.
>
> À direita, o público mediano por ano. E reparem no eixo: ele está em **escala
> logarítmica**. Cada marca vale dez vezes a anterior. Se a gente plotasse isso em escala
> linear, os últimos quinze anos seriam uma linha reta colada no zero e a queda ficaria
> invisível. Em log, ela aparece: de cem mil espectadores no pico de 2003 para menos de
> mil em 2020 — **duas ordens de grandeza**.
>
> A conclusão que a gente tira daqui é uma só, e ela é metodológica: **um filme de 1997 e
> um filme de 2023 não competem no mesmo mercado.** Comparar os dois pela mesma régua é
> comparar coisas diferentes."

> 🔗 "E foi exatamente esse erro que a gente quase cometeu."

### Slide 5 — A definição de sucesso · 0:30

> "A forma óbvia de definir sucesso é: público acima da mediana **da base inteira**. Um
> número só, dois mil oitocentos e seis, e todo filme acima dele é sucesso.
>
> Ela tem uma propriedade que parece ótima: produz classes **perfeitamente equilibradas**,
> cinquenta por cento contra cinquenta por cento. A gente olhou esse resultado e quase
> seguiu em frente.
>
> Mas se o público mediano caiu quinze vezes em trinta anos, um limiar fixo não está
> medindo qualidade de filme. Está medindo **década**."

> 🔗 "E quando a gente desagregou, o tamanho do problema apareceu."

### Slide 6 — O achado central · 1:40

*Esta é a tela mais importante da apresentação. Não corram. Deixem a barra vermelha na
tela um segundo antes de falar.*

> "Este gráfico tem duas séries. A **laranja** é a taxa de sucesso por década usando a
> mediana **global**. A **azul** é a mesma taxa usando a mediana **do ano**.
>
> Olhem a laranja. Nos anos 1990, **oitenta e seis por cento** dos filmes são classificados
> como sucesso. Nos anos 2020, **vinte e seis por cento**. São **sessenta pontos
> percentuais** de diferença entre duas décadas, com a mesma definição.
>
> Isso quer dizer que, com a mediana global, o rótulo 'sucesso' está quase inteiramente
> determinado por **quando o filme foi lançado**. Um modelo que receba o ano como atributo
> — e ele recebe — vai encontrar esse atalho, vai atingir um AUC alto, e **não vai ter
> aprendido nada sobre cinema**. Vai ter aprendido a ler o calendário.
>
> Agora olhem a azul. Quarenta e nove, cinquenta, cinquenta, cinquenta. Reta. Ao trocar
> para a mediana do ano, cada filme passa a ser comparado com os filmes que estrearam
> junto com ele, e a década deixa de carregar informação sobre o rótulo.
>
> E embaixo está a medida disso. A correlação entre o **ano** e o alvo era de **menos
> zero vírgula trezentos e sessenta e quatro** com a definição global. Com a definição
> relativa ao ano, ela vai para **mais zero vírgula zero zero dois**. Dois milésimos.
> Efetivamente zero.
>
> Essa é a diferença entre um problema sobre cinema e um problema sobre calendário. E
> nenhuma linha de código distingue os dois — a única coisa que muda é como a gente
> escreveu a definição do alvo.
>
> Isso também tem uma consequência que a gente quer deixar explícita: **não existe
> desbalanceamento a tratar nesta base.** As classes estão em cinquenta e cinquenta por
> construção do alvo. Aplicar SMOTE aqui seria cumprir tabela. O desbalanceamento real
> deste problema nunca foi entre classes — era **ao longo do tempo**, e está resolvido
> nesta tela."

> 🔗 "Tirando o calendário da jogada, o que é que sobra para prever? A Ana Raquel vai
> mostrar."

---

## ATO 2 — Ana Raquel

### Slide 7 — O que carrega informação · 0:45

> "Obrigada. Com o alvo corrigido, a gente foi medir quanto cada atributo se associa ao
> sucesso — e aqui é preciso um cuidado que a gente quer deixar claro, porque **estes três
> números não estão na mesma escala**.
>
> Para os atributos **categóricos**, como gênero, a gente usou o **V de Cramér**, que vai de
> zero a um e mede associação entre variáveis categóricas. Para os **numéricos**, como a
> quantidade de projetos aprovados em leis de incentivo, a gente usou o **rho de Spearman**,
> que vai de menos um a mais um e mede relação monotônica — e a gente usou Spearman, e não
> Pearson, porque a assimetria desta base é dez, e Pearson pressupõe uma distribuição que
> a nossa não tem.
>
> Então: gênero com V de zero vírgula trezentos e trinta e oito é o categórico mais
> associado ao alvo; projetos de incentivo com rho de zero vírgula duzentos e setenta e
> quatro é o numérico mais associado. **Não dá para dizer que o primeiro é 'maior' que o
> segundo** — são réguas diferentes, e por isso a gente mostra as duas separadas."

> 🔗 "O ranking completo está aqui."

### Slide 8 — A evidência dos atributos · 1:10

*Não leiam as barras uma a uma. Apontem três coisas.*

> "Comecem pelo painel da esquerda, e olhem para o **fim** da lista, não para o começo.
> Lá embaixo estão **`ano`, com mais zero vírgula zero zero dois**, e **`filmes_no_ano`,
> com mais zero vírgula zero zero três**. São as duas barras que praticamente não existem
> no gráfico.
>
> Isso é a prova do que a Ana Laura argumentou no slide anterior. Lá era argumento; aqui é
> medida. **O calendário saiu da jogada — e não por convencimento, por número.**
>
> Agora o topo. O atributo honesto mais associado ao alvo é a quantidade de projetos
> aprovados em leis de incentivo, com **zero vírgula vinte e sete**. Depois vem o histórico
> da direção — quantos filmes aquela direção já lançou antes —, com zero vírgula dezenove,
> e o histórico da distribuidora, com zero vírgula dezoito.
>
> Nenhum chega a zero vírgula três. E a gente quer ser explícita sobre isso: **esse
> resultado é modesto, e é esperado que seja.** Se existisse um único atributo que
> explicasse o sucesso de um filme, não existiria indústria de cinema — e nem risco de
> investimento em audiovisual.
>
> No painel da direita, as categóricas pelo V de Cramér. **Gênero, com zero vírgula
> trinta e quatro, é o atributo mais associado ao alvo em toda a base**, considerando cada
> régua na sua escala. Isso tem uma consequência prática imediata para a Entrega 2: nesta
> base, **como a gente codifica as categóricas importa mais do que como a gente transforma
> as numéricas**."

> 🔗 "Isso é o que os dados têm. Agora, o que falta neles."

### Slide 9 — Quatro naturezas de ausência · 0:55

> "A gente não quis tratar valor ausente como um problema só, porque **nem todo dado
> ausente significa a mesma coisa** — e cada natureza pede um tratamento diferente.
>
> Os **cinquenta e nove vírgula nove por cento** de produtora minoritária não são falta de
> dado. São **ausência estrutural**: o filme simplesmente não teve coprodutora. Imputar aqui
> seria inventar uma empresa que não existe. O tratamento correto é uma categoria própria,
> tipo 'sem coprodução'.
>
> Os **vinte e três vírgula três por cento** de população são de outra natureza: vieram da
> **junção** com a série do IBGE, que não cobre todos os anos da nossa base. É uma falha
> nossa de cobertura, não do filme.
>
> Os **dois vírgula um por cento** de máximo de salas são o caso mais delicado: a ausência
> parece **não aleatória** — os filmes sem esse campo têm perfil de público diferente dos
> demais. Se for MNAR mesmo, a própria ausência carrega informação, e o certo é uma
> variável indicadora de ausência, não imputação. A gente registra como hipótese, porque
> são poucos registros.
>
> E os **zero vírgula oito por cento** sem público são os filmes **sem variável-alvo** —
> vinte e dois filmes que a ANCINE publica com público 'ND'. Esses não se imputa: sem
> rótulo, não dá para treinar nem para avaliar. Saem da base de modelagem."

### Slide 10 — A evidência da ausência · 0:30

> "No gráfico completo, a maior ausência não é a que a gente acabou de citar: é
> **`uf2_bruto`, com sessenta e um e meio por cento** — que é a UF da coprodutora. É o mesmo
> fenômeno estrutural da produtora minoritária, visto por outro campo: sem coprodução, não
> há UF de coprodutora.
>
> E o que importa mais é o que está do meio para baixo: fora esses três campos, **a base é
> notavelmente completa.** Tudo o mais fica abaixo de dois por cento. Isso é incomum em
> dado administrativo e é uma coisa boa de dizer sobre esta base."

### Slide 11 — Outliers · 0:55

> "Sobre outliers, a gente tomou uma decisão de **não fazer**, e ela é deliberada.
>
> Se a gente aplicar o critério clássico de Tukey, o intervalo interquartil,
> **dezessete vírgula quatro por cento da base inteira** é marcado como outlier. Um em cada
> seis filmes. Esse número enorme não é sinal de que a base está suja — é sinal de que o
> critério não serve aqui. **O IQR pressupõe uma distribuição aproximadamente simétrica, e
> a nossa tem assimetria dez.** A distribuição de público é uma lei de potência: mediana de
> dois mil oitocentos, média de cento e quarenta e oito mil — a média é cinquenta e três
> vezes a mediana. Um por cento dos filmes concentra trinta e seis por cento de todo o
> público.
>
> E a gente verificou que os extremos são reais, não erro de digitação: o preço implícito
> do ingresso, que é renda dividida por público, tem mediana de onze reais e dezesseis, e
> nunca sai de uma faixa plausível. Nenhum valor negativo, nenhuma duplicata.
>
> Então a decisão é: **não remover.** Num regime de lei de potência, a cauda não é anomalia
> — **é o fenômeno que a gente quer aprender a reconhecer.** Remover os blockbusters seria
> remover justamente os casos que interessam. O tratamento certo é transformação
> logarítmica nos modelos que precisam dela, não exclusão."

### Slide 12 — Balanceamento, cardinalidade e redundância · 0:55

> "Três diagnósticos rápidos que viram três decisões.
>
> **Balanceamento:** como a Ana Laura mostrou, as classes já estão em cinquenta e cinquenta
> por construção do alvo. **Decisão: não aplicar balanceamento.** É a segunda decisão de
> 'não fazer' do trabalho, e ela é tão justificada quanto as de fazer.
>
> **Cardinalidade:** são **mil setecentas e trinta e oito** direções distintas e
> **quatrocentas e sessenta e sete** distribuidoras, muitas delas com um único filme na
> base inteira. Se a gente fizer one-hot encoding direto, a matriz explode e o modelo
> memoriza empresa em vez de aprender padrão. **Decisão: agrupar as categorias raras** numa
> categoria 'outras', com frequência mínima entre cinco e quinze — o que a gente mediu que
> custa menos de zero vírgula zero um de AUC e elimina trezentas e oitenta colunas.
>
> **Redundância:** `ano` e `filmes_no_ano` têm **rho de zero vírgula oitenta e seis** entre
> si, o que é esperado — mais filmes são lançados nos anos mais recentes. Num modelo
> linear, manter os dois infla variância; escolhemos um.
>
> E o `n_ufs` tem a **moda em noventa e sete por cento** dos registros: é praticamente uma
> constante. Variável quase constante não separa classe nenhuma. A gente mediu, e remover
> muda o AUC em zero. **Decisão: remover, por parcimônia** — e o ponto metodológico aqui é
> que agora a gente sabe disso por medição, e não por intuição."

> 🔗 "Só que existe um problema que nenhuma dessas decisões resolve, e ele é o mais grave
> do trabalho. A Laura vai falar dele."

---

## ATO 3 — Laura Virgínia

### Slide 14 — Vazamento de dados · 1:25

*Slide 13 cortado. Se não deu tempo de cortar, passem direto sem comentar.*

> "Obrigada. O problema mais grave desta base não é dado faltando nem outlier: é que
> **vários atributos que estão na base não existiriam no momento em que a gente precisa
> usar o modelo**.
>
> A frase que resume o critério é essa aí em cima: **estar na base não é a mesma coisa que
> estar disponível antes da estreia.** E reparem que isso **não** é um critério de
> correlação. Não é 'tirar o que correlaciona demais'. É um critério de **disponibilidade
> temporal** — o que é que existia no mundo no dia em que a decisão precisava ser tomada.
>
> Do lado direito estão os atributos que a gente teve que excluir. **`renda`** é o caso
> óbvio: renda é público vezes preço do ingresso; a correlação dela com o alvo é zero
> vírgula noventa e nove. Não é um atributo preditivo — **é a resposta escrita numa coluna
> diferente**. O mesmo vale para a renda deflacionada.
>
> **`max_salas`** é o caso mais sutil, e é o ponto mais discutível do nosso trabalho, então
> a gente prefere levantá-lo do que esperar a pergunta. Número de salas *parece*
> característica de lançamento — a nossa proposta inicial listava ele como atributo válido.
> Mas o campo que a ANCINE publica é o **máximo atingido durante toda a carreira do filme**,
> e distribuidora expande filme que está indo bem. Então esse número é, em parte,
> **consequência** do sucesso, não causa. Sem a data de estreia, a gente não consegue
> separar a parcela que foi decidida antes da parcela que reagiu ao desempenho. Na dúvida,
> escolhemos a versão que **não pode** inflar o resultado.
>
> E esse não é um argumento sem preço. A gente mediu: com o conjunto honesto, o AUC é
> **zero vírgula oitocentos e trinta e dois**. Acrescentando só o máximo de salas, sobe para
> **zero vírgula noventa e quatro** — mais zero vírgula onze. Acrescentando a renda, vai para
> **zero vírgula noventa e nove**. **Excluir os dois custa dezesseis pontos de AUC** — e é
> exatamente essa diferença que separa um resultado honesto de um resultado inflado.
>
> Do lado esquerdo está o que sobrevive. E uma escolha merece explicação: **por que
> fomento não é vazamento?** Porque **fomento público é aprovado antes de a obra existir**.
> É uma decisão de política pública sobre um projeto, não uma medida de desempenho — não
> tem como carregar bilheteria. Ele é legítimo.
>
> Com uma ressalva que a gente faz questão de declarar: o Fundo Setorial foi criado em
> 2006, então o indicador de FSA tem correlação de **zero vírgula cinco** com o ano — ele é,
> em parte, um marcador de filme recente. Não é vazamento, mas é confundimento, e por isso
> ele só entra no modelo junto com o ano."

### Slide 15 — De evidência a decisão · 0:45

*Não leiam a tabela. Digam o que ela é e comentem duas linhas.*

> "Esta tabela é o entregável desta fase. Cada linha da esquerda é uma **evidência** que a
> gente encontrou nos dados; cada linha da direita é a **decisão** de pré-processamento que
> decorre dela. Nenhuma decisão aqui veio de checklist — todas vieram de alguma coisa que a
> gente mediu.
>
> E a gente quer chamar atenção para as três últimas linhas, que são decisões de **não
> fazer**: não balancear, não remover outliers, não aplicar PCA. Num trabalho de
> pré-processamento, é fácil aplicar tudo o que se aprendeu na disciplina e apresentar como
> rigor. A gente acha que justificar por que **não** aplicar exige mais evidência do que
> aplicar — e as três estão justificadas: classes já equilibradas, cauda que é o fenômeno,
> e só onze numéricas úteis, num caso em que o crescimento de dimensão vem da codificação
> categórica e não delas."

### Slide 16 — Conclusão · 1:25

*A tela mais dependente da fala. Comecem pelo aviso, não pelos números.*

> "E aí a gente chega no resultado que dá título a esta conclusão.
>
> Antes dos números, um aviso: **os dois AUCs que estão aqui vieram do mesmo algoritmo, uma
> floresta aleatória, com o mesmo protocolo.** A gente não trocou de modelo. O que muda
> entre a esquerda e a direita são só três coisas — e todas as três são decisões que a
> gente tomou.
>
> **À esquerda, zero vírgula novecentos e noventa e cinco.** Praticamente perfeito. Esse é
> o resultado que sai se a gente seguir o caminho fácil: alvo pela mediana global,
> atributos posteriores à estreia incluídos, e validação cruzada aleatória.
>
> E cada uma dessas três decisões é um atalho diferente. Com o **alvo global**, o modelo lê
> o calendário — vocês viram, oitenta e seis por cento contra vinte e seis. Com a **renda**,
> ele lê a resposta. E com a **validação aleatória**, ele vê o futuro: num k-fold embaralhado,
> filmes de 2019 vão parar no treino e filmes de 2015 no teste, e o modelo aprende
> tendências que, no uso real, ainda não teriam acontecido.
>
> **À direita, zero vírgula setecentos e vinte e cinco.** Alvo relativo ao ano, só atributos
> disponíveis antes da estreia, e partição temporal — treino até 2017, teste de 2018 em
> diante, que é a única partição que corresponde ao uso real, porque o uso real é prever um
> filme que ainda não estreou.
>
> A diferença é de quase **zero vírgula vinte e sete de AUC**, e ela é decomponível: o alvo
> relativo custa seis centésimos, excluir os atributos posteriores custa dezesseis, e a
> validação temporal custa nove.
>
> **E o ponto do trabalho é este: nenhuma linha de código distingue as duas versões.** As
> duas rodam sem erro, as duas produzem uma métrica bonita, e a errada produz uma métrica
> mais bonita. A diferença está inteiramente em decisões que são tomadas antes de o modelo
> existir — na definição do alvo, na escolha dos atributos e no desenho da validação.
>
> Então, voltando à pergunta com que a gente abriu: **é possível prever o sucesso de um
> filme brasileiro antes da estreia?** A resposta honesta é **parcialmente, sim**. Zero
> vírgula setenta e dois é bem acima do acaso, que seria zero vírgula cinco, e bem longe da
> certeza. É um resultado modesto — e ele é modesto porque é verdadeiro."

*Se alguém quiser a versão de uma frase, é essa: um resultado maior não significa um
modelo melhor; significa, muitas vezes, um problema mais fácil do que o real.*

### Slide 17 — Fechamento · 0:10

> "É isso. A base, o notebook executado e o relatório completo estão no repositório.
> Obrigada — e a gente está à disposição para as perguntas."

---

# PARTE 4 — OS RESULTADOS, EXPLICADOS

Para cada achado: o que encontramos, o que significa, por que importa, que conclusão
permite, e qual o limite da interpretação.

### 1. O mercado mudou de natureza (slides 3–4)

| | |
|---|---|
| **O que** | 1995: 14 lançamentos, mediana de 14.230. 2024: 197 lançamentos, mediana de 933. |
| **Significa** | O filme mediano de hoje é um objeto diferente do filme mediano de 1995 — muito mais documentário e circuito limitado. |
| **Por que importa** | Invalida qualquer limiar fixo de sucesso aplicado sobre 30 anos. |
| **Conclusão** | O alvo precisa ser **relativo ao ano**. |
| **Limitação** | É estatística descritiva, não causal. A gente **não** demonstrou *por que* a composição mudou — a explicação por documentário é plausível e coerente com os dados, mas não foi testada formalmente. Não digam "provamos que"; digam "é consistente com". |

### 2. A definição de sucesso (slides 5–6)

| | |
|---|---|
| **O que** | Mediana global: 85,6% de sucesso nos 1990s contra 26,3% nos 2020s. Mediana do ano: 49–50% em todas as décadas. Correlação do ano com o alvo: −0,364 → +0,002. |
| **Significa** | Com a definição global, o rótulo é quase uma função do ano. Com a relativa, o ano deixa de informar. |
| **Por que importa** | É a diferença entre um modelo que aprende cinema e um que aprende calendário. |
| **Conclusão** | `sucesso_no_ano` como alvo principal. |
| **Limitação** | O alvo relativo tem um custo: ele **descarta a informação de nível**. Um filme de 2024 com 5.000 espectadores vira "sucesso", e um de 1997 com 20.000 vira "fracasso" — mesmo o segundo tendo tido cinco vezes mais público. A gente trocou uma pergunta ("é um filme grande?") por outra ("é grande para o seu ano?"). A segunda é mais justa e menos espetacular. **Isso é uma escolha, e precisa ser defendida como escolha, não como correção óbvia.** |

### 3. Associação das variáveis (slides 7–8)

| | |
|---|---|
| **O que** | Máximo honesto: projetos de incentivo, rho = +0,274. Gênero, V de Cramér = 0,338. `ano` = +0,002. |
| **Significa** | Nenhum atributo isolado chega perto de explicar sucesso; o sinal é distribuído e fraco. |
| **Por que importa** | Calibra a expectativa para a Entrega 2 — AUC na faixa de 0,7 é o teto realista, não um fracasso. |
| **Conclusão** | O ganho virá de **combinação** de atributos e de boa codificação das categóricas, não de um preditor forte. |
| **Limitação** | Spearman e V de Cramér são medidas **marginais e bivariadas**: só capturam relação de um atributo por vez, e só relação monotônica no caso do Spearman. Um atributo com rho ≈ 0 pode ser muito informativo **em interação** com outro. Correlação baixa não autoriza descartar variável. |

### 4. Valores ausentes (slides 9–10)

| | |
|---|---|
| **O que** | 61,5% `uf2_bruto`, 59,9% produtora minoritária, 23,3% população, 2,13% `max_salas`, 0,84% público. |
| **Significa** | Quatro mecanismos distintos: estrutural, de junção, possivelmente MNAR, e alvo faltante. |
| **Por que importa** | Cada mecanismo pede tratamento diferente; imputar tudo com a mediana seria errado três vezes. |
| **Conclusão** | Categoria própria para o estrutural; indicadora de ausência para o MNAR; exclusão para os 22 filmes sem alvo. |
| **Limitação** | **A hipótese MNAR de `max_salas` é fraca.** Verificado na base: só 37 filmes com alvo não têm o campo, e a mediana de público deles é 3.400 contra 2.753 dos demais — diferença pequena e em direção *contrária* à esperada. Se perguntarem, digam "é indício com n = 37, não conclusão". Não afirmem a direção. |

### 5. Outliers (slide 11)

| | |
|---|---|
| **O que** | O IQR marca 17,4% da base. Assimetria 10,0; média 53× a mediana; 1% dos filmes com 36% do público. |
| **Significa** | O critério de Tukey falha porque pressupõe simetria; a distribuição é de lei de potência. |
| **Por que importa** | Remover a cauda removeria exatamente os casos que o projeto quer prever. |
| **Conclusão** | Não remover; tratar com `log1p` nos modelos que precisam. |
| **Limitação** | Manter a cauda tem um preço: modelos lineares ficam sensíveis a esses pontos, e a métrica pode ser dominada por poucos filmes. A defesa não é "outlier nunca se remove" — é "**nesta base e para esta pergunta**, a cauda é o alvo". |

### 6. Balanceamento (slides 6 e 12)

| | |
|---|---|
| **O que** | 50,0% / 49,7%. |
| **Significa** | O equilíbrio é **artefato da construção do alvo** (corte pela mediana), não propriedade do mundo. |
| **Por que importa** | Aplicar SMOTE aqui não corrigiria nada e adicionaria pontos sintéticos sem motivo. |
| **Conclusão** | Não balancear. |
| **Limitação** | Vale só para este alvo. Se a Entrega 2 mudar o limiar — por exemplo, "acima do percentil 90 do ano" —, o desbalanceamento aparece e a decisão se inverte. **Digam isso**: a decisão é condicional ao alvo, não uma posição geral sobre SMOTE. |

### 7. Cardinalidade e redundância (slide 12)

| | |
|---|---|
| **O que** | 1.738 direções, 467 distribuidoras (287 com um único filme), `ano` × `filmes_no_ano` rho = 0,86, `n_ufs` com moda em 97,1%. |
| **Significa** | One-hot direto explodiria a dimensão e levaria à memorização de entidade. |
| **Por que importa** | Define a estratégia de codificação, que é a decisão de maior impacto para a Entrega 2. |
| **Conclusão** | Agrupar raras (corte 5–15: −0,009 de AUC, −380 colunas); escolher um entre `ano` e `filmes_no_ano`; remover `n_ufs`. |
| **Limitação** | Agrupar categorias raras **apaga distribuidoras pequenas de nicho** que podem ter perfil próprio. O custo medido em AUC é quase zero, mas o custo em interpretabilidade não é. |

### 8. Vazamento (slide 14)

| | |
|---|---|
| **O que** | Honesto 0,832 → +`max_salas` 0,940 (+0,108) → +`renda` 0,993 (+0,161) → ambos 0,995. |
| **Significa** | Os dois atributos carregam desempenho pós-estreia; `renda` é literalmente a resposta (rho = 0,99). |
| **Por que importa** | É a diferença entre um número publicável e um número inflado. |
| **Conclusão** | Excluir ambos; o critério é **disponibilidade temporal**, não correlação. |
| **Limitação** | **`max_salas` é uma decisão de julgamento, não um fato.** Ele mistura decisão de lançamento (legítima) com reação ao desempenho (vazamento), e sem a data de estreia as duas parcelas não são separáveis. A postura correta é a que vocês tomaram — excluir e publicar quanto valeria —, mas apresentem como escolha conservadora, não como verdade. |

### 9. Os dois cenários — 0,995 e 0,725 (slide 16)

| | |
|---|---|
| **O que** | Caminho fácil 0,995; cenário coerente com o uso real 0,725. Decomposição: alvo −0,062, atributos posteriores −0,163, partição temporal −0,087. |
| **Significa** | 0,995 é alto porque o problema foi tornado mais fácil, não porque o modelo é bom. |
| **Por que importa** | É a tese do trabalho e o que a banca deve levar embora. |
| **Conclusão** | Um resultado maior não significa um modelo melhor; significa, com frequência, um problema diferente. |
| **Limitação** | **Os dois números não são estritamente comparáveis** — a esquerda prevê `sucesso_global` e a direita prevê `sucesso_no_ano`, que são alvos diferentes. Antecipem isso: *"é justamente esse o ponto — o da esquerda é um problema diferente, e mais fácil, e menos útil."* Além disso, os dois vêm de **um** protocolo fixo com semente fixa; são medidas de **diferença entre versões da base**, não o desempenho de um modelo escolhido. A modelagem é a Entrega 2. |

### 10. Validação temporal (slide 16)

| | |
|---|---|
| **O que** | 5-fold aleatório 0,832 contra treino<2018/teste≥2018 0,745, no mesmo alvo global: +0,087 de otimismo. |
| **Significa** | A partição aleatória mede uma tarefa que ninguém executa: interpolar no meio de uma série que já aconteceu. |
| **Por que importa** | O uso real é extrapolar para o futuro; a métrica tem que medir isso. |
| **Conclusão** | Partição temporal, treino até 2017. |
| **Limitação** | Uma única divisão em 2018 é **um ponto de teste, não uma distribuição**. O ideal seria validação temporal deslizante, com vários cortes. E o período de teste (2018–2024) contém a pandemia, o que pode tanto inflar quanto deprimir o número. Vale declarar. |

---

# PARTE 5 — PERGUNTAS QUE O PROFESSOR PODE FAZER

**1. Por que AUC, e não acurácia?**
Porque AUC independe do limiar de decisão e da proporção de classes — ela mede a
capacidade de **ordenar** os filmes por probabilidade de sucesso, que é exatamente o uso
real: não decidimos "sim ou não", priorizamos projetos. Também usamos F1, acurácia e
matriz de confusão no relatório; a AUC é a métrica de comparação porque é a única que
continua comparável quando a proporção de positivos muda entre os recortes temporais.

**2. Por que o modelo com AUC 0,995 pode estar enganando?**
Porque ele acerta por três motivos ilegítimos somados: o alvo global faz ele ler o ano de
lançamento; a `renda` é o público multiplicado pelo preço do ingresso, com correlação
0,99 — é a resposta; e o k-fold aleatório coloca filmes de 2019 no treino e de 2015 no
teste, deixando ele enxergar o futuro. Retirados os três, o mesmo algoritmo, no mesmo
protocolo, entrega 0,725.

**3. O que é data leakage neste projeto, concretamente?**
É usar atributo que existe na base mas **não existiria no momento da predição**. O critério
é disponibilidade temporal, não correlação alta. `renda` e `renda_deflacionada_2024` só
existem depois que o filme rodou; `max_salas` é o máximo atingido durante a carreira, e
distribuidora expande filme que vai bem. Medimos o custo de excluir: 0,16 de AUC.

**4. Por que não remover os outliers?**
Porque não são erros — são os blockbusters, e são o fenômeno que queremos prever. A
distribuição é de lei de potência, com assimetria 10 e 1% dos filmes concentrando 36% do
público; o critério de Tukey pressupõe simetria e por isso marca 17,4% da base. Validamos
que os extremos são plausíveis: o preço implícito do ingresso tem mediana de R$ 11,16 e
nunca sai de faixa razoável. O tratamento é `log1p` nos modelos que precisam, não exclusão.

**5. Por que não aplicar balanceamento?**
Porque não há desbalanceamento: o corte pela mediana produz 50,0% contra 49,7% **por
construção**. SMOTE aqui seria ritual. Registramos como hipótese de *não fazer*. Ressalva
que damos de graça: se a Entrega 2 mudar o limiar — digamos, percentil 90 do ano —, o
desbalanceamento aparece e a decisão se inverte.

**6. Por que validação temporal?**
Porque o uso real é prever um filme que ainda não estreou, o que é extrapolação para o
futuro. O k-fold aleatório mede interpolação dentro de um passado já conhecido — uma tarefa
que ninguém executa. Medimos a diferença: o aleatório é 0,087 otimista. A limitação que
reconhecemos é que usamos um único corte, em 2018; o ideal seria validação deslizante com
vários cortes.

**7. Por que o ano deixou de ter correlação relevante?**
Porque mudamos o alvo, não os dados. Com a mediana global, um limiar fixo sobre um mercado
cujo público mediano caiu 15 vezes classifica quase todo filme antigo como sucesso — daí
rho = −0,364. Com a mediana **do próprio ano**, cada filme é comparado com os que
estrearam junto com ele, e o ano perde poder explicativo sobre o rótulo: rho = +0,002.

**8. Como vocês definiram sucesso?**
Público acima da **mediana do ano de lançamento** do filme. Consideramos três alternativas:
mediana global (descartada, embute o ano), limiar absoluto em espectadores (arbitrário e
com o mesmo problema), e retorno sobre orçamento (impossível — a ANCINE não publica
orçamento). A mediana do ano é comparação entre pares que disputaram o mesmo mercado.

**9. Que informação estaria realmente disponível antes da estreia?**
Gênero; se o projeto recebeu fomento e de que tipo (FSA, leis de incentivo, ou os dois) —
e isso é legítimo porque fomento é **aprovado antes de a obra existir**; o histórico da
direção, da produtora e da distribuidora, contado só com filmes anteriores àquele; a UF
majoritária; e se é coprodução. Tudo o que mede desempenho está fora.

**10. O que vocês fariam na próxima etapa?**
Três coisas, nessa ordem. Primeiro, **codificação das categóricas**, porque gênero é o
atributo mais associado ao alvo e distribuidora tem 467 níveis — é onde está o maior ganho
disponível. Segundo, **validação temporal deslizante** com vários cortes, em vez de um único
em 2018. Terceiro, buscar atributos pré-estreia que não temos: duração (a ANCINE não
publica; o Wikidata teria, mas não era alcançável do nosso ambiente) e elenco. E
compararíamos modelos com uma linha de base honesta, sempre reportando o cenário temporal.

**Bônus — "vocês mediram AUC; isso não é modelagem, fora do escopo de uma EDA?"**
O modelo aqui é **instrumento de medida**, como um termômetro. Rodamos **um** protocolo
fixo, com todo o pré-processamento dentro dos folds, e reportamos sempre a **diferença**
entre duas versões da base — nunca o desempenho de um modelo escolhido. A base entregue
em `data/processed/filmes.csv` continua sem imputação, sem remoção de outlier e sem
codificação, como uma entrega exploratória exige.

**Bônus — "por que a base vai só até 2024?"**
Porque a edição 1995–2025 não existe. Sondamos as URLs: as de 2025 devolvem HTTP 404. A
publicação mais recente é a `1995 a 2024r`, retificada.

---

# PARTE 6 — VEREDITO FINAL

## NOTA DA APRESENTAÇÃO

### **7,5 / 10** — como os slides estão hoje.
### **9,0 / 10** — com as duas correções obrigatórias e o roteiro da Parte 3.

| Critério | Nota | Comentário |
|---|---|---|
| Conteúdo | 9,0 | Acima do esperado para a disciplina. O achado do alvo é original e bem construído. |
| Rigor técnico | 9,5 no repositório / **6,0 nos slides** | O repositório é excelente e mede tudo. O slide 16 exibe um número que o repositório não sustenta — e isso pesa muito num trabalho cujo tema é rigor. |
| Narrativa | 8,0 | A espinha 3→4→5→6 é ótima; o final (9–15) perde energia e o slide 2 não é respondido. |
| Clareza | 7,0 | Conceitos certos, mas várias decisões aparecem sem a evidência ao lado. |
| Visual | 6,0 | Template bom e consistente; erros de edição visíveis (linha duplicada, spell-check, quebra de palavra) e figuras sem frase de conclusão. |
| Adequação aos 15 min | 6,5 | Os slides sustentam ~7 minutos de fala. Sem o roteiro, sobra tempo. |

## O QUE ESTÁ MUITO BOM

- **A tese.** "A definição do alvo decide se o problema é sobre cinema ou sobre calendário"
  é um achado de verdade, não um exercício. Poucos grupos de graduação chegam nisso.
- **As decisões de NÃO fazer**, com justificativa empírica. Não balancear, não remover
  outlier, não aplicar PCA — justificadas, e não omitidas. Isso é maturidade.
- **A definição de vazamento por disponibilidade temporal**, e não por correlação. É o
  enquadramento correto, e é o que um professor de ML procura.
- **A honestidade sobre `max_salas`.** Vocês excluíram o atributo que inflaria o resultado e
  publicaram quanto ele valeria. Isso é a coisa certa a fazer e merece ser dita em voz alta.
- **O slide 6** — melhor slide do deck, e por sorte é também o mais importante.
- **A rastreabilidade.** Cada número dos slides (fora o 0,696) confere com o notebook e com
  `data/processed/filmes.csv`. Eu verifiquei −0,364, +0,002, 2.806, 148.399, 17,4%, 1.738,
  467, 0,86, 97,1%, 59,9%, 23,3%, 2,13%, 0,84%, 0,338, 0,320, 0,274, e as quatro linhas de
  `sensibilidades_s1.csv`. Todos batem.

## O QUE PRECISA SER CORRIGIDO ANTES DE APRESENTAR

**Obrigatório (15 minutos de trabalho):**

1. **Slide 16 — trocar 0,696 por 0,725.** Ou reproduzir 0,696 no notebook antes de
   apresentar. É o item de maior risco do trabalho inteiro.
2. **Slide 2 — apagar a linha "Restrição" duplicada.**

**Alto retorno (mais uma hora):**

3. **Slide 2 — acrescentar a definição de sucesso** ("público acima da mediana do ano de
   lançamento") **e o tamanho da base** (2.626 filmes, 1995–2024, 35 atributos, 5 fontes
   públicas). O espaço vazio já está lá.
4. **Cortar o slide 13** (repetição do 6).
5. **Slide 14 — acrescentar "+0,16 de AUC"** ao lado da coluna "depois da estreia". Um
   vazamento com preço é resultado; sem preço, é opinião.
6. **Slide 16 — acrescentar a resposta à pergunta do slide 2**: "sim, parcialmente — AUC
   0,725, acima do acaso e longe da certeza."
7. **Slide 15 — recapturar a tabela sem os sublinhados vermelhos de corretor ortográfico.**

**Se sobrar tempo:**

8. **Acrescentar `reports/figuras/fig01-distribuicao-publico.png`** antes do slide de
   outliers. A figura já existe, pronta, e é a evidência que falta para a decisão mais
   contra-intuitiva do trabalho.
9. **Uma frase grande de conclusão em cada slide de figura** (4, 8, 10). Da quinta fileira
   ninguém lê o título interno de um gráfico do matplotlib.
10. **Slide 14 — consertar a quebra de `renda_deflacionada_2024`.**
11. **Fundir os slides 11 e 12** sob o título "Três decisões de não fazer".

## O QUE NÃO PRECISA SER ALTERADO

Para não gastarem tempo à toa:

- **O template preto com ícones de cinema.** Está consistente, é legível e é apropriado ao
  tema. Não mexam.
- **A tabela do slide 3.** É o melhor objeto visual do deck.
- **A figura do slide 6.** Rótulos, linha de referência e cores estão certos. Não redesenhem.
- **O slide 8.** Dois painéis com escalas separadas é exatamente o certo. Não juntem.
- **A tabela do slide 15** (fora o spell-check). O conteúdo está bom e o formato também.
- **A estrutura de duas colunas do slide 16.** Funciona. O que falta é fala, não desenho.
- **Todos os percentuais dos slides 9, 11 e 12.** Conferidos contra a base. Estão corretos.
- **A ordem geral dos slides 1 a 8.** A narrativa funciona.
- **O nível de detalhe.** Não acrescentem mais números. O deck precisa de mais *explicação*,
  não de mais *dado*.

## VEREDITO

> **"Se vocês apresentassem exatamente assim, estaria bom o suficiente para um pitch
> universitário de 15 minutos?"**

**Não — mas por pouco, e o que falta é barato de consertar.**

Faltam três coisas, e só três:

1. **Um número que não se sustenta.** O slide 16 diz AUC 0,696; o notebook que vocês vão
   entregar diz 0,725. Num trabalho cuja tese é "cuidado com o número bonito", apresentar
   um número que a própria evidência não confirma é o erro mais caro possível. **Isso
   sozinho já reprovaria o pitch diante de um professor que abrisse o notebook.**

2. **Um erro de edição visível** — a linha duplicada no slide 2, na tela por um minuto, no
   começo, quando a banca está formando a primeira impressão.

3. **Sete a oito minutos de conteúdo falado que os slides não sustentam sozinhos.** O deck,
   lido como está, dura metade do tempo. A Parte 3 resolve isso.

Corrigidos os itens 1 e 2 — que somam quinze minutos de trabalho — e estudado o roteiro da
Parte 3, **esta apresentação fica acima da média da turma com folga confortável.** O
conteúdo já está lá; o que falta é não deixar um número solto derrubar um trabalho que, no
resto, é rigoroso.

---

# PARTE 7 — ROTEIRO FINAL, VERSÃO DE PALCO

Uma linha por ideia. Cada linha é uma coisa que se fala. Para imprimir e levar.
**Total: 14:25 falados + trocas ≈ 15:00.**

## ANA LAURA — 5:30 · relógio: terminar aos **5:30**

**S1 · Capa — 0:40**
- Mediano: **2.806** espectadores. Maior da série: **12,2 milhões**. **4.342 vezes**.
- "Dá para saber de que lado um filme cai — antes de estrear?"

**S2 · A pergunta — 1:10**
- Classificação binária.
- **Sucesso = público acima da mediana DO PRÓPRIO ANO.** ← guardem o "do próprio ano".
- Restrição: só o que existia **antes da estreia**. Cenário real = produtor decidindo.
- Base: **2.626 filmes · 1995–2024 · 35 atributos · 5 fontes públicas** (ANCINE, FSA,
  incentivo, IPCA, IBGE).

**S3 · O mercado mudou — 0:35**
- 1995: **14** lançamentos, mediana **14.230**. 2024: **197**, mediana **933**.
- **14× mais lançamentos, 15× menos público.**
- Não é crise: é **composição** — entrou documentário e circuito limitado.

**S4 · A evidência — 0:55**
- Esquerda: crescimento, pandemia, 2024 recorde.
- Direita: **eixo log** — em linear a queda some.
- 10⁵ em 2003 → menos de 10³ em 2020: **duas ordens de grandeza**.
- → "Filme de 1997 e filme de 2023 não competem no mesmo mercado."

**S5 · A definição — 0:30**
- Óbvio: mediana da base inteira → classes 50/50, parece impecável.
- Mas com a mediana caindo 15×, limiar fixo mede **década**, não qualidade.

**S6 · O ACHADO — 1:40** ⏱ *não corram*
- Laranja = mediana global. Azul = mediana do ano.
- **86% nos 1990s × 26% nos 2020s.** Sessenta pontos.
- → o rótulo é função do **ano**. Modelo acha o atalho e **aprende calendário, não cinema**.
- Azul: 49 / 50 / 50 / 50. Reta.
- Correlação do ano com o alvo: **−0,364 → +0,002**.
- **"Nenhuma linha de código distingue as duas. Só a definição do alvo."**
- Bônus: logo, **não há desbalanceamento** — 50/50 por construção. SMOTE seria cumprir tabela.
- 🔗 "Tirando o calendário, o que sobra? Ana Raquel."

## ANA RAQUEL — 4:30 · relógio: terminar aos **10:00**

**S7 · O que carrega informação — 0:45**
- ⚠️ **Escalas diferentes**: V de Cramér [0,1] para categóricas; Spearman [−1,1] para numéricas.
- Spearman e não Pearson: **assimetria 10**.
- Gênero V = 0,338 (categórico) · incentivo rho = 0,274 (numérico). **Não é um ranking só.**

**S8 · A evidência — 1:10**
- Comecem pelo **fim** da lista: `ano` **+0,002**, `filmes_no_ano` **+0,003**. Barras invisíveis.
- → "Lá era argumento. Aqui é medida."
- Topo: incentivo 0,274 · direção 0,193 · distribuidora 0,183. **Nenhum chega a 0,3.**
- "Se um atributo sozinho explicasse sucesso, não existiria indústria de cinema."
- Direita: **gênero 0,338 é o mais associado da base**.
- → **codificar categóricas importa mais que transformar numéricas.**

**S9 · Ausentes — 0:55**
- **59,9% produtora minoritária** = ausência **estrutural**. Não houve coprodução. Categoria própria.
- **23,3% população** = falha de **junção** com o IBGE. Problema nosso, não do filme.
- **2,13% max_salas** = possivelmente **MNAR** → indicadora de ausência. *(se perguntarem: n = 37, é indício)*
- **0,84% público** = **sem alvo**. 22 filmes com "ND". Saem.

**S10 · A figura — 0:30**
- Topo real é **`uf2_bruto`, 61,5%** = UF da coprodutora, mesmo fenômeno estrutural.
- Fora esses três, **tudo abaixo de 2%** — base notavelmente completa.

**S11 · Outliers — 0:55**
- IQR marca **17,4%**. Um em cada seis.
- Não é base suja: **IQR pressupõe simetria; a assimetria é 10**.
- Mediana 2.806 × média 148.399 (**53×**). **1% dos filmes = 36% do público.**
- Extremos validados: ingresso mediano **R$ 11,16**, nada negativo.
- **Decisão: não remover. Num regime de lei de potência a cauda é o fenômeno.** Trata-se com log.

**S12 · Três decisões — 0:55**
- **Balanceamento:** 50/50 por construção → **não aplicar**.
- **Cardinalidade:** 1.738 direções, 467 distribuidoras → **agrupar raras** (−0,009 AUC, −380 colunas).
- **Redundância:** ano × filmes_no_ano **rho = 0,86** → escolher um.
- **`n_ufs` moda 97,1%** → remover. Medido: **AUC muda zero**. "Sabemos por medição, não por intuição."
- 🔗 "Mas existe um problema que nada disso resolve. Laura."

## LAURA VIRGÍNIA — 3:45 · relógio: terminar aos **14:00**

**S14 · Vazamento — 1:25** ⏱ *o segundo pico*
- **"Estar na base ≠ estar disponível antes da estreia."**
- ⚠️ Critério é **disponibilidade temporal**, NÃO correlação alta.
- `renda` = público × preço. **rho 0,99. É a resposta em outra coluna.**
- `max_salas` = **máximo durante a carreira**. Distribuidora expande filme que vai bem →
  em parte **consequência**, não causa. Sem data de estreia não dá para separar.
  **"Na dúvida, a versão que não pode inflar."**
- **Preço medido: honesto 0,832 → +max_salas 0,940 → +renda 0,993. Excluir custa 0,16.**
- **Por que fomento é legítimo: é aprovado ANTES de a obra existir.**
- Ressalva espontânea: FSA criado em 2006 → **rho 0,51 com o ano**. Confundimento, não
  vazamento. Só entra junto com o ano.

**S15 · Evidência → decisão — 0:45**
- Não leiam a tabela. "Cada linha da esquerda é evidência; cada uma da direita, decisão."
- Destaquem as três de **não fazer**: não balancear, não remover outlier, não aplicar PCA.
- "Justificar por que **não** aplicar exige mais evidência do que aplicar."

**S16 · Conclusão — 1:25** ⏱ *o fecho*
- ⚠️ Primeiro o aviso: **mesmo algoritmo, mesmo protocolo.** Só mudam três decisões.
- **0,995** = alvo global (lê o calendário) + renda (lê a resposta) + k-fold aleatório (vê o futuro).
- **0,725** = sucesso_no_ano + só pré-estreia + treino até 2017 / teste de 2018.
- Diferença **0,27**, decomposta: alvo **−0,062** · atributos **−0,163** · partição **−0,087**.
- **"Nenhuma linha de código distingue as duas versões."**
- Fechem respondendo o slide 2: **"É possível? Parcialmente, sim. 0,725 é bem acima do
  acaso e longe da certeza. É modesto porque é verdadeiro."**

**S17 · 0:10**
- "Base, notebook e relatório estão no repositório. Obrigada."

## Cartão de emergência

**Se estourar o tempo, cortem nesta ordem** — tela inteira, nunca acelerando a fala:

| ordem | corte | ganha |
|---|---|---|
| 1º | S10 — a figura confirma o S9; digam só "uf2_bruto é 61,5%, mesmo fenômeno" | 0:25 |
| 2º | S7 — pulem direto para o S8 e digam a ressalva das escalas lá | 0:40 |
| 3º | S15 — uma frase só: "cada evidência virou uma decisão, três delas de não fazer" | 0:30 |
| 4º | S4 — só o eixo log e a frase "não competem no mesmo mercado" | 0:30 |

**Intocáveis: S2 (a definição de sucesso), S6, S14 e S16.** São as quatro telas que sustentam a nota.

**Se sobrar tempo**, três coisas que valem ser ditas e não estão no roteiro:
1. A coleta: o portal devolve HTML em vez do CSV; os arquivos de fomento estão num host não linkado.
2. O gradiente do fomento: **33%** de sucesso sem fomento contra **77%** com FSA e incentivo juntos.
3. Gênero: animação e ficção com mediana uma a duas ordens acima de documentário — mas as
   caixas se sobrepõem: **gênero informa, não determina**.

## Checklist de ensaio

- [ ] Cronometrar **cada ato separadamente**. O erro clássico é a primeira pessoa gastar
      5 minutos nos dois primeiros slides.
- [ ] Ensaiar as **três passagens de bastão em voz alta**. É onde grupo trava.
- [ ] **Cada uma responde as perguntas do seu ato.**
- [ ] Números de cor: **2.626 × 35** · **2.806** · **4.342×** · **86% × 26%** ·
      **−0,364 → +0,002** · **0,16 de AUC** · **0,995 × 0,725**.
- [ ] Notebook aberto e **já executado** antes de começar.
- [ ] Conferir uma última vez: **o slide 16 diz 0,725?**
