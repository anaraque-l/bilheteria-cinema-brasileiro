# Roteiro da apresentação — Entrega 1 (EDA)

**CIN0144 · Bilheteria do cinema brasileiro · ~10 minutos**
**Grupo 11 — Ana Laura, Ana Raquel e Laura Virgínia**

---

## O projeto em uma frase

Para a capa, para a abertura falada e para o resumo do relatório:

> **Queríamos prever quais filmes brasileiros dão certo — e descobrimos que a forma
> óbvia de definir "dar certo" faz o modelo aprender o calendário, não o cinema.**

Variantes, conforme o espaço:

| Onde | Frase |
|---|---|
| **Capa / título** | Prever bilheteria antes da estreia: quando o alvo mede a coisa errada |
| **Uma linha** | Um modelo com AUC 0,99 que não aprendeu nada sobre cinema. |
| **Abertura falada** | O filme brasileiro mediano é visto por 2.806 pessoas. O maior foi visto por 12 milhões. Queríamos saber o que separa os dois — antes da estreia. |

## A definição formal (T · P · E)

- **T** — classificar se um filme brasileiro lançado comercialmente alcançará público
  **acima da mediana do seu ano de lançamento**.
- **P** — AUC, F1, acurácia e matriz de confusão, sob **partição temporal** (treino até
  2017, teste de 2018 em diante), que é a que corresponde ao uso real: prever um filme
  que ainda não estreou.
- **E** — 2.626 filmes lançados entre 1995 e 2024, com 35 atributos vindos da listagem
  da ANCINE, dos registros de fomento público, do IPCA e do IBGE — **nenhum deles
  posterior à estreia**.

---

## A espinha: uma apresentação, não três

O erro clássico de grupo é cada pessoa apresentar *a sua parte*. A banca ouve três
mini-palestras e não guarda nenhuma. O que une três pessoas é **um argumento único, em
três atos**, em que cada um só faz sentido depois do anterior:

| Ato | Quem | A frase que o ato defende |
|---|---|---|
| **1** | pessoa 1 | "A bilheteria é **absurdamente desigual** — e isso decide tudo." |
| **2** | pessoa 2 | "A definição óbvia de sucesso **mede o ano**, não o filme." |
| **3** | pessoa 3 | "E nada disso é opinião: **medimos tudo**, inclusive os três atalhos." |

**Cada passagem de bastão é uma pergunta que a próxima pessoa responde.** Estão no
roteiro, em itálico. Decorem a sua — é o que faz a costura aparecer.

**A tese, em uma frase.** Se a banca só levar uma ideia embora:

> Nesta base, o caminho fácil entrega AUC 0,995 e o honesto entrega 0,725 — e **nenhuma
> linha de código distingue os dois**.

---

## Divisão: 3 pessoas × 3 telas

Nove telas, ~65 s cada, **9 min 40** com 20 s de folga.

| Ato | Telas | Quem | Tempo |
|---|---|---|---|
| 1 — A base e a desigualdade | 1–3 | pessoa 1 | 3:15 |
| 2 — O alvo que mede o ano | 4–6 | pessoa 2 | 3:15 |
| 3 — A prova e os três atalhos | 7–9 | pessoa 3 | 3:10 |

**Dois relógios:** aos **3:15** a pessoa 1 termina; aos **6:30** a pessoa 2 termina.
Perguntas: **quem é dono do ato responde**.

---

# ATO 1 — pessoa 1 · "a bilheteria é absurdamente desigual" (3:15)

## Tela 1 — A pergunta (60 s)

**Abram com os dois números, um ao lado do outro:**

> "O filme brasileiro **mediano** é visto por **2.806 pessoas**. O maior da série, *Nada
> a Perder*, foi visto por **12,2 milhões**. É uma diferença de **4.342 vezes**. A
> pergunta do nosso trabalho: dá para saber de que lado um filme vai cair — **antes da
> estreia**?"

Aí o enquadramento:

- Classificação binária. O alvo, o limiar e a restrição de informação estão os três
  nomeados na pergunta.
- **A restrição é o que define o trabalho.** Renda, número de salas, tudo que é medido
  *depois* da estreia está fora. Só entra o que um produtor sabe quando ainda está
  decidindo.

> 🗣 *"Para responder isso, precisamos de uma base. E ela deu trabalho."*

## Tela 2 — A base e a coleta (60 s)

- **2.626 filmes**, 1995–2024, **35 atributos**. Cinco fontes federais abertas: listagem
  da ANCINE, os dois registros de **fomento público**, IPCA do Banco Central e IBGE.
  **Nenhuma exige cadastro ou chave.**

**A coleta tem duas histórias que valem 20 segundos:**

> "O portal do gov.br roda Plone, e a URL do arquivo **não devolve o arquivo** — devolve
> a página dele. HTTP 200, `text/html`. O CSV só vem com o sufixo `/@@download/file`.
> Sem isso, o pandas lê HTML e quebra com um erro que não aponta para a causa."

> "E os arquivos de fomento **não estão no portal**. O catálogo é uma aplicação de
> página única cuja API devolve 401 para cliente externo. Renderizando a página num
> navegador, a mesma API responde 200 e revela um host que não é linkado em lugar
> nenhum: `dados.ancine.gov.br`."

*(Se sobrar fôlego: o arquivo tem 47 linhas de rodapé que o pandas lê como filmes, a
falta vem como texto — `ND` e `-` — e os números são pt-BR.)*

> 🗣 *"Com a base pronta, a primeira coisa que olhamos foi a distribuição do público."*

## Tela 3 — A cauda (75 s) · fig. `fig01-distribuicao-publico.png`

**Três frases, nesta ordem:**

> "Na escala linear, o gráfico é uma barra colada no zero — a variação que importa para
> 99% dos filmes é **invisível**. Em log, aparece: a distribuição se espalha por **sete
> ordens de grandeza**, de 2 espectadores a 12 milhões."

> "A concentração é extrema. **1% dos filmes concentra 36% de todo o público. 10%
> concentram 91%. A metade inferior da base inteira responde por 0,28%.**"

> "Isso tem duas consequências imediatas para a modelagem: média e desvio-padrão são
> inúteis como resumo — a média é 53 vezes a mediana; e **a cauda não é outlier a
> remover, é o fenômeno**. O critério IQR marca 17,4% dos filmes, e remover isso
> eliminaria justamente o que queremos aprender a reconhecer."

> 🗣 *"Diante dessa desigualdade, como é que se define 'sucesso'? [Nome] vai mostrar que
> essa pergunta é o trabalho inteiro."*

---

# ATO 2 — pessoa 2 · "o alvo mede o ano" (3:15)

## Tela 4 — O mercado mudou de natureza (55 s) · fig. `fig02-evolucao-anual.png`

| ano | lançamentos | público mediano |
|---|---|---|
| 1995 | 14 | 14.230 |
| 2024 | 197 | **933** |

> "Os lançamentos cresceram **14 vezes**. O público mediano por filme **caiu 15 vezes**.
> Não é que o cinema brasileiro tenha encolhido — o público total não caiu na mesma
> proporção. É que entrou uma quantidade enorme de documentário e produção de circuito
> limitado que antes não chegava à sala. **A queda da mediana é efeito de composição.**"

> 🗣 *"Guardem esse número, porque ele vai explodir na próxima tela."*

## Tela 5 — O achado central (85 s) · fig. `fig08-alvo-por-decada.png`

**Esta é a tela mais forte da apresentação. Não corram nela.**

> "A definição óbvia é: sucesso = público acima da mediana da base. Ela produz classes
> **perfeitamente equilibradas** — 50,0% contra 50,0%. Parece impecável, e a gente
> quase seguiu em frente."

Aí mostrem a figura:

| década | mediana **global** | mediana **do ano** |
|---|---|---|
| 1990 | **85,6%** | 49,0% |
| 2000 | 75,7% | 49,5% |
| 2010 | 50,2% | 49,8% |
| 2020 | **26,3%** | 49,7% |

> "Desagregado por década: **85,6% dos filmes dos anos 1990 são 'sucesso', contra 26,3%
> dos anos 2020.** Quase 60 pontos de diferença. O alvo não está medindo sucesso — está
> medindo **antiguidade**."

> "Um modelo que receba o ano como atributo encontra esse atalho, atinge AUC alto e
> **não aprendeu absolutamente nada sobre cinema**."

**E a conclusão que a banca não espera:**

> "Isso também significa que **não há desbalanceamento a tratar** nesta base — as
> classes já estão em 50/50 por construção. SMOTE aqui seria cumprir tabela. O
> desbalanceamento real não está na proporção de classes: está na **distribuição do
> alvo ao longo do tempo**."

> 🗣 *"E o que sobra para prever, quando se tira o ano da jogada?"*

## Tela 6 — Fomento público: o que de fato separa (55 s) · fig. `fig09-fomento.png`

| origem do fomento | filmes | taxa de sucesso | público mediano |
|---|---|---|---|
| sem fomento | 843 | 0,33 | 1.495 |
| **só FSA** | 339 | 0,40 | **535** |
| só incentivo | 932 | 0,55 | 7.472 |
| **FSA e incentivo** | 476 | **0,77** | 7.562 |

> "Juntamos os registros de fomento da ANCINE por CPB — cobrem 67% da base. E o que
> torna esse atributo utilizável é que **fomento é aprovado antes de a obra existir**.
> Não há como carregar o desempenho."

> "O gradiente é forte: 33% sem fomento, **77% com os dois mecanismos**. E há uma
> inversão: o grupo *só FSA* tem público mediano de **535 espectadores**, abaixo de quem
> não teve fomento nenhum. Isso não é crítica ao FSA — é descrição do que ele financia:
> muito documentário e circuito limitado."

⚠️ **Digam a ressalva, é o que impede a pergunta:**

> "O FSA foi criado em 2006, então o indicador de FSA tem **ρ = 0,511 com o ano** — é em
> parte um marcador de filme recente. Mas dentro dos anos 2010 isoladamente o gradiente
> se mantém, 80% contra 29%. O efeito sobrevive ao controle temporal."

> 🗣 *"Até aqui, tudo isso é argumento. E argumento pode estar errado. [Nome] vai mostrar
> o que aconteceu quando medimos."*

---

# ATO 3 — pessoa 3 · "a prova, e os três atalhos" (3:10)

## Tela 7 — A prova do ato 2 (55 s) · fig. `fig10-correlacao-com-alvo.png`

**Esta tela existe para transformar o argumento da pessoa 2 em número.**

> "No ato 2 vocês ouviram que definir sucesso pela mediana do próprio ano neutraliza o
> calendário. Isso é afirmação. Aqui está a medida: **o ano tem correlação de +0,002 com
> o alvo**. Dois milésimos. A quantidade de filmes lançados no ano, +0,003. O calendário
> saiu da jogada, e não por convencimento — por número."

> "O que sobra é modesto, e isso era esperado. O atributo honesto mais associado ao alvo
> é a quantidade de projetos de incentivo, **+0,274**, seguido do histórico da direção,
> +0,193, e do da distribuidora, +0,183. Nenhum chega a 0,3. Se um atributo sozinho
> explicasse o sucesso de um filme, não existiria indústria de cinema."

> "E o painel da direita muda o ranking. Para categórica, Spearman não serve: usamos o
> **V de Cramér**. **Gênero, com 0,338, é o atributo mais associado ao alvo em toda a
> base** — acima de qualquer numérica. Isso tem consequência prática imediata: nesta
> base, a codificação das categóricas importa mais que a transformação das numéricas."

> 🗣 *"Essa é a medida de uma decisão que a gente acertou. Faltam as três que a gente
> quase errou."*

## Tela 8 — Os três atalhos (85 s) — **o diferencial**

**A tela que nenhum outro grupo vai ter.**

> "Uma hipótese sem número é palpite. Rodamos um protocolo fixo — floresta aleatória,
> 5 folds, todo o pré-processamento dentro do fold — e medimos a **diferença** entre duas
> versões da base. O modelo aqui é termômetro: nenhum destes números é o desempenho do
> nosso modelo."

**Atalho 1 — usar a renda.** Conjunto honesto: AUC **0,832**. Com a renda: **0,993**
(+0,161). Renda é público × preço do ingresso, ρ = 0,99. É a resposta.

**Atalho 2 — usar o máximo de salas.** +0,108 de AUC. E aqui está o argumento mais
sutil do trabalho:

> "o máximo de salas *parece* característica de lançamento — a nossa proposta inicial listava
> ele como atributo. Mas o campo é o máximo atingido **durante** a carreira: distribuidora
> expande filme que vai bem. O número de salas é, em parte, **consequência** do sucesso,
> não causa. Sem a data de estreia, não dá para separar as duas parcelas — então
> excluímos, e publicamos quanto ele valeria."

**Atalho 3 — validar errado.** *k-fold* aleatório: 0,832. Treinar até 2017 e testar de
2018 em diante: **0,745**. O aleatório é **+0,087 otimista**, porque põe filmes de 2019
no treino e de 2015 no teste — o modelo enxerga o futuro.

**E um resultado de segunda ordem que vale citar:**

> "Quando ampliamos o conjunto honesto com o fomento e com duas variáveis ordinais, a
> referência subiu de 0,821 para 0,832 — e **o ganho do vazamento encolheu na mesma
> medida**. Atributo honesto melhor não só melhora o modelo: reduz o que o atalho tem a
> oferecer."

## Tela 9 — Hipóteses e fecho (50 s)

| Evidência | Hipótese |
|---|---|
| Alvo global embute o ano | adotar o alvo relativo ao ano — **medido: −0,062** |
| Renda e máximo de salas são posteriores | excluir — **medido: −0,163** |
| Uso real é prever filme não estreado | partição temporal — **medido: −0,087** |
| Assimetria 10,0 | log só no modelo linear — **medido: +0,024 vs 0,000** |
| 467 distribuidoras, 287 com um filme | agrupar as raras, corte de 5 a 15 — **medido: −0,009** |
| Classes já em 50/50 | **não** balancear |
| Cauda é o fenômeno | **não** remover outlier |
| Indicador de FSA com ρ = 0,511 com o ano | usar só junto com o ano no modelo |

**O fecho (20 s):**

> "O que diferencia esta EDA é que **cada hipótese tem justificativa empírica, não de
> checklist** — inclusive as duas de *não fazer*. E a lição do trabalho é que o caminho
> fácil entrega 0,995, o honesto entrega 0,725, e **nenhuma linha de código distingue os
> dois**."

---

## O que ficou de fora, de propósito

Dez minutos não comportam a EDA inteira. Cada item abaixo **está no notebook e no
relatório**, e vira **uma frase** se perguntarem:

| Ficou de fora | A frase de resposta |
|---|---|
| **Gênero** | "Animação e ficção têm mediana uma a duas ordens acima de documentário, mas as caixas se sobrepõem muito — gênero informa, não determina. E *Videomusical* tem um único filme." |
| **Correlação** | "Usamos Spearman, não Pearson, por causa da assimetria de 10. E há redundância que nós mesmos criamos: a contagem de filmes anteriores da direção e o indicador de estreia têm ρ = 0,98." |
| **PCA** | "Descartado, e não por esquecimento: são 11 numéricas úteis, e o crescimento de dimensão vem da codificação categórica, não delas." |
| **Inventário dos ausentes** | "Há quatro naturezas distintas de ausência. Os 60% sem produtora minoritária não são falta: o filme não teve coprodutora. Já o máximo de salas é MNAR, porque os filmes sem o campo têm público mediano muito menor — a própria ausência informa." |
| **Consistência da base** | "O preço médio implícito do ingresso, renda dividida por público, tem mediana de R$ 11,16 e nunca sai de faixa plausível. Nenhum valor negativo, nenhuma duplicata, nenhum CPB repetido." |
| **Cardinalidade** | "O campo de UF tem 87 valores distintos para 27 unidades da federação, porque a ANCINE concatena as UFs das coprodutoras. E são 467 distribuidoras, das quais 287 aparecem num filme só." |
| **Ordinais e região** | "As duas ordinais se comportam diferente: a experiência da direção sobe de 0,43 a 0,69 e satura; o porte da distribuidora não é monótono, cai na faixa grande, porque mede volume de catálogo e não poder comercial. Entre as UFs com pelo menos 30 filmes, Pernambuco aparece em segundo, com 0,53." |

---

## Plano de corte (se estourar)

Cortem **tela inteira**, nunca acelerando a fala:

| ordem | o que fazer | ganha |
|---|---|---|
| 1º | Tela 2 — cortem a segunda história da coleta | 20 s |
| 2º | Tela 6 — cortem a inversão do *só FSA*, mantenham o gradiente | 20 s |
| 3º | Tela 7 — cortem o painel do V de Cramér, mantenham o +0,002 do ano | 25 s |

**Intocáveis:** telas 3, 5 e 8, e o número +0,002 da tela 7. São as que sustentam a nota.

---

## Ensaio — checklist

- [ ] Cronometrar **cada ato separadamente**. O problema típico é a pessoa 1 gastar 5
      minutos na tela 1.
- [ ] Ensaiar as **passagens de bastão em voz alta** — é a costura, e é onde grupo trava.
- [ ] Cada pessoa responde as perguntas do **seu** ato.
- [ ] Notebook **já executado e aberto** antes de começar.
- [ ] Números de cor: **2.626 × 35**, **2.806**, **4.342×**, **85,6% vs 26,3%**,
      **0,995 vs 0,725**, **+0,002** do ano com o alvo.
- [ ] Uma pessoa só no mouse.

---

## Perguntas prováveis — e a resposta curta

**"Vocês não trataram o desbalanceamento?"**
Não há desbalanceamento: o corte pela mediana produz 50,0/49,7 por construção. Provamos
isso e registramos como hipótese de **não fazer** — aplicar SMOTE numa base equilibrada
seria cumprir tabela. O desbalanceamento real desta base é temporal, e está na seção do
alvo.

**"Se vocês mediram AUC, não é modelagem? Não fugiram do escopo da EDA?"**
O modelo é instrumento de medida, não entregável. Rodamos **um** protocolo fixo e
reportamos sempre a **diferença** entre duas versões da base — nunca o desempenho de um
modelo escolhido. Nenhuma transformação testada foi aplicada à base entregue: elas vivem
dentro do fold e morrem no fim da função.

**"Por que não removeram os outliers de público?"**
Porque não são erros — são os blockbusters, e o fenômeno que queremos prever. A
distribuição é log-normal e o critério de Tukey pressupõe simetria: ele marca 17,4% da
base. O tratamento é log, não remoção.

**"O máximo de salas não é uma característica de lançamento?"**
Em parte sim, e é o ponto mais discutível do trabalho — por isso o deixamos explícito. O
campo é o **máximo atingido durante a carreira**, e distribuidora expande filme que vai
bem. Sem a data de estreia não dá para separar a parcela decidida antes da que reagiu ao
desempenho. Na dúvida escolhemos a versão que não pode inflar o resultado, e publicamos
o número da outra: +0,108.

**"Por que a base vai só até 2024?"**
Porque a edição 1995–2025 **não existe**. Sondamos as URLs: as de 2025 devolvem 404. A
publicada mais recente é a `1995 a 2024r`, retificada.

**"Vocês não têm duração do filme?"**
A ANCINE não publica. A fonte aberta que traria (Wikidata, CC0) não era alcançável do
nosso ambiente. Está registrado como limitação e como melhoria, não silenciado.

**"O fomento não é vazamento?"**
Não, e essa é justamente a diferença para a renda e para as salas: fomento é **aprovado
antes de a obra existir**. O que exige cuidado é outra coisa — o indicador de FSA tem
ρ = 0,511 com o ano, porque o FSA foi criado em 2006. Por isso ele só entra junto com o ano no
modelo.

**"Por que duas variáveis ordinais e não numéricas?"**
Porque as faixas têm ordem natural e essa ordem é informação — uma direção *veterana*
fez mais filmes que uma *iniciante*. Como numérica, assumiríamos que a distância entre
faixas é constante, o que não é verdade; como nominal, jogaríamos a ordem fora.

**"Qual o desempenho do modelo de vocês?"**
Não temos um — a Entrega 1 é exploratória. O que temos é a medida de quanto cada decisão
de pré-processamento custa, e a faixa em que um modelo honesto vai cair: **AUC em torno
de 0,73** na partição temporal.
