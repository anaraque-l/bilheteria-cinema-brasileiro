# Storyboard da Entrega 1 — as 13 telas, uma a uma

**CIN0144 · AMCD · CIn/UFPE — Grupo 11**
As 17 telas atuais reorganizadas em **13**: o texto exato de cada tela, o que muda em
relação ao que existe hoje, e por quê. Tempo falado: **14:30**.

Companion de [`revisao-e-roteiro-15min.md`](revisao-e-roteiro-15min.md), que traz a
avaliação e o roteiro de fala. Todos os números foram conferidos contra o notebook
executado, `reports/sensibilidades_s1.csv` e `data/processed/filmes.csv`.

---

## O princípio de organização

O deck atual alterna telas de **texto sem evidência** e telas de **figura sem palavra
nenhuma do grupo**. É isso que o faz parecer desorganizado, e é isso que gasta 17 telas
para 15 minutos. A correção é um sistema de dois arquétipos, e nada fora deles:

| Arquétipo | Estrutura fixa | Quando usar |
|---|---|---|
| **Evidência** | título · faixa de números · **figura de largura total** · uma frase de conclusão em corpo grande | sempre que existir uma figura |
| **Decisão** | título · subtítulo com o critério · colunas ou linhas **evidência → decisão** · faixa inferior com o peso medido | sempre que a tela defender uma escolha de pré-processamento |

Mais quatro regras, que respondem sozinhas por quase toda a impressão de organização:

| Regra | Por quê |
|---|---|
| **Tudo alinhado à esquerda**, em todas as telas, inclusive a capa | Hoje títulos centralizados convivem com corpo à esquerda. Um único eixo vertical é o que o olho lê como "organizado". |
| **Uma conclusão por tela**, sempre no rodapé, sempre no mesmo corpo | A banca aprende onde olhar depois da segunda tela e para de procurar. |
| **Código de cor herdado dos gráficos**: laranja = o caminho fácil, o que sai, o alvo global · azul = o honesto, o que fica, o alvo do ano | As figuras já usam essas duas cores. Estendê-las ao texto faz o público decodificar cada gráfico antes de vocês explicarem. |
| **Rodapé discreto** em todas as telas: `Grupo 11 · 7/13` | Dá à banca a noção de progresso, o que evita a pergunta "quanto falta?". |

---

# ATO 1 — O problema e o alvo

**Ana Laura · 4:55**

## Tela 1 — Capa

`Capa` · vem de: slide 1 · **0:40**

**O texto exato da tela**

- *Rodapé superior* — CIN0144 · Aprendizado de Máquina e Ciência de Dados · CIn/UFPE
- *Título* — PREVISÃO DE SUCESSO DE FILMES BRASILEIROS ANTES DA ESTREIA
- *Linha de tese (nova)* — Um modelo com AUC 0,99 que não aprendeu nada sobre cinema.
- *Autoras* — Ana Laura Barboza Oliveira dos Santos · Ana Raquel Rodrigues · Laura Virgínia do Nascimento Fonseca
- *Canto inferior* — Análise Exploratória de Dados — Entrega 1

**O que muda**

- [ ] Alinhar tudo à esquerda. Hoje está centralizado, e nenhuma outra tela é centralizada — é a primeira quebra de consistência do deck.
- [ ] Acrescentar a **linha de tese**. Uma capa que já entrega o achado prende a banca antes da primeira palavra.
- [ ] Acrescentar a identificação da disciplina no topo.

> **Por quê.** A capa é a única tela que a banca olha sem ouvir ninguém falar. Ela deve entregar, sozinha, o assunto e o achado.

## Tela 2 — É possível prever o sucesso antes da estreia?

`Decisão` · vem de: slide 2 (corrigido) · **1:15**

**O texto exato da tela**

- *Título* — É POSSÍVEL PREVER O SUCESSO ANTES DA ESTREIA?
- *Coluna 1 — TAREFA* — Classificação binária. / **Sucesso = público acima da mediana do ano de lançamento.**
- *Coluna 2 — RESTRIÇÃO* — Só informação que existia **antes da estreia**. / O cenário real é um produtor decidindo financiar um projeto que ainda não existe.
- *Coluna 3 — BASE* — **2.626 filmes · 1995–2024 · 35 atributos** / ANCINE · FSA · Leis de incentivo · IPCA/BCB · IBGE — cinco fontes públicas.

**O que muda**

- [ ] **Apagar a linha “Restrição” duplicada.** Hoje ela aparece duas vezes na mesma tela. Correção obrigatória.
- [ ] Escrever a **definição de sucesso**. Hoje ela não está em nenhum slide — o público só a descobre pela legenda de um gráfico.
- [ ] Acrescentar o **tamanho e as fontes da base**. Hoje o deck inteiro nunca diz quantos filmes são.
- [ ] Usar as três colunas: a metade inferior da tela está vazia hoje.

> **Por quê.** Numa banca de Computação, “o que é o alvo” e “quantos dados são” são as duas primeiras perguntas. Respondidas aqui, nenhuma volta depois.

## Tela 3 — O mercado mudou de natureza

`Evidência` · figura `reports/figuras/fig02-evolucao-anual.png` · vem de: slides 3 + 4, fundidos · **1:10**

**O texto exato da tela**

- *Título* — O MERCADO MUDOU DE NATUREZA
- *Faixa de números* — **1995** — 14 lançamentos · mediana 14.230 &nbsp;&nbsp; **2024** — 197 lançamentos · mediana 933
- *Figura* — reports/figuras/fig02-evolucao-anual.png, largura total
- *Frase de conclusão* — **14× mais lançamentos, 15× menos público por filme.** Não é crise — é composição: entrou documentário e circuito limitado. *(eixo da direita em escala log)*

**O que muda**

- [ ] **Fundir a tabela e a figura numa tela só.** Hoje são duas telas: uma com números e nenhuma evidência, outra com evidência e nenhuma palavra.
- [ ] A tabela de 2 linhas vira uma **faixa horizontal de números** — ocupa um quinto do espaço e lê-se igual.
- [ ] Acrescentar a **frase de conclusão em corpo grande** abaixo da figura, e dizer nela que o eixo é logarítmico.

> **Por quê.** Um slide de figura sem texto do grupo obriga o público a ler o título interno do matplotlib, que é ilegível da quinta fileira. A figura prova; a frase é o que fica.

## Tela 4 — A definição do alvo decide o problema

`Evidência` · figura `reports/figuras/fig08-alvo-por-decada.png` · vem de: slides 5 + 6 + 13, fundidos · **1:50**

**O texto exato da tela**

- *Título* — A DEFINIÇÃO DO ALVO DECIDE O PROBLEMA
- *Legenda em duas linhas, com as cores do gráfico* — ■ Mediana **global** — um limiar único para 30 anos / ■ Mediana **do ano** — cada filme contra os que estrearam com ele
- *Figura* — reports/figuras/fig08-alvo-por-decada.png, largura total
- *Conclusão* — **86%** dos filmes dos anos 1990 contra **26%** dos anos 2020 — mesma definição. Correlação do ano com o alvo: **−0,364 → +0,002**.
- *Linha menor* — E as classes ficam em 50,0% / 49,7% por construção — **não há desbalanceamento a tratar**.

**O que muda**

- [ ] **Fundir três telas em uma:** o slide 5 (que hoje tem uma frase solta), o slide 6, e o slide 13 (que é repetição exata do 6 e deve sumir).
- [ ] Pôr as **duas definições acima da figura**, cada uma com o quadradinho da cor correspondente no gráfico. Assim o público lê o gráfico sozinho.
- [ ] Trazer o **balanceamento para cá**. Ele é consequência direta desta tela, e hoje aparece solto no slide 12, cinco telas depois da evidência que o justifica.

> **Por quê.** É a tela mais importante da apresentação. Concentrar aqui a montagem, a prova e as duas consequências transforma três telas fracas numa tela forte — e libera quase dois minutos.

# ATO 2 — A qualidade dos dados

**Ana Raquel · 5:30**

## Tela 5 — A bilheteria é uma lei de potência

`Evidência` · figura `reports/figuras/fig01-distribuicao-publico.png` · vem de: NOVA — figura já pronta, nunca usada · **1:05**  ·  **TELA NOVA**

**O texto exato da tela**

- *Título* — A BILHETERIA É UMA LEI DE POTÊNCIA
- *Faixa de números* — **2.806** público mediano &nbsp; **148.399** média (53× a mediana) &nbsp; **10,0** assimetria
- *Figura* — reports/figuras/fig01-distribuicao-publico.png, largura total
- *Conclusão* — **1% dos filmes concentra 36% de todo o público.** 10% concentram 91%; a metade inferior da base responde por 0,28%.

**O que muda**

- [ ] **Tela nova.** A figura já existe no repositório, pronta, e nunca foi usada.
- [ ] Ela entra imediatamente **antes** da decisão sobre outliers — que é a decisão que ela justifica.

> **Por quê.** Hoje o deck afirma “a cauda faz parte do fenômeno” sem nunca mostrar a cauda. É a maior evidência descritiva do trabalho e a que falta para a decisão mais contra-intuitiva. Maior retorno por esforço do deck inteiro: a figura já está pronta.

## Tela 6 — Duas decisões de não fazer

`Decisão` · vem de: slides 11 + 12, parcialmente fundidos · **1:05**

**O texto exato da tela**

- *Título* — DUAS DECISÕES DE **NÃO** FAZER
- *Coluna 1 — NÃO REMOVER OUTLIERS* — O critério de Tukey marca **17,4%** da base — um em cada seis filmes. / Não é base suja: o IQR pressupõe simetria, e a assimetria aqui é 10. / Extremos validados — ingresso mediano R$ 11,16, nenhum valor negativo. / **Num regime de lei de potência, a cauda é o fenômeno.**
- *Coluna 2 — NÃO BALANCEAR* — Classes em **50,0% / 49,7%** — por construção do alvo. / O equilíbrio é artefato do corte pela mediana, não propriedade do mundo. / Se a Entrega 2 mudar o limiar, a decisão se inverte. / **SMOTE numa base equilibrada seria cumprir tabela.**
- *Rodapé* — E uma terceira: **não aplicar PCA** — são só 11 numéricas úteis; a dimensão cresce na codificação categórica, não nelas.

**O que muda**

- [ ] **Reunir as três decisões de “não fazer” numa tela só**, sob um título que anuncia o que elas são. Hoje estão espalhadas por três telas (11, 12 e 15).
- [ ] Tirar daqui a cardinalidade e a redundância — elas são decisões de *fazer* e vão para a próxima tela.
- [ ] Acrescentar a ressalva de que a decisão de não balancear é **condicional ao alvo**.

> **Por quê.** “Justificar por que não aplicar exige mais evidência do que aplicar” é o argumento mais forte que vocês têm, e ele só aparece se as três decisões estiverem juntas, com o título dizendo isso.

## Tela 7 — Nem toda ausência é a mesma coisa

`Evidência` · figura `reports/figuras/fig07-ausentes.png` · vem de: slides 9 + 10, fundidos · **1:05**

**O texto exato da tela**

- *Título* — NEM TODA AUSÊNCIA É A MESMA COISA
- *Quatro caixas de altura igual* — **61,5%** ESTRUTURAL — não houve coprodução → categoria própria / **23,3%** DE JUNÇÃO — cobertura do IBGE → falha nossa / **2,13%** TALVEZ MNAR — max_salas → indicadora de ausência / **0,84%** SEM ALVO — 22 filmes com “ND” → excluir
- *Figura* — reports/figuras/fig07-ausentes.png, largura total
- *Conclusão* — Fora esses três campos, **tudo abaixo de 2%** — a base é notavelmente completa para dado administrativo.

**O que muda**

- [ ] Fundir as duas telas: os percentuais e o gráfico que os mostra devem estar juntos.
- [ ] **Incluir os 61,5% de uf2_bruto.** Hoje o texto abre em 59,9% e o gráfico da tela seguinte mostra 61,5% no topo — o público vê a contradição.
- [ ] Cada caixa ganha o **tratamento**, não só o diagnóstico. Uma caixa que diz “ausência não aleatória” e para aí não mostra decisão nenhuma.
- [ ] Igualar a altura das quatro caixas e subir o percentual para o maior corpo.

> **Por quê.** A tela hoje diagnostica e não decide. Acrescentar a seta “→ tratamento” em cada caixa é o que transforma um inventário numa análise.

## Tela 8 — Cardinalidade e redundância

`Decisão` · vem de: slide 12 (parte) · **0:55**

**O texto exato da tela**

- *Título* — CARDINALIDADE E REDUNDÂNCIA
- *Linha 1* — **1.738** direções · **467** distribuidoras (287 com um único filme) &nbsp;→&nbsp; **agrupar categorias raras** — frequência mínima 5–15 · −0,009 AUC · −380 colunas
- *Linha 2* — ano ↔ filmes_no_ano · **ρ = 0,86** &nbsp;→&nbsp; **escolher um dos dois** — manter os dois infla variância no modelo linear
- *Linha 3* — n_ufs · moda em **97,1%** &nbsp;→&nbsp; **remover** — medido: o AUC muda 0,000
- *Conclusão* — Todas as três por **medição**, não por intuição.

**O que muda**

- [ ] Reorganizar em **três linhas evidência → decisão**. Hoje são quatro fatos empilhados numa coluna, sem nenhuma decisão ao lado.
- [ ] Acrescentar **o peso medido** de cada decisão. Vocês mediram os três; nenhum aparece no slide.
- [ ] Tirar daqui o balanceamento, que foi para a tela 4.

> **Por quê.** Alinhar evidência e decisão na mesma linha é o que faz o público ver que nenhuma decisão foi arbitrária — e é isso que a disciplina está avaliando.

## Tela 9 — O que carrega informação

`Evidência` · figura `reports/figuras/fig10-correlacao-com-alvo.png` · vem de: slides 7 + 8, fundidos · **1:20**

**O texto exato da tela**

- *Título* — O QUE CARREGA INFORMAÇÃO
- *Aviso, em faixa destacada* — **Escalas diferentes:** V de Cramér ∈ [0, 1] para categóricas · ρ de Spearman ∈ [−1, 1] para numéricas. Spearman, e não Pearson, por causa da assimetria 10.
- *Figura* — reports/figuras/fig10-correlacao-com-alvo.png, largura total
- *Conclusão* — **ano = +0,002** — o calendário saiu, e por medida. **Gênero (V = 0,338) é o atributo mais associado da base** → codificar categóricas importa mais que transformar numéricas.

**O que muda**

- [ ] Fundir as duas telas. O slide 7 de hoje são três números flutuando com dois terços da tela vazios; a evidência deles está na tela seguinte.
- [ ] **Acrescentar o aviso das escalas.** Hoje o slide 7 põe V = 0,338 ao lado de ρ = 0,274 como se fosse um ranking só — e não é.
- [ ] Na conclusão, destacar o **+0,002 do ano**: é a prova numérica da tela 4.

> **Por quê.** Comparar V de Cramér com ρ de Spearman é o único erro conceitual que o deck pode cometer. Dito em faixa destacada, vira demonstração de cuidado em vez de armadilha.

# ATO 3 — Vazamento, decisões e conclusão

**Laura Virgínia · 4:05**

## Tela 10 — Vazamento de dados

`Decisão` · vem de: slide 14 · **1:35**

**O texto exato da tela**

- *Título* — VAZAMENTO DE DADOS
- *Subtítulo* — Estar na base ≠ estar disponível antes da estreia. O critério é **disponibilidade temporal**, não correlação alta.
- *Coluna ✓ — ANTES DA ESTREIA* — gênero · fomento (FSA / incentivo) · histórico da direção · histórico da distribuidora · UF · coprodução / **Fomento é aprovado antes de a obra existir — por isso é legítimo.**
- *Coluna ✕ — DEPOIS DA ESTREIA* — publico · renda (ρ = 0,99 com o alvo — é a resposta) · renda_deflacionada_2024 · max_salas (máximo durante a carreira)
- *Faixa inferior — o preço* — honesto **0,832** → + max_salas **0,940** → + renda **0,993**. &nbsp;**−0,16 de AUC.**

**O que muda**

- [ ] **Acrescentar o preço: −0,16 de AUC.** Hoje a tela diz quais atributos saem e não diz quanto custa tirá-los — e vocês mediram isso.
- [ ] Acrescentar **por que fomento é legítimo**. É o argumento mais inteligente do trabalho e hoje está invisível no slide.
- [ ] Acrescentar o **critério** no subtítulo: disponibilidade temporal, não correlação. É o que separa quem entendeu de quem decorou.
- [ ] Consertar a quebra de renda_deflacionada_2024 no meio da palavra e igualar a altura das duas caixas.

> **Por quê.** Um vazamento sem preço é opinião; com preço, é resultado. Esta é a segunda melhoria de maior retorno do deck, e o número já está em reports/sensibilidades_s1.csv.

## Tela 11 — De evidência a decisão

`Decisão` · vem de: slide 15 · **0:45**

**O texto exato da tela**

- *Título* — DE EVIDÊNCIA A DECISÃO
- *Tabela de três colunas* — Evidência | Decisão | **Peso medido** — sete linhas, terminando nas duas decisões de “não fazer”, com travessão na coluna de peso.

**O que muda**

- [ ] **Acrescentar a terceira coluna: “peso medido”.** Hoje a tabela tem duas colunas e nenhum número — e vocês mediram seis das sete linhas.
- [ ] **Recapturar a tabela sem os sublinhados vermelhos do corretor ortográfico**, que estão visíveis no print atual sob sucesso_no_ano, max_salas e “Cauda”. Melhor ainda: refazer como tabela nativa, não imagem.
- [ ] Ordenar por peso decrescente, deixando as duas de “não fazer” no fim.

> **Por quê.** A coluna de peso é o que distingue esta EDA de um checklist. Sem ela, a tabela diz “decidimos”; com ela, diz “medimos e então decidimos”.

## Tela 12 — Um resultado maior não significa um modelo melhor

`Decisão` · vem de: slide 16 (corrigido) · **1:30**

**O texto exato da tela**

- *Título* — UM RESULTADO MAIOR NÃO SIGNIFICA UM MODELO MELHOR
- *Subtítulo* — Mesmo algoritmo, mesmo protocolo. Mudam só três decisões.
- *Coluna esquerda* — **AUC 0,995** — o caminho fácil / alvo global — *lê o calendário* / renda e max_salas — *lê a resposta* / *k*-fold aleatório — *vê o futuro*
- *Coluna direita* — **AUC 0,725** — coerente com o uso real / sucesso_no_ano / só informação pré-estreia / treino ≤ 2017 · teste ≥ 2018
- *Faixa inferior* — A diferença, decomposta: alvo **−0,062** · atributos **−0,163** · partição **−0,087**. **Nenhuma linha de código distingue as duas.**

**O que muda**

- [ ] **0,696 → 0,725.** Correção obrigatória: 0,696 não existe em nenhum arquivo do repositório; 0,725 é o que o notebook executado registra para exatamente esta combinação.
- [ ] Acrescentar “**mesmo algoritmo, mesmo protocolo**” no subtítulo. Sem isso, metade da sala conclui que vocês pioraram o modelo de propósito.
- [ ] Acrescentar, ao lado de cada marcador, **o que ele faz o modelo ler**: o calendário, a resposta, o futuro. Hoje os marcadores são rótulos, não explicações.
- [ ] Acrescentar a **decomposição da diferença** na faixa inferior — ela mostra que o 0,27 não é opinião.

> **Por quê.** É a tela que mais depende da fala hoje. Com a decomposição e o aviso do protocolo em tela, ela passa a se sustentar sozinha — que é o critério de um bom slide de conclusão.

## Tela 13 — É possível prever? Parcialmente, sim.

`Fecho` · vem de: slide 17 (reescrito) · **0:15**

**O texto exato da tela**

- *Título* — É POSSÍVEL PREVER? PARCIALMENTE, SIM.
- *Número grande* — AUC 0,725
- *Abaixo* — Bem acima do acaso (0,5). Longe da certeza. **É modesto porque é verdadeiro.**
- *Rodapé* — Base, notebook executado e relatório completo · github.com/anaraque-l/bilheteria-cinema-brasileiro · ANCINE · FSA · Leis de incentivo · IPCA/BCB · IBGE

**O que muda**

- [ ] **Substituir o “OBRIGADA!” isolado.** Um slide vazio fica na tela durante toda a rodada de perguntas — é o pior uso possível do momento de maior atenção da banca.
- [ ] **Responder a pergunta da tela 2.** O deck abre perguntando e hoje fecha sem responder.
- [ ] Deixar em tela o que vocês querem consultar durante as perguntas: o número, o repositório e as fontes.

> **Por quê.** O slide de fechamento é o que a banca olha enquanto formula as perguntas. Deve conter a resposta, não uma saudação.

---

# De onde veio cada tela

Nada foi jogado fora. Onze das dezessete telas atuais continuam existindo; o que muda é
que cada figura passou a morar na mesma tela que o texto que ela prova.

| Hoje | Vira | O que acontece |
|---|---|---|
| 1 | 1 | ganha a linha de tese e alinhamento à esquerda |
| 2 | 2 | perde a linha duplicada; ganha a definição de sucesso e a base |
| 3 + 4 | 3 | tabela e figura na mesma tela |
| 5 + 6 + 13 | 4 | montagem, prova e consequência numa tela só; a repetição do 13 sai |
| — | 5 | **tela nova**: `fig01`, que já existe no repositório e nunca foi usada |
| 11 + parte do 12 | 6 | as decisões de "não fazer" reunidas sob um título que as anuncia |
| 9 + 10 | 7 | percentuais e gráfico juntos; cada ausência ganha o seu tratamento |
| resto do 12 | 8 | vira três linhas evidência → decisão, com o peso medido |
| 7 + 8 | 9 | fundidos, com o aviso das escalas em faixa destacada |
| 14 | 10 | ganha o preço (−0,16 de AUC) e o porquê de o fomento ser legítimo |
| 15 | 11 | ganha a coluna "peso medido"; sai o print com corretor ortográfico |
| 16 | 12 | **0,696 → 0,725**; ganha o aviso do protocolo e a decomposição |
| 17 | 13 | deixa de ser "OBRIGADA!" e passa a responder a pergunta da tela 2 |

---

# Ordem de execução

Se o tempo até a apresentação for curto, façam nesta ordem. As duas primeiras são as
únicas que, sozinhas, mudam a nota.

| # | O que fazer | Onde | Custo |
|---|---|---|---|
| 1 | **Trocar 0,696 por 0,725** | tela 12 | 1 min |
| 2 | **Apagar a linha "Restrição" duplicada** | tela 2 | 1 min |
| 3 | Apagar a tela repetida | slide 13 de hoje | 1 min |
| 4 | Escrever a definição de sucesso e o tamanho da base | tela 2 | 10 min |
| 5 | Acrescentar "−0,16 de AUC" e o porquê do fomento | tela 10 | 10 min |
| 6 | Responder a pergunta no fechamento | tela 13 | 10 min |
| 7 | Recapturar a tabela sem o corretor e acrescentar a coluna de peso | tela 11 | 20 min |
| 8 | Acrescentar a frase de conclusão em cada tela de figura | telas 3, 5, 7, 9 | 30 min |
| 9 | Inserir `fig01` como tela nova | tela 5 | 15 min |
| 10 | Fundir as telas de texto com as de figura | 3, 4, 7, 9 | 1 h |
| 11 | Alinhar tudo à esquerda e pôr o rodapé com numeração | todas | 30 min |
