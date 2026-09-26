# Relatório — Entrega 1: Análise Exploratória de Dados

## Prever bilheteria de filme brasileiro antes da estreia (1995–2024)

**CIN0144 — Aprendizado de Máquina e Ciência de Dados**
Centro de Informática · UFPE

> Esta é a versão técnica do relatório, que vive junto do código e cita os nomes reais
> das colunas. A versão de entrega é o arquivo `Relatorio_Entrega_1_Grupo_11.docx`,
> nesta mesma pasta, com o mesmo conteúdo escrito em linguagem corrida.

---

## Sumário executivo

Analisamos **2.626 filmes brasileiros** lançados comercialmente em salas de exibição
entre 1995 e 2024, a partir da listagem oficial da ANCINE, para responder: *um filme
vai alcançar público acima da mediana do seu ano de lançamento, prevendo apenas com
atributos conhecidos antes da estreia?*

A resposta preliminar é **sim, parcialmente** — mas o resultado que mais importa é
outro. Esta base contém **três atalhos** que produzem desempenho excelente e conclusão
sem valor. Medimos cada um:

| atalho | ganho ilusório de AUC |
|---|---|
| usar a renda de bilheteria como atributo | **+0,161** |
| usar o máximo de salas como atributo | **+0,108** |
| validar com *k-fold* aleatório em vez de partição temporal | **+0,087** |

Somados a uma definição de alvo que embute o ano de lançamento, o caminho fácil entrega
**AUC 0,995** e o caminho honesto entrega **0,725**. **0,27 de AUC** separa as duas
versões, e nenhuma linha de código as distingue à primeira vista.

E há um quarto atalho, que não é de atributo nem de validação, e sim **da própria
definição de sucesso**. Auditamos nosso alvo (§2.9 e `docs/04-auditoria-do-alvo.md`) e o
resultado contraria o ponto de partida: o público brasileiro não é uma distribuição a ser
partida ao meio, e sim **duas populações** — circuito limitado (64% dos filmes, centro em
915 espectadores) e lançamento comercial (36%, centro em 51.402) —, com fronteira no
**percentil 69**. A mediana cai *dentro* da primeira. O corte pela mediana, portanto,
separa circuito limitado bom de circuito limitado ruim.

Este relatório documenta a base, a análise exploratória, os **quinze problemas**
identificados e as **catorze hipóteses** de pré-processamento — cada uma acompanhada da
medida do que custa e do que vale.

---

## 1. Descrição da base

### 1.1 Fonte, coleta e licença

| fonte | órgão | papel | licença |
|---|---|---|---|
| Listagem dos Filmes Brasileiros Lançados 1995–2024 | ANCINE / OCA | primária | dado aberto federal |
| Obras com Investimento do FSA | ANCINE | fomento direto, por CPB | **CC-BY** |
| Obras com Fomento Indireto Aprovado | ANCINE | leis de incentivo, por CPB | **CC-BY** |
| IPCA, série 433 do SGS | Banco Central | deflacionar a renda | dado aberto federal |
| População residente estimada, agregado 6579 | IBGE | contexto de mercado | dado aberto federal |

Todas são dados abertos federais regidos pela **Lei 12.527/2011** (LAI) e pelo
**Decreto 8.777/2016**: uso livre, com citação da fonte, sem restrição a uso acadêmico.
Os dois conjuntos de fomento declaram licença nominal no catálogo —
**Creative Commons Attribution**. Nenhuma exige cadastro, chave de API ou aceite de
termos — restrição que o grupo impôs para que qualquer integrante e o professor
reproduzam a ingestão numa máquina limpa.

**A coleta exigiu descobrir coisas que não estão documentadas.** O portal do gov.br roda
Plone e a URL "bonita" devolve a *página* do arquivo, não o arquivo — o CSV só vem com o
sufixo `/@@download/file`, e sem ele o pandas lê HTML. A edição 1995–2025 não existe: as
URLs de 2025 devolvem 404. E os dois arquivos de fomento **não estão no portal do OCA**:
o catálogo `dados.gov.br` é uma aplicação de página única cuja API devolve 401 para
cliente externo; renderizada num navegador, a mesma API responde 200 e revela o host
real, **`dados.ancine.gov.br`**, que não é linkado de lugar nenhum.

**Coleta.** `src/ingestao.py` baixa os três arquivos usando apenas a biblioteca padrão
do Python e grava em `data/raw/` **sem transformar nada**. O bruto é versionado no
repositório: órgão público republica arquivo sem avisar — a própria edição `2024r` é uma
retificação da `2024` — e versionar é o que garante que outra pessoa reproduza *os
mesmos números*. `src/build_dataset.py` faz a tipagem e as junções.

### 1.2 Duas ressalvas de honestidade

**A listagem 1995–2025 não existe.** Em 10/09/2026, a edição publicada mais recente é a
`1995 a 2024r`; as URLs de 2025 devolvem HTTP 404. Trabalhamos com **1995–2024**.

**O atributo `duração` não está disponível.** A ANCINE não o publica. A fonte aberta
que o traria (Wikidata, licença CC0) não é alcançável neste ambiente. O trabalho segue
sem ele, e isso está registrado em vez de silenciado.

### 1.3 Dimensões e tipos

**2.626 instâncias × 35 atributos** — acima do mínimo de 1.000 instâncias e 10
atributos. Treze vêm direto da listagem da ANCINE, cinco das junções com fomento, IPCA e
IBGE, e os demais foram derivados.

Os seis tipos que o enunciado nomeia estão todos presentes e distinguidos:

| tipo | atributos |
|---|---|
| identificadores | `cpb`, `titulo` |
| temporais | `ano`, `decada` |
| numéricas contínuas | `publico`, `renda_corrente`, `renda_deflacionada_2024`, `deflator`, `populacao_br`, `mediana_publico_do_ano` |
| numéricas discretas | `max_salas`, `n_ufs`, `filmes_no_ano`, `filmes_diretor_antes`, `filmes_distribuidora_antes`, `filmes_produtora_antes` |
| categóricas nominais | `genero`, `direcao`, `produtora_maj`, `produtora_min`, `distribuidora`, `uf_bruto`, `uf2_bruto`, `uf_maj` |
| **categóricas ordinais** | `experiencia_da_direcao`, `porte_da_distribuidora` |
| categóricas binárias | `coproducao`, `estreia_do_diretor`, `recebeu_fsa`, `recebeu_incentivo` |
| **alvos** | `sucesso_global`, `sucesso_no_ano` |

As duas **ordinais** foram construídas de propósito, porque as faixas têm ordem natural
e essa ordem é informação: uma direção *veterana* fez mais filmes que uma *iniciante*.
Ambas derivam de contagens que olham só para anos anteriores, então herdam a propriedade
de serem anteriores à estreia.

O dicionário completo está em `docs/dicionario-de-dados.csv`, gerado pelo notebook.

### 1.4 Justificativa do problema

Entre 1995 e 2024 o Estado brasileiro investiu bilhões em fomento ao audiovisual — Lei
do Audiovisual, Lei Rouanet, Fundo Setorial do Audiovisual. A decisão de investir é
tomada **antes** de o filme existir. Saber quais características de lançamento se
associam ao alcance de público informa produtoras (estratégia de lançamento e escolha
de distribuidora), distribuidoras (dimensionamento da janela de salas) e formuladores
de política pública (o fomento está chegando a filmes que encontram plateia?).

A junção com os dados de fomento torna essa última pergunta respondível de forma
direta, e ela passa a ser a justificativa mais forte do trabalho:

> **O dinheiro público está indo para filmes que encontram plateia?**

Há também interesse analítico: como a seção 2 mostra, a bilheteria brasileira é uma
distribuição de cauda extremamente longa. Prever nesse regime é genuinamente difícil.

### 1.5 Tipo de tarefa e variável-alvo

**Classificação binária.** O alvo nasce de `publico`, transformado em `sucesso = 1` se o
público supera a mediana.

Regressão sobre o público em nível foi descartada: com assimetria 10,0 e máximo 4.342
vezes a mediana, o erro médio diria mais sobre meia dúzia de blockbusters do que sobre
os 2.600 filmes restantes.

Mas **"a mediana" é ambíguo**, e a ambiguidade se revelou o achado central. Construímos
os dois alvos candidatos:

| alvo | definição | positivos |
|---|---|---|
| `sucesso_global` | público > mediana de toda a base (2.806) | 1.302 / 1.302 (50,0%) |
| `sucesso_no_ano` | público > mediana do próprio ano | 1.294 / 1.310 (49,7%) |

Vinte e dois filmes têm `publico` ausente e portanto **não têm alvo**.

> **Ressalva metodológica, e ela é grande.** Nenhuma das duas definições foi escolhida
> porque representa bem o conceito de sucesso comercial: as duas cortam na mediana porque
> a mediana é conveniente. A §2.9 mostra o que os dados dizem sobre onde o corte deveria
> estar, e `docs/04-auditoria-do-alvo.md` audita a questão inteira — incluindo a resposta
> à pergunta que qualquer banca faria: *por que acima da mediana significa sucesso?*

---

## 2. Resultados da análise exploratória

### 2.1 A distribuição do público é uma lei de potência

| estatística | valor |
|---|---|
| mediana | **2.806** espectadores |
| média | **148.399** — 53× a mediana |
| 1º quartil | 542 |
| 3º quartil | 22.747 |
| percentil 99 | 2.995.628 |
| máximo | 12.184.373 (*Nada a Perder*, 2018) |
| assimetria | **10,04** |
| curtose | **135,25** |

Quando média e mediana divergem nessa ordem de grandeza, a média deixou de descrever
qualquer filme real. A distribuição se espalha por **sete ordens de grandeza**, de 2
espectadores a 12,2 milhões, e é aproximadamente log-normal (fig. 1, painel central).

A concentração é extrema:

- **1% dos filmes concentra 36,2% de todo o público**
- **10% concentram 90,7%**
- **a metade inferior da base responde por 0,28%**

> **Implicação.** Média e desvio-padrão são inúteis como resumo. `StandardScaler` sobre
> o valor bruto comprimiria 99% dos dados num ponto. E o corte pela mediana, ao produzir
> classes equilibradas, **esconde** essa assimetria do alvo — bom para o treino,
> perigoso para a interpretação.

📊 `reports/figuras/fig01-distribuicao-publico.png`

### 2.2 O mercado mudou de natureza

| ano | lançamentos | público mediano |
|---|---|---|
| 1995 | 14 | 14.230 |
| 2024 | 197 | **933** |

O número de lançamentos cresceu **14×**; o público mediano por filme **caiu 15×**.

Não é que o cinema brasileiro tenha encolhido — o público *total* não caiu na mesma
proporção. É que o conjunto de filmes que chegam à sala mudou: entrou uma quantidade
enorme de documentários e produções de circuito limitado que antes não eram lançados
comercialmente. **A queda da mediana é um efeito de composição.**

A pandemia (2020–2021) aparece como choque real na série, não como ruído.

> **Implicação — a mais séria do trabalho.** Se o público mediano de 1995 é uma ordem de
> grandeza maior que o de 2024, um corte pela mediana **global** classifica quase todo
> filme antigo como sucesso e quase todo filme recente como fracasso.

📊 `reports/figuras/fig02-evolucao-anual.png` · `fig06-salas-e-decada.png`

### 2.3 Categóricas: cardinalidade e concentração, os dois extremos

| atributo | distintos | observação |
|---|---|---|
| `genero` | **4** | *Videomusical* tem **1 filme** |
| `uf_maj` | 24 | RJ + SP concentram **75,4%** da produção |
| `distribuidora` | **467** | **287 aparecem em um único filme** |
| `direcao` | 1.738 | quase um identificador |
| `produtora_maj` | 1.502 | idem |

`genero` sofre do problema oposto ao de `distribuidora`. Com 4 categorias, é candidato
natural a *one-hot* — mas a categoria de um registro só estará ausente do treino em pelo
menos 4 dos 5 folds. `distribuidora`, com 467 categorias numa base de 2.626 linhas,
geraria mais dimensão do que informação; e as 287 categorias de filme único seriam
indicadores individuais, ou seja, memorização disfarçada de atributo.

Há ainda **entidade fragmentada**: `Downtown` (65 filmes), `Paris` (59) e
`Downtown/Paris` (92) são três categorias para as mesmas empresas em arranjos diferentes.

📊 `reports/figuras/fig03-categoricas.png`

### 2.4 Fomento público: o gradiente, e a inversão

A ANCINE publica quais obras tiveram investimento do **FSA** e quais tiveram projeto
aprovado nas **leis de incentivo**. As junções são por CPB e cobrem **67,1%** dos filmes
com CPB válido. O que torna esses atributos utilizáveis é que **fomento é aprovado antes
de a obra existir** — não há como carregar o desempenho.

| origem do fomento | filmes | taxa de sucesso | público mediano |
|---|---|---|---|
| sem fomento | 843 | 0,326 | 1.495 |
| **só FSA** | 339 | 0,401 | **535** |
| só incentivo | 932 | 0,547 | 7.472 |
| **FSA e incentivo** | 476 | **0,773** | 7.562 |

O gradiente é forte: a combinação dos dois mecanismos mais que dobra a taxa de sucesso
em relação a não ter nenhum.

**A inversão está no grupo *só FSA*:** taxa de 40,1%, mas público mediano de apenas
**535 espectadores** — abaixo dos 1.495 do grupo *sem fomento*. Um mecanismo que
seleciona filmes acima da mediana do seu ano, mas cuja mediana absoluta é baixa, é um
mecanismo que financia muito documentário e produção de circuito limitado. Não é crítica
ao FSA: é descrição do que ele financia.

> ⚠️ **Confundimento temporal.** O FSA foi criado em **2006**: a cobertura é 0,0% nos
> anos 1990 e 63,3% nos anos 2020, e `recebeu_fsa` tem **ρ = 0,511 com `ano`**. Isso não
> o invalida — dentro dos anos 2010 isoladamente o gradiente se mantém (80,4% contra
> 28,7%) — mas obriga a manter `ano` no modelo. É a hipótese **H14**.

📊 `reports/figuras/fig09-fomento.png`

### 2.5 Gênero informa, mas não determina

A mediana de público da Animação e da Ficção está uma a duas ordens de grandeza acima da
do Documentário, e cerca de dois terços das ficções ficam acima da mediana do ano, contra
menos de um terço dos documentários.

As caixas, porém, **se sobrepõem amplamente**: existem documentários com centenas de
milhares de espectadores e ficções com dezenas.

📊 `reports/figuras/fig04-publico-por-genero.png`

### 2.6 Relação de cada atributo com a variável-alvo

O heatmap da seção seguinte mede atributo contra atributo. Esta mede cada atributo
contra o **alvo**, que é binário — e por isso exige duas medidas: **ρ de Spearman** para
as numéricas, **V de Cramér** para as categóricas.

| numérica | ρ com `sucesso_no_ano` | | categórica | V de Cramér |
|---|---|---|---|---|
| `projetos_incentivo` | **+0,274** | | `genero` | **0,338** |
| `filmes_diretor_antes` | +0,193 | | `origem_do_fomento` | 0,320 |
| `filmes_distribuidora_antes` | +0,183 | | `porte_da_distribuidora` | 0,205 |
| `recebeu_fsa` | +0,164 | | `experiencia_da_direcao` | 0,192 |
| `coproducao` | +0,136 | | `uf_maj` | 0,178 |
| `filmes_no_ano` | **+0,003** | | `coproducao` | 0,135 |
| **`ano`** | **+0,002** | | | |

**Este quadro fecha o argumento central do relatório.** `ano` tem correlação de
**+0,002** com o alvo, e `filmes_no_ano` de +0,003 — praticamente zero.

Com `sucesso_global`, o ano seria um dos atributos mais preditivos da base, porque a
mediana global embute o calendário (seção 3.3). Ao definir o alvo **relativo à mediana
do próprio ano**, a informação temporal foi **completamente neutralizada**. Não é um
argumento: é um número.

**O que sobra quando o atalho sai** são correlações modestas — nenhuma numérica chega a
0,3. Isso é esperado: se um atributo isolado explicasse o sucesso de um filme, não
haveria indústria de cinema.

**E as categóricas mudam o ranking.** Pelo V de Cramér, **`genero` é o atributo mais
associado ao alvo em toda a base** (0,338), acima de qualquer numérica. Isso não
apareceria num heatmap de Spearman, que não opera sobre categórica nominal.

> **Implicação.** A codificação das categóricas importa mais que a transformação das
> numéricas nesta base — é onde está o sinal. Reforça **H4** e explica **H13**: o
> gargalo de dimensionalidade é categórico, não numérico.

📊 `reports/figuras/fig10-correlacao-com-alvo.png`

### 2.7 Os atributos ordinais e a dimensão regional

| experiência da direção | taxa | | porte da distribuidora | taxa | | UF | taxa |
|---|---|---|---|---|---|---|---|
| estreante (n=1.768) | 0,43 | | nova (n=1.033) | 0,38 | | RJ (n=1.057) | 0,55 |
| iniciante (n=581) | 0,61 | | pequena (n=592) | 0,56 | | **PE (n=92)** | **0,53** |
| estabelecida (n=204) | **0,69** | | média (n=626) | **0,62** | | SP (n=906) | 0,51 |
| veterana (n=51) | 0,69 | | grande (n=353) | 0,53 | | RS (n=127) | 0,36 |

**A experiência da direção sobe e satura.** De 0,43 a 0,69, com a faixa veterana empatada
com a estabelecida. Os primeiros filmes de carreira são os que mais mudam a chance; o
retorno marginal depois desaparece. É comportamento de variável de reputação, e justifica
ter binado a contagem em faixas em vez de usá-la crua.

**O porte da distribuidora NÃO é monótono, e isso é achado.** Sobe até a faixa média e
**cai na grande**. O atributo mede **volume de catálogo, não poder comercial** — a
distribuidora com mais filmes na base é a Vitrine Filmes, com 189, e boa parte do que ela
distribui é circuito de arte. Uma ordinal cuja ordem não produz gradiente monótono
continua informativa, mas avisa que "grande" não significa o que o senso comum sugere.

**A dimensão regional** varia 19 pontos entre as UFs com pelo menos 30 filmes, e
**Pernambuco aparece em segundo**, à frente de São Paulo — com 92 filmes, não é ruído de
amostra pequena, e é consistente com o que se sabe do setor sobre a produção pernambucana.

> ⚠️ **Associação, não causalidade.** `uf_maj` é o endereço fiscal da produtora
> majoritária, não onde o filme foi rodado nem onde foi visto — e está confundida com
> gênero e com acesso a fomento.

📊 `reports/figuras/fig11-ordinais-e-regiao.png`

### 2.8 Relações entre variáveis

Usamos **Spearman**, não Pearson: com assimetria acima de 10, Pearson mediria o efeito
dos poucos blockbusters, não a relação monotônica de interesse.

| par | ρ | natureza |
|---|---|---|
| `renda_deflacionada_2024` × `publico` | **0,994** | vazamento direto |
| `renda_corrente` × `publico` | 0,985 | vazamento direto |
| `max_salas` × `publico` | **0,788** | vazamento provável |
| `ano` × `filmes_no_ano` | 0,862 | redundância |
| `filmes_diretor_antes` × `estreia_do_diretor` | 0,978 | redundância que **nós** criamos |

Fora esses blocos, as correlações com o público são modestas: histórico da direção
(0,29), da produtora (0,22), da distribuidora (0,12), coprodução (0,06). **Nenhum
atributo honesto sozinho explica o sucesso** — o que é esperado e é o que dá sentido a
usar um modelo.

📊 `reports/figuras/fig05-correlacao.png`

---

### 2.9 O corte que os dados propõem — duas populações, não uma

A §2.1 mostrou que o público é quase log-normal. Quase: em log₁₀ uma mistura de **duas**
gaussianas ajusta melhor que uma só (BIC **8.260** contra **8.358**), e as duas componentes
têm leitura direta no domínio:

| componente | peso | centro | leitura |
|---|---|---|---|
| circuito limitado | 64% | **915** espectadores | mostra, festival, janela curta — 90% dos documentários caem aqui |
| lançamento comercial | 36% | **51.402** espectadores | filme que disputa a bilheteria de fato |

A fronteira entre elas — o público em que uma componente passa a dominar a outra — fica em
**11.830 espectadores**, o **percentil 69** da base. Três consequências:

1. **A mediana (2.806) cai dentro da população de circuito limitado.** O alvo atual não
   separa sucesso comercial de fracasso comercial: separa circuito limitado bom de circuito
   limitado ruim.
2. **O quartil superior (P75) é o quantil redondo que cai em cima da fronteira empírica.**
   É o único corte deste relatório que não escolhemos — foi a distribuição que o indicou.
3. **O patamar comercial é estável e a mediana não é.** O centro da componente comercial fica
   entre 108 mil e 130 mil espectadores nos anos 1990, 2000 e 2010 — e só colapsa nos 2020
   (9.687). A mediana, no mesmo período, cai de 24.704 para 573. **O que desabou não foi o
   cinema comercial brasileiro; foi a composição da lista de lançamentos.**

> **Implicação.** O corte pela mediana é conveniente, não descoberto. E o equilíbrio 50/50
> que ele produz não é evidência de nada: cortar na mediana devolve 50/50 em *qualquer*
> distribuição — inclusive numa em que 1% dos filmes leva 36,2% do público, como é o caso.

📊 `reports/figuras/fig12-duas-populacoes.png`

---

## 3. Problemas identificados

| # | problema | evidência | gravidade |
|---|---|---|---|
| **P1** | alvo global embute o ano | 85,6% (1990s) × 26,3% (2020s) | **crítica** |
| **P2** | vazamento por `renda` | ρ = 0,994; AUC vai a 0,994 | **crítica** |
| **P3** | vazamento provável por `max_salas` | +0,108 de AUC | alta |
| **P4** | assimetria extrema do público | skew 10,0; máx/mediana 4.342× | alta |
| P5 | cardinalidade da distribuidora | 467 categorias, 287 com um só filme | média |
| P6 | ausência MNAR em `max_salas` | público mediano difere entre os grupos | média |
| P7 | `uf_bruto` malformada | 87 valores distintos para 27 UFs | média |
| P8 | redundância `ano` × `filmes_no_ano` | ρ = 0,862 | média |
| P9 | `n_ufs` quase constante | moda em 97,1% | baixa |
| P10 | categoria de 1 registro em `genero` | *Videomusical*, n = 1 | baixa |
| P11 | entidade fragmentada | Downtown / Paris / Downtown-Paris | baixa |
| P12 | 22 filmes sem alvo | `publico` = `ND` | baixa |
| P13 | `recebeu_fsa` confundido com o ano | FSA criado em 2006; ρ = 0,511 | média |
| **P14** | **20% dos rótulos são ruído amostral** | público dentro do IC95% da mediana do ano | **alta** |
| **P15** | **vazamento de coorte no alvo anual** | a mediana do ano só fecha em 31/12 | **alta** |

### 3.1 Valores ausentes — quatro naturezas distintas

| atributo | ausência | natureza |
|---|---|---|
| `uf2_bruto` | 61,5% | **estrutural** — não houve coprodutora |
| `produtora_min` | 59,9% | **estrutural** — idem |
| `populacao_br` | 23,3% | **de junção** — o IBGE não publica 1995–2000 |
| `max_salas` | 2,13% | `ND` no arquivo, e **MNAR** |
| `renda_corrente` | 0,95% | `ND` no arquivo |
| `publico` | 0,84% | `ND` — **sem alvo** |

Tratar os quatro casos com a mesma imputação seria um erro. `produtora_min` **não é dado
faltante**: o filme não teve coprodutora, e imputar inventaria coprodução onde não houve
— por isso criamos `coproducao` como binária, já que a informação está na própria
ausência. `populacao_br` exigiria interpolação temporal, não média. E a ausência de
`max_salas` **não é aleatória**: os filmes sem o campo têm público mediano muito menor,
ou seja, a própria ausência informa que a carreira foi mínima.

📊 `reports/figuras/fig07-ausentes.png`

### 3.2 Outliers — e por que não vamos removê-los

O critério IQR marca **17,4%** dos filmes como *outlier* de público. Isso não indica
erro nos dados: indica que **o IQR é o critério errado para esta distribuição**. Num
regime de lei de potência, a cauda não é anomalia — é o fenômeno. Removê-la eliminaria
justamente os casos que o modelo precisa aprender a reconhecer.

**A verificação de domínio confirma que os dados são consistentes:**

- preço médio implícito do ingresso (renda ÷ público): mediana **R$ 11,16**, faixa de
  R$ 1,39 a R$ 31,43 — plausível em todos os registros;
- **nenhum** valor negativo, **nenhum** preço implícito abaixo de R$ 1,00;
- os 13 filmes com menos de 10 espectadores são extremos, mas coerentes com lançamento
  de sala única em circuito restrito.

**Inconsistências pontuais:** 1 filme com renda registrada e público ausente; 37 filmes
com público registrado e `max_salas` ausente.

**Duplicatas: nenhuma.** Zero linhas idênticas, zero CPB repetido. Os 6 títulos repetidos
ocorrem em anos diferentes — refilmagens e homônimos, registros legítimos.

### 3.3 Desbalanceamento — não está onde se esperava

Globalmente, os dois alvos são equilibrados: 50,0% e 49,7%. Desagregado por década, o
quadro se inverte:

| década | `sucesso_global` | `sucesso_no_ano` |
|---|---|---|
| 1990 | **0,856** | 0,490 |
| 2000 | 0,757 | 0,495 |
| 2010 | 0,502 | 0,498 |
| 2020 | **0,263** | 0,497 |

Com `sucesso_global`, a diferença entre a primeira e a última década é de quase **60
pontos percentuais**. O alvo não está medindo sucesso: está medindo **antiguidade**. Um
modelo com acesso a `ano` encontra esse atalho, atinge AUC alto e não aprende nada sobre
cinema.

> **O desbalanceamento desta base não está na proporção global de classes — está na
> distribuição condicional do alvo ao longo do tempo.** É por isso que SMOTE não
> resolveria nada: o problema não é falta de exemplos de uma classe, é uma definição de
> alvo que embute a variável errada.

📊 `reports/figuras/fig08-alvo-por-decada.png`

### 3.4 P14 — um quinto dos rótulos é indeterminado

Reamostramos cada ano com reposição (2.000 réplicas) e calculamos o IC95% da mediana
daquele ano. Um filme cujo público cai **dentro** desse intervalo tem classe indeterminada:
outra amostra do mesmo mercado o colocaria do outro lado do corte.

| ano | filmes | mediana | IC95% da mediana | indeterminados |
|---|---|---|---|---|
| 1995 | 14 | 14.230 | **5.308 – 155.000** | 50,0% |
| 2003 | 30 | 106.579 | 57.066 – 440.066 | 33,3% |
| 2013 | 127 | 2.376 | 1.646 – 3.708 | 18,1% |
| 2024 | 197 | 933 | 739 – 1.314 | 13,7% |

**Na base inteira, 521 filmes (20,0%) têm classe indeterminada.** Isso é um teto para
qualquer acurácia que a Entrega 2 venha a reportar, e precisa ser dito antes do número, não
depois. Nos anos 1990 a instabilidade é tão grande que o corte daquele ano é praticamente um
sorteio — o IC95% de 1995 tem largura de 10,5 vezes a própria mediana.

📊 `reports/alvo_estabilidade_mediana.csv`

### 3.5 P15 — o alvo anual olha para o futuro

`sucesso_no_ano` compara o filme com a mediana do ano *t*, que só é conhecida **em 31 de
dezembro de t**. Para prever um filme que estreia em março, o rótulo depende de filmes que
ainda não estrearam. O mesmo vale para o atributo `filmes_no_ano`: o total de lançamentos do
ano é uma contagem fechada no fim do ano, não observável no momento da previsão.

Há ainda uma coluna que é o **próprio limiar do alvo**: `mediana_publico_do_ano`. Ela está na
base por transparência de auditoria e, se entrar como atributo, entrega metade da resposta.

> **Lista de colunas proibidas na modelagem** — declarada em código, em
> `build_dataset.COLUNAS_PROIBIDAS`: `publico`, `renda_corrente`,
> `renda_deflacionada_2024`, `max_salas`, `mediana_publico_do_ano`, `filmes_no_ano`,
> `sucesso_global`, `sucesso_no_ano`.

Custo de corrigir P15, medido: usar o percentil do **ano anterior** — conhecido, publicado e
não contaminado pelo próprio filme — troca a classe de apenas **9,2%** dos filmes (κ = 0,82)
e custa 0,03 de AUC (0,774 → 0,743).

---

## 4. Hipóteses de pré-processamento

Cada hipótese decorre de uma evidência e, quando possível, foi **medida**. O protocolo é
fixo: floresta aleatória, 5-fold estratificado, semente 42, todo o pré-processamento
dentro dos folds via `Pipeline`.

> O modelo aqui é **instrumento de medida**, como um termômetro. Nenhum número desta
> seção é "o desempenho do nosso modelo" — a modelagem é a Entrega 2. A base entregue em
> `data/processed/filmes.csv` permanece **sem imputação, sem remoção de *outlier* e sem
> codificação**, como o enunciado exige de uma entrega exploratória.

| # | hipótese | decorre de | impacto medido |
|---|---|---|---|
| **H1** | adotar `sucesso_no_ano` como alvo principal | P1 | **−0,062** de AUC, elimina o atalho temporal |
| **H2** | excluir `renda*` e `max_salas` dos atributos | P2, P3 | **−0,163** de AUC, resultado honesto |
| **H3** | `log1p` só nos modelos que precisam | P4 | **+0,024** no linear, **0,000** na árvore |
| **H4** | agrupar distribuidora com `min_frequency` 5–15 | P5 | −0,009 de AUC, −380 colunas |
| **H5** | indicadora de ausência em vez de imputar `max_salas` | P6 | preserva o sinal MNAR |
| **H6** | usar `uf_maj`; descartar `uf_bruto` | P7 | 87 → 24 categorias |
| **H7** | escolher um de `ano` / `filmes_no_ano` | P8 | reduz variância no modelo linear |
| **H8** | remover `n_ufs` | P9 | **0,000** — indistinguível de zero |
| **H9** | validação **temporal**, não aleatória | — | **−0,087** de AUC, corresponde ao uso real |
| **H10** | **não** aplicar balanceamento | §3.3 | classes já em 50/49,7 |
| **H11** | **não** remover a cauda como *outlier* | §3.2 | a cauda é o fenômeno |
| **H12** | descartar (não imputar) os 22 sem alvo | P12 | rótulo não se inventa |
| **H13** | **não** aplicar PCA / redução de dimensionalidade | P8 | 11 numéricas úteis; o gargalo é categórico |
| **H14** | usar `recebeu_fsa` só com `ano` no modelo | P13 | ρ = 0,511 com o ano; efeito sobrevive dentro da década |

### Cobertura das técnicas citadas no enunciado

O enunciado (§5) nomeia sete técnicas de pré-processamento. Abaixo, onde cada uma é
tratada — inclusive as duas que decidimos **não** aplicar, com a evidência que sustenta
a decisão.

| técnica citada no enunciado | posição do grupo | hipótese | evidência |
|---|---|---|---|
| imputação | seletiva, conforme a natureza da ausência | H5, H12 | §3.1 |
| tratamento de *outliers* | **não aplicar** | H11 | §3.2 |
| codificação de categóricas | *one-hot* com agrupamento de raras | H4 | §2.3, S4 |
| normalização | só nos modelos que precisam dela | H3 | §2.1, S5 |
| balanceamento | **não aplicar** | H10 | §3.3 |
| seleção de atributos | remover vazamento, redundância e ruído | H2, H6, H7, H8 | §2.5, §3.4, S1, S6 |
| redução de dimensionalidade | **não aplicar PCA** | H13 | §3.4 |

**Sobre PCA.** Descartado por três razões, e não por esquecimento. O conjunto honesto
tem **7 atributos numéricos**, dos quais só um par é de fato redundante — não há
maldição da dimensionalidade a combater. O crescimento de dimensão desta base vem da
**codificação categórica**, não das numéricas, e PCA sobre variáveis *dummy* mistura
categorias sem sentido interpretável. E o custo é alto no que mais importa aqui: os
componentes não teriam leitura, e o produto do trabalho é justamente explicar *quais*
características se associam ao sucesso.

**H10, H11 e H13 são hipóteses de *não fazer*.** Estão aqui porque decidir não aplicar uma
técnica exige a mesma evidência que decidir aplicá-la. Aplicar SMOTE a uma base 50/50 ou
remover 17% dos filmes como *outlier* seria cumprir tabela — e o enunciado cobra que
toda decisão seja justificada, inclusive a de não intervir.

### 4.1 Detalhamento das medições

**S1 — vazamento.** Conjunto honesto: AUC 0,832 ± 0,012. Com `max_salas`: 0,940 ± 0,003.
Com `renda`: 0,993 ± 0,002. Com ambos: 0,995 ± 0,001.

Um efeito de segunda ordem vale registro: ampliar o conjunto honesto com fomento e com
as duas ordinais subiu a referência de 0,821 para 0,832 — e **encolheu o ganho do
vazamento na mesma medida** (`max_salas` caiu de +0,122 para +0,108). Atributo honesto
melhor reduz o que o atalho tem a oferecer.

**S2 — definição do alvo.** `sucesso_global` 0,832; `sucesso_no_ano` 0,770. A queda de
0,062 *é* a medida do atalho temporal.

**S3 — partição.** 5-fold aleatório 0,832; treino < 2018 / teste ≥ 2018 (n = 1.068)
0,745. Otimismo de **+0,087**.

**S4 — cardinalidade.** `min_frequency` 1 → 508 colunas, AUC 0,843; 5 → 126 colunas,
0,834; 15 → 79 colunas, 0,834; 60 → 45 colunas, 0,826. A faixa inteira cabe em 0,017, e o
ganho de manter tudo vem de colunas que identificam distribuidoras com pouquíssimos
filmes — memorização que não sobrevive a dados novos.

**S5 — log.** Regressão logística 0,926 → 0,950; floresta 0,940 → 0,940. Árvore
particiona por limiar e só enxerga a **ordem**; `log1p` é monotônica, logo as partições
possíveis são idênticas. É o argumento contra "normalizar tudo por precaução".

**S6 — variância quase nula.** Com `n_ufs` 0,832; sem `n_ufs` 0,832. O efeito é
indistinguível de zero.

---

## 5. Discussão: o principal desafio da base

Somando S1, S2 e S3:

| versão | AUC |
|---|---|
| alvo global · com `renda` e `max_salas` · *k-fold* aleatório | **0,995** |
| alvo relativo ao ano · só atributos pré-estreia · partição temporal | **0,725** |

**0,27 de AUC separa as duas versões, e nenhuma linha de código as distingue à primeira
vista.** As duas rodam sem erro, as duas produzem matriz de confusão e curva
ROC, e a primeira parece muito melhor.

O desafio central desta base não é técnico — não é achar o modelo certo nem ajustar
hiperparâmetro. É **resistir aos três atalhos**. Cada um deles é uma escolha razoável à
primeira vista: a renda está na base e correlaciona lindamente; o número de salas parece
uma característica de lançamento; o *k-fold* aleatório é o padrão de qualquer tutorial.

Um resultado adicional merece registro: **o teto honesto é modesto**. Com AUC em torno
de 0,70 na partição temporal, um modelo que use só informação pré-estreia acerta bem
mais que o acaso, mas está longe de determinar o sucesso. Isso é coerente com o que a
seção 2.5 mostrou — nenhum atributo honesto tem correlação forte com o público — e com
o que se sabe do setor: o desempenho de um filme depende de boca a boca, crítica,
concorrência na semana de estreia e campanha de marketing, nada disso presente na base.

**Dizer isso é parte do resultado.** Um trabalho que reportasse AUC 0,99 sobre estes
dados não teria encontrado um bom modelo: teria encontrado um vazamento.

---

## 6. Encaminhamentos para a Entrega 2

Além de aplicar H1–H12, as melhorias de maior retorno estão detalhadas em
`docs/03-melhorias-e-tradeoffs.md`:

| # | melhoria | impacto | viabilidade |
|---|---|---|---|
| **M7** | data de estreia + **salas na 1ª semana** | muito alto | 🟢 destravada |
| **M1** | fomento público (FSA / leis de incentivo) por CPB | alto | 🟢 destravada |
| **M8** | **alvo = P75 do ano anterior**, com P50 e P90 como robustez | alto | imediata |
| **M2** | histórico de **sucesso** anterior, não só contagem de filmes | alto | imediata |
| M3 | validação temporal com janela deslizante | médio | imediata |
| M5 | alvo alternativo: regressão em `log(publico)` | médio | imediata |

**M7 é a mais valiosa, e resolve o problema aberto da seção 4 (D6).** A bilheteria
diária da ANCINE traz uma linha por obra × sala × dia, com `CPB_ROE` como chave. De
`min(DATA_EXIBICAO)` sai a data exata de estreia; contando salas distintas nos 7
primeiros dias sai **salas na primeira semana** — que é decidida *antes* de o desempenho
ser conhecido. Trocar `max_salas` por ela **converte o atributo de maior poder preditivo
do trabalho (+0,108 de AUC) de vazamento em atributo legítimo**.

Ressalva de cobertura: a série começa em 2014 e alcança **1.617 dos 2.626 filmes
(61,6%)**. Usar esses atributos implica ou restringir a base a 2014–2024 — perdendo a
comparação entre décadas, que é o achado central deste relatório — ou conviver com uma
ausência perfeitamente correlacionada com o período. A escolha é da Entrega 2.

**M1 mudou de natureza.** Os arquivos de fomento existem e foram baixados, mas trazem
apenas o **número do contrato**, não o valor: dão `recebeu_fsa` e `recebeu_incentivo`
como binárias, não o orçamento. Em compensação, o risco de vazamento que suspeitávamos
desapareceu — fomento é aprovado antes de a obra existir.

**M8 é a recomendação da auditoria do alvo**, e é a única da lista que não depende de
fonte nova: `publico > P75 dos filmes brasileiros lançados no ano anterior`. Justifica-se por
três evidências desta EDA — a fronteira empírica entre as duas populações está no percentil
69 (§2.9), os limiares resultantes são interpretáveis em todo o período (154.940 espectadores
em 1995, 47.439 em 2014, 5.278 em 2024), e o percentil do ano anterior é o único conhecido
antes da estreia (§3.5). Com a condição inseparável de **reportar todo resultado também em
P50 e P90**: entre P50 e P75 mudam de classe 24,6% dos filmes; entre P50 e P90, 39,3%
(κ = 0,21). A definição é decisão nossa, defensável mas não única, e a robustez a ela é parte
do resultado.

M2 é a de melhor relação custo-benefício e também a de maior risco: contagem mede
experiência, média anterior mede **reputação** — e qualquer descuido na janela temporal
faz o alvo entrar pela porta dos fundos.

> As três URLs foram testadas em 10/09/2026 e estão em `fontes.PARA_ENTREGA_2`, todas
> **CC-BY**. Não estão no portal do OCA: o host é `dados.ancine.gov.br`, descoberto pela
> API do dados.gov.br renderizada em navegador — ela devolve 401 para cliente externo.

---

## Anexos

| item | onde |
|---|---|
| Notebook executado, com todas as visualizações | `notebooks/` |
| Figuras em PNG (12) | `reports/figuras/` |
| Dicionário de dados | `docs/dicionario-de-dados.csv` |
| Base analítica (2.626 × 28) | `data/processed/filmes.csv` |
| Registro das fontes, com as descartadas | `src/fontes.py` · `docs/01-fontes-de-dados.md` |
| Decisões de escopo (D1–D9) | `docs/02-decisoes-e-escopo.md` |
| Melhorias e trade-offs (S1–S6, M1–M8) | `docs/03-melhorias-e-tradeoffs.md` |

### Reprodução

```bash
pip install -r requirements.txt
python src/ingestao.py
python src/build_dataset.py
python src/sensibilidades.py
jupyter lab notebooks/
```

### Referências das fontes

> ANCINE. *Listagem dos Filmes Brasileiros Lançados Comercialmente em Salas de Exibição
> 1995 a 2024*. Observatório Brasileiro do Cinema e do Audiovisual. Acesso em
> 10 set. 2026.
>
> BANCO CENTRAL DO BRASIL. *IPCA — variação percentual mensal*. Série 433, Sistema
> Gerenciador de Séries Temporais. Acesso em 10 set. 2026.
>
> IBGE. *População residente estimada*. Agregado 6579, variável 9324, API de agregados
> v3. Acesso em 10 set. 2026.
