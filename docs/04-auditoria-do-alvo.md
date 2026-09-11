# Auditoria do alvo — afinal, o que é sucesso de bilheteria neste projeto?

Este documento audita a variável-alvo do projeto. Ele não altera a base: nenhuma linha de
`build_dataset.py` foi mexida. Todos os números aqui saem de
[`src/auditoria_alvo.py`](../src/auditoria_alvo.py), que grava sete tabelas em
[`reports/`](../reports/) e pode ser reexecutado com um comando.

```bash
python src/auditoria_alvo.py
```

A pergunta que estamos respondendo não é "o alvo funciona?". É: **o que a base consegue,
de fato, afirmar sobre o que significa um filme brasileiro ser bem-sucedido?**

---

## Resumo em cinco frases

1. `sucesso_global` **não é uma definição de sucesso; é uma definição de década disfarçada** —
   85,6% dos filmes dos anos 1990 são "sucesso", contra 26,3% dos anos 2020.
2. `sucesso_no_ano` conserta o calendário, mas troca o problema por outro: em 2020 o corte
   cai para **198 espectadores**, e chamar de sucesso um filme que levou 218 pessoas ao
   cinema é indefensável fora da planilha.
3. A mediana **não** é um corte que os dados sugerem: ela é um corte que nós impusemos, e o
   equilíbrio 50/50 é consequência aritmética da escolha, não descoberta empírica.
4. Os dados **sugerem sim** um corte próprio: o público se organiza como **mistura de duas
   populações** (circuito limitado ≈ 900 espectadores; lançamento comercial ≈ 51 mil), e a
   fronteira entre elas fica em ~12 mil espectadores na base inteira — **P68,7**, não P50.
5. A conclusão sobre *quais* filmes deram certo **muda muito** com a definição: de P50 para
   P75 mudam de classe **25% dos filmes**; para P90, **40%**. Isso é uma limitação que
   precisa estar escrita no relatório, não escondida.

**Recomendação:** manter classificação binária, mas **mover o corte de P50 para P75 dentro do
ano**, calculado com a distribuição do **ano anterior**. Justificativa completa na seção 12.

---

## 1. Auditoria das duas definições atuais

### 1.1 `sucesso_global` — público > 2.806 espectadores

| critério | avaliação |
|---|---|
| Interpretação | "O filme vendeu mais ingressos que o filme mediano de 1995–2024." |
| Vantagem | Corte único, estável, trivial de explicar e de reproduzir. |
| Coerência estatística | Razoável como estatística descritiva; a mediana resiste à cauda (a média, 148.399, não resistiria). |
| Coerência com o negócio | **Baixa.** 2.806 espectadores é uma sessão cheia num multiplex médio — cerca de R$ 31 mil de bilheteria. Ninguém no mercado chama isso de sucesso. |
| Coerência com o cinema brasileiro | **Baixa.** A base mistura dois mercados: 910 documentários (35%) com mediana de 1.000 espectadores e 1.639 ficções com mediana de 6.679. O corte global trata os dois como concorrentes da mesma bilheteria. |
| Impacto do período | **Fatal.** Ver tabela abaixo. |
| Inflação / tamanho do mercado | Irrelevante para *público* (é contagem de pessoas, não moeda) — mas o tamanho do mercado mudou de outra forma, muito pior: o número de lançamentos. |
| Interpretabilidade | Alta. |
| Utilidade preditiva | **Enganosa.** AUC 0,74 no teste temporal, mas com 62,8% de positivos no treino contra 31,6% no teste: o modelo é treinado num mundo e testado noutro. |

O problema de período, medido (`reports/alvo_prevalencia_decada.csv`):

| década | % sucesso — `sucesso_global` | % sucesso — `sucesso_no_ano` |
|---|---|---|
| 1990 | **85,6%** | 49,0% |
| 2000 | 75,7% | 49,5% |
| 2010 | 50,2% | 49,8% |
| 2020 | **26,3%** | 49,7% |

Um modelo que só soubesse a década acertaria a maior parte de `sucesso_global`. Isso não é
conhecimento sobre cinema; é leitura de calendário. **`sucesso_global` está reprovado.**

### 1.2 `sucesso_no_ano` — público > mediana do próprio ano

| critério | avaliação |
|---|---|
| Interpretação | "O filme vendeu mais ingressos que o filme brasileiro mediano lançado no mesmo ano." |
| Vantagem | Neutraliza o efeito de período por construção: ~49,7% de positivos em **toda** década. |
| Coerência estatística | Boa em um aspecto (comparação dentro de coorte), frágil em outro: a mediana de anos com 14 a 30 filmes é instável (seção 6). |
| Coerência com o negócio | **Fraca**, e por um motivo específico: o corte oscila entre 198 e 106.579 espectadores conforme o ano. |
| Interpretabilidade | Média — exige explicar que "sucesso" é relativo à safra. |
| Utilidade preditiva | Boa: prevalência idêntica em treino e teste (49,7% / 49,7%), AUC 0,73. |
| Pré-lançamento | **Problema.** A mediana do ano *t* só existe quando *t* acaba (seção 9). |

`sucesso_no_ano` é claramente superior a `sucesso_global`, e a decisão D4 do projeto está
certa nessa comparação. Mas "superior" não é "adequada". Veja os cortes implicados:

| ano | corte (mediana do ano) | ano | corte |
|---|---|---|---|
| 1995 | 14.230 | 2018 | 2.500 |
| 2003 | 106.579 | 2019 | 1.715 |
| 2010 | 7.431 | **2020** | **198** |
| 2013 | 2.376 | 2021 | 267 |
| 2016 | 3.377 | 2024 | 933 |

Os cinco "sucessos" mais modestos de 2020 sob essa definição:

| título | gênero | público | salas |
|---|---|---|---|
| Cidade Pássaro | Ficção | **218** | 7 |
| Soldado Estrangeiro | Documentário | 254 | 10 |
| Sertânia | Ficção | 255 | 5 |
| Os Under-Undergrounds, O Começo | Animação | 258 | 1 |
| Inaudito | Documentário | 293 | 6 |

Esses filmes são rotulados **sucesso** e entram na mesma classe de *Nada a Perder*
(12,2 milhões). Um modelo treinado assim aprende a separar "218 de 190 espectadores", que é
ruído, e é avaliado como se tivesse aprendido bilheteria.

---

## 2. Questionando a mediana

**Por que a mediana?** A razão honesta é que ela é o corte que *sempre funciona*: produz
duas classes cheias, não depende de escolher um número, e sobrevive à assimetria. Nenhuma
dessas razões é sobre cinema. São razões sobre conveniência.

**O que significa estar acima dela?** Exatamente uma coisa: **ser melhor que metade dos
concorrentes**. "Ser melhor que a metade" é uma afirmação sobre *posição no ranking*, não
sobre *desempenho*. São conceitos diferentes e a diferença aparece quando a régua encolhe:
em 2020, ser melhor que metade dos filmes brasileiros significava vender 218 ingressos.

**Um filme ligeiramente acima da mediana é sucesso?** Não. E são muitos: 38 filmes (2,9% dos
positivos) estão entre 1,0x e 1,1x a mediana global; 254 (19,5%) estão a menos de 2x. Há
ainda 16 filmes que ficam *exatamente* na mediana do seu ano e, pelo `>` estrito, são
classificados como fracasso — o filme mediano é, por construção, um fracasso.

**Um filme muito acima recebe o mesmo tratamento?** Sim, e é o custo mais alto da
binarização. Dentro da classe "sucesso global", o maior tem **4.341 vezes** o público do
menor; entre o P1 e o P99 da classe a razão ainda é 1.377. A classe positiva mistura
*Cidade de Deus* com um documentário de 2.900 espectadores e pede ao modelo que os trate
como a mesma coisa.

**O 50/50 é evidência de boa definição?** **Não. É tautologia.** A mediana é *definida* como
o valor que parte a amostra ao meio; obter 50,0% de positivos ao cortar na mediana é o mesmo
que "descobrir" que metade dos números é maior que o do meio. O equilíbrio não diz nada
sobre o fenômeno — se metade dos filmes brasileiros fracassasse comercialmente e a outra
metade triunfasse, ou se 95% fracassassem, **o corte na mediana devolveria 50/50 nos dois
casos**. Ele é incapaz de distinguir os dois mundos, e é exatamente essa distinção que
queremos estudar.

E os dados mostram que vivemos no segundo mundo: **1% dos filmes concentra 36,2% do público;
10% concentram 90,7%; a metade inferior responde por 0,28%** (`reports/alvo_distribuicao.csv`).
Numa distribuição assim, dizer que 50% dos filmes são sucesso é uma afirmação que a própria
base contradiz.

---

## 3. Definições alternativas testadas

Dezesseis definições foram construídas e medidas (`reports/alvo_sensibilidade.csv`). As
principais:

| definição | % positivos | público mínimo de um "sucesso" | público mediano dos "sucessos" | κ vs. `global_P50` | % que muda de classe |
|---|---|---|---|---|---|
| `global_P50` *(atual)* | 50,0 | 2.807 | 22.750 | 1,00 | — |
| `global_P75` | 25,0 | 22.754 | 131.220 | 0,50 | 25,0 |
| `global_P80` | 20,0 | 38.957 | 206.568 | 0,40 | 30,0 |
| `global_P90` | 10,0 | 206.568 | 673.269 | 0,20 | 40,0 |
| `ano_P50` *(atual)* | 49,7 | **218** | 21.776 | 0,68 | 16,1 |
| **`ano_P75`** | **25,1** | 589 | 114.974 | 0,48 | 26,2 |
| `ano_P90` | 10,4 | 6.670 | 560.127 | 0,21 | 39,6 |
| `anoANTERIOR_P75` | 25,3 | 584 | 113.795 | 0,45 | 27,5 |
| `janela5a_P75` | 24,8 | 3.311 | 127.792 | 0,50 | 25,2 |
| `abs_100k` | 13,8 | 102.171 | 424.353 | 0,27 | 36,3 |
| `percapita_P50` | 50,0 | 2.608 | 21.696 | **0,98** | 0,9 |
| `fatia_10pct_do_ano` | 3,3 | 20.499 | 2.219.423 | 0,07 | 46,7 |

Leitura por família:

**A. Percentis globais.** Resolvem o problema conceitual (P90 = 206 mil espectadores é
inegavelmente sucesso) e **agravam** o problema temporal: `global_P90` marca 16,3% dos anos
1990 e 2,6% dos anos 2020. Trocar P50 por P90 sem sair do global é trocar de doença.

**C. Quartis.** Q3 é a alternativa mais interessante e está discutida na seção 12. Q1 não faz
sentido ("sucesso = melhor que os 25% piores" seria ainda mais permissivo que a mediana).

**D. Período em vez de ano.** A janela móvel de 5 anos (`janela5a_P75`) estabiliza o corte em
anos de poucos filmes e concorda 90% com `ano_P75` (κ = 0,90). É defensável, mas custa
interpretabilidade ("percentil 75 da vizinhança de cinco anos" não cabe numa frase) e
introduz olhar-para-o-futuro (usa *t*+1 e *t*+2).

**E. Normalização pelo tamanho do mercado.** **A base não sustenta.** Duas evidências:
- Dividir o público pela população brasileira é inútil: a população cresceu ~1,3x no período
  enquanto o público mediano caiu ~15x. O alvo resultante é indistinguível do original
  (**κ = 0,98**, apenas 0,9% dos filmes mudam de classe).
- Pior: a série do IBGE (agregado 6579) **não cobre 9 dos 30 anos** — 1995–2000, 2007, 2010,
  2022 e 2023 ficam sem `populacao_br`. Qualquer alvo per capita seria indefinido para ~1/3
  do período.
- O que faltaria de verdade é o **público total do mercado brasileiro por ano** (incluindo
  filmes estrangeiros), que a ANCINE publica em *outro* conjunto e que não está nesta base. A
  aproximação disponível — fatia do público *brasileiro* do ano — produz classes de 3,3%
  (87 filmes) e κ = 0,07 com o alvo atual: é outra pergunta, não outra medida da mesma.

**F. Critério de negócio.** O ideal seria **retorno**: público ou receita contra orçamento.
A base **não tem orçamento** (decisão D1: só fontes sem credencial) — e sem ele não existe
"lucro", "ROI" nem "se pagou". Não vamos inventar uma métrica que os dados não sustentam.
O que a base tem de utilizável nessa direção:
- `renda_deflacionada_2024`: correlação de Spearman **0,985** com público — é a mesma
  variável em outra unidade (preço mediano do ingresso: R$ 11,16, faixa R$ 1,39–31,43).
  Não acrescenta informação, e é posterior ao lançamento (D5).
- `max_salas`: ρ = 0,79 com público, mas é o **máximo da carreira**, contaminado pelo
  desempenho (D6). Serve como *descrição* de escala de lançamento, não como alvo nem como
  atributo.

---

## 4. Alvo fácil ou alvo correto?

**A crítica procede, e é melhor admitirmos antes que perguntem.**

A cadeia de decisões foi: o enunciado pede classificação → precisamos de um corte → a mediana
divide ao meio e não exige justificar número nenhum → pronto. Nenhum passo dessa cadeia
passou por "o que o mercado de cinema chama de sucesso". A mediana entrou porque é
*conveniente*: dá classes cheias, dispensa arbitrar um limiar, evita desbalanceamento e
sobrevive à assimetria.

A prova de que a conveniência veio antes do conceito é que a definição **falha o teste mais
simples de validade aparente**: nenhum produtor, distribuidor ou analista da ANCINE diria que
um filme com 2.806 espectadores — ou, em 2020, com 218 — foi bem-sucedido. Uma definição de
sucesso que o especialista do domínio não reconhece não é uma definição de sucesso; é um
ponto de corte.

Isso não invalida o trabalho feito. `sucesso_no_ano` já é uma correção real e bem medida. Mas
a justificativa "a mediana equilibra as classes" precisa sair do relatório: **classe
equilibrada é propriedade desejável de um alvo, nunca critério para escolhê-lo.**

---

## 5. O efeito do tempo

Um filme com 50 mil espectadores em 1995 e outro com 50 mil em 2024 **não são comparáveis**,
e a razão não é a inflação — público é contagem de pessoas, não dinheiro. É a estrutura do
mercado:

- **Volume de lançamentos:** 14 filmes brasileiros em 1995; **197 em 2024** (14x). A mediana
  por filme caiu de 14.230 para 933 em grande parte porque o denominador explodiu.
- **Composição:** documentários eram 13% dos lançamentos nos anos 1990 e são 32–39% desde os
  2000 — em geral com circuito de poucas salas. A mediana caiu, em parte, porque a base passou
  a conter outro tipo de filme.
- **Público total:** o público somado dos filmes brasileiros *cresceu* (3,3 milhões em 1995;
  27,9 milhões em 2019), mas repartido entre muito mais títulos.
- **Pandemia:** 2020 é uma quebra estrutural, não um ano ruim. Público total de **141 mil**
  contra 27,9 milhões em 2019 (−99,5%); só 59 lançamentos; maior filme do ano com 38.043
  espectadores — menos que a mediana de 1998.
- **Streaming e janelas:** desde 2020, parte dos títulos tem lançamento em salas quase
  simbólico, cumprindo janela antes da plataforma. O "público em salas" passou a medir uma
  fração menor do alcance real do filme — e a base não vê essa fração.
- **Deflação:** relevante apenas para `renda`, que já está deflacionada e não é alvo.

**Conclusão:** esses fatores tornam `sucesso_global` **inválido**, não apenas imperfeito. Não
é um viés a corrigir depois; é a variável medindo a coisa errada.

---

## 6. O que exatamente `sucesso_no_ano` mede

"Filme acima da mediana daquele ano" **não** é equivalente a "filme bem-sucedido". É
equivalente a **"filme que teve desempenho acima do filme mediano daquele ano"** — uma
afirmação sobre posição relativa numa coorte, que só vira afirmação sobre sucesso se a coorte
for uma referência estável. Não é o caso:

- **Anos com poucos filmes.** Em 1995 (14 filmes) o IC95% *bootstrap* da mediana vai de
  **5.308 a 155.000 espectadores** — largura de 10,5 vezes a própria mediana. O corte daquele
  ano é praticamente um sorteio.
- **Classe indeterminada.** Em toda a base, **521 filmes (20,0%)** têm público dentro do IC95%
  da mediana do próprio ano: outra amostra do mesmo mercado os colocaria do outro lado do
  corte. Um quinto dos rótulos é ruído amostral (`reports/alvo_estabilidade_mediana.csv`).
- **Quantidade de lançamentos.** O número de filmes do ano correlaciona −0,82 (Spearman) com a
  mediana do ano. O corte é, em boa medida, uma função de quantos filmes estrearam.
- **Períodos atípicos.** 2020 e 2021 têm cortes de 198 e 267 espectadores. A definição obriga
  a declarar que 49,7% dos filmes de 2020 foram bem-sucedidos — num ano em que o mercado
  brasileiro inteiro vendeu menos ingressos que um único filme de 2019.
- **Mudança estrutural.** Antes e depois de 2020 são mercados diferentes; a mediana anual
  esconde isso ao renormalizar tudo para 50%.

`sucesso_no_ano` é um alvo **honesto quanto ao tempo e mudo quanto à magnitude**: ele garante
que nenhuma década é privilegiada, e paga por isso declarando sucesso qualquer filme que
supere a metade da sua safra, por menor que ela seja.

---

## 7. O que a distribuição do público diz

`reports/alvo_distribuicao.csv`, 2.604 filmes com público informado:

| | |
|---|---|
| mediana | **2.806** |
| média | **148.399** (53x a mediana) |
| desvio-padrão | 685.961 |
| assimetria | **10,04** |
| curtose | **135,25** |
| Gini | **0,922** |
| máximo | 12.184.373 (**4.342x** a mediana) |
| top 1% dos filmes | **36,2%** de todo o público |
| top 10% | **90,7%** |
| metade inferior | **0,28%** |

Isso é lei de potência: um Gini de 0,922 é maior que o de qualquer distribuição de renda
nacional do mundo. A cauda **não é anomalia — é o fenômeno**, e removê-la como *outlier*
apagaria o objeto de estudo.

**E há uma estrutura que a mediana ignora.** Em log₁₀, a distribuição é quase simétrica
(assimetria 0,38), e uma mistura de **duas** gaussianas ajusta melhor que uma
(BIC 8.260 contra 8.358) — `reports/alvo_duas_populacoes.csv`:

| período | peso circuito limitado | centro | peso lançamento comercial | centro | fronteira entre as duas |
|---|---|---|---|---|---|
| 1995–2024 | 64% | 915 | 36% | 51.402 | **11.830** |
| 1990 | 53% | 7.159 | 47% | 122.321 | 32.052 |
| 2000 | 58% | 4.124 | 42% | 130.311 | 30.830 |
| 2010 | 73% | 1.378 | 27% | 108.370 | 24.537 |
| 2020 | 70% | 285 | 30% | 9.687 | 3.672 |

Três leituras importantes:

1. **A base contém dois mercados, não um.** Um grupo de filmes de circuito limitado (centro
   em ~900 espectadores; 90% dos documentários caem nele) e um grupo de lançamentos
   comerciais (centro em ~51 mil). A mediana global, 2.806, cai **dentro do primeiro grupo** —
   ou seja, o corte atual separa "circuito limitado bom" de "circuito limitado ruim", e não
   sucesso comercial de fracasso comercial.
2. **A fronteira empírica entre os dois grupos está no percentil 68,7**, não no 50. O dado
   propõe um corte, e ele fica perto de **Q3**.
3. **O grupo comercial é notavelmente estável até 2019** (centro entre 108 mil e 130 mil ao
   longo de três décadas) e **colapsa nos anos 2020** (9.687). Ou seja: o que mudou não foi só
   quantos filmes há — mudou o patamar do próprio lançamento comercial, e por isso um corte
   absoluto único para 1995–2024 também não serve.

**Resposta à pergunta desta seção:** a distribuição diz que sucesso é um fenômeno de cauda,
que a régua deve ser relativa à coorte (porque o patamar muda), e que o corte deve ficar
**na fronteira entre as duas populações — em torno de Q3 —, não na mediana.**

---

## 8. Análise de sensibilidade — a conclusão depende da definição?

**Depende, e muito.** Percentual de filmes que trocam de classe em relação ao alvo atual:

| comparação | filmes que mudam de classe |
|---|---|
| `global_P50` → `ano_P50` | 16,1% |
| `global_P50` → `global_P75` | 25,0% |
| `ano_P50` → `ano_P75` | 24,6% |
| `global_P50` → `global_P90` | 40,0% |
| `ano_P50` → `ano_P90` | 39,3% |
| `global_P50` → `fatia_10pct_do_ano` | 46,7% |

O κ de Cohen entre `global_P50` e `global_P90` é **0,20** — concordância fraca entre duas
definições que qualquer pessoa descreveria como "sucesso de bilheteria". **Trocar o percentil
reescreve entre um quarto e metade da resposta.**

Que tipo de filme entra como sucesso em cada definição (`reports/alvo_prevalencia_genero.csv`):

| gênero | n | público mediano | `global_P50` | `ano_P50` | `ano_P75` | `ano_P90` |
|---|---|---|---|---|---|---|
| Ficção | 1.639 | 6.679 | 61,6% | 61,7% | 35,1% | 15,9% |
| Documentário | 910 | 1.000 | 28,4% | 26,7% | **6,2%** | 0,5% |
| Animação | 54 | 8.478 | 61,1% | 70,4% | 42,6% | 11,1% |

Cortes mais exigentes praticamente eliminam o documentário da classe positiva. Isso é
**informação, não defeito**: documentário brasileiro em geral não disputa bilheteria de
circuito comercial. Mas precisa ser dito na apresentação — é a diferença entre "nosso modelo
prevê sucesso comercial" e "nosso modelo prevê o gênero do filme".

**Esta seção é a limitação central do projeto e deve constar do relatório nesses termos:**
a base mede desempenho de bilheteria com precisão, mas o rótulo "sucesso" é uma decisão
nossa, e escolhas igualmente defensáveis discordam sobre até 40% dos filmes.

---

## 9. Coerência com o objetivo preditivo — e vazamento

| pergunta | resposta |
|---|---|
| O alvo pode ser determinado sem informação posterior ao lançamento? | **Não** — nem poderia: o alvo *é* o resultado. O que precisa ser pré-lançamento são os **atributos**. |
| As variáveis que constroem o alvo são independentes dos preditores? | Só depois de excluir `renda` e `max_salas` (D5/D6). |
| Há risco de vazamento? | **Sim, em quatro pontos.** |

**V1 — `renda_corrente` / `renda_deflacionada_2024`.** ρ de Spearman com público = **0,985**.
É o alvo em outra unidade. Já tratado por D5. *Nunca* como atributo.

**V2 — `max_salas`.** ρ = 0,79. É o máximo da carreira, e distribuidora amplia filme que vai
bem. Já tratado por D6.

**V3 — `mediana_publico_do_ano` (novo).** Essa coluna está em `data/processed/filmes.csv` e
**é o próprio limiar do alvo**. Se entrar como atributo, o modelo recebe metade da resposta e,
combinada com o alvo global, entrega o ano de bandeja. Ela existe para auditoria; precisa
estar na lista explícita de colunas proibidas da Entrega 2, ao lado de `publico` e `renda`.

**V4 — vazamento de coorte (novo, e é o que mais importa aqui).** `sucesso_no_ano` compara o
filme com a mediana do ano *t* — que só é conhecida **em 31 de dezembro de t**. Para prever um
filme que estreia em março, o rótulo depende de filmes que ainda não estrearam. O mesmo vale
para o atributo `filmes_no_ano`, hoje na lista de "honestos": o total de lançamentos do ano é
uma contagem fechada no fim do ano. Nenhum dos dois é observável no momento da previsão.

Custo de corrigir V4, medido: usar o percentil do **ano anterior** (conhecido, publicado, e
não contaminado pelo próprio filme) troca a classe de apenas **9,2%** dos filmes em relação à
mediana do ano corrente (κ = 0,82) e custa cerca de 0,02 de AUC. **É barato e elimina uma
objeção que a professora tem todo direito de levantar.**

Utilidade preditiva de cada alvo, com atributos só pré-estreia e partição temporal
(treino ≤ 2017, teste ≥ 2018) — `reports/alvo_utilidade_preditiva.csv`:

| alvo | AUC teste | % pos. treino | % pos. teste | desequilíbrio |
|---|---|---|---|---|
| `global_P50` | 0,745 | 62,8 | 31,6 | **31,3 pts** |
| `ano_P50` | 0,725 | 49,7 | 49,7 | 0,0 |
| **`ano_P75`** | **0,773** | 25,2 | 25,0 | **0,2** |
| `ano_P90` | 0,828 | 10,6 | 10,2 | 0,3 |
| `anoANTERIOR_P75` | 0,750 | 24,7 | 25,7 | 0,9 |
| `abs_100k` | 0,876 | 19,3 | 5,7 | 13,6 |

Duas advertências sobre esta tabela: (a) AUC não é comparável entre alvos diferentes — cortes
extremos separam grupos mais distantes e sobem o AUC quase automaticamente, então **não use
AUC alto como argumento a favor do P90**; (b) a coluna que importa é a última: alvos relativos
ao ano mantêm a mesma prevalência em treino e teste, alvos globais e absolutos não, e prever
num regime de prevalência diferente do de treino é o caminho mais curto para um modelo
inútil na prática.

---

## 10. O que o artigo de referência acrescenta

[Sen Sharma et al. (2021), *Presenting a Larger Up-to-date Movie Dataset and Investigating the
Effects of Pre-released Attributes on Gross Revenue*](https://arxiv.org/abs/2110.07039) —
três ideias úteis, nenhuma copiada:

1. **Eles deflacionam antes de definir o alvo.** Usam o CPI para trazer receita e orçamento a
   dólares constantes. A lição transposta para nós não é sobre inflação (nosso alvo é
   contagem de pessoas) e sim sobre o princípio: **normalize a medida antes de rotular, nunca
   depois.** É exatamente o argumento contra `sucesso_global`.
2. **Eles não binarizam: usam 10 classes ordenadas de receita**, e reportam *bingo accuracy*
   (30%) ao lado de *one-class-away accuracy* (~60%) — métrica que dá crédito parcial a errar
   por uma faixa. Isso reconhece o que o corte binário apaga: **a distância entre as classes
   tem significado.** Para nós, é a melhoria M-ordinal registrada na seção 12 (faixas
   `circuito limitado / lançamento médio / sucesso comercial / grande sucesso`), inviável como
   alvo principal desta entrega mas excelente como extensão.
3. **Eles constroem *star power* a partir do histórico anterior de elenco e direção** — uma
   variável pré-lançamento derivada de desempenho passado. Nossos `filmes_diretor_antes`,
   `filmes_distribuidora_antes` e `porte_da_distribuidora` são a versão pobre da mesma ideia
   (contam obras, não público acumulado). Com a base atual dá para construir a versão rica:
   *público mediano dos filmes anteriores daquele diretor/distribuidora*, calculado só com
   anos estritamente anteriores. Isso é atributo, não alvo — mas é a melhoria de maior
   retorno esperado para a Entrega 2.

Diferença que precisa ser dita: eles têm **orçamento**, e por isso conseguem falar de retorno.
Nós não temos, e é por isso que nosso conceito de sucesso é necessariamente relativo — não é
preguiça nossa, é limite da fonte.

---

## 11. Os dados definem "sucesso" objetivamente?

**Não.** E essa é uma conclusão, não uma desistência.

A base mede **desempenho de bilheteria** com boa precisão: público por filme, 2.604 registros,
30 anos, fonte oficial. O que ela não contém é o que transformaria desempenho em sucesso:
orçamento (não há como saber se o filme se pagou), meta comercial (um documentário de 5 mil
espectadores pode ter superado a expectativa de quem o financiou), público total do mercado
por ano, e alcance fora das salas.

Transformar essa limitação em decisão metodológica bem justificada tem três passos, e é assim
que ela deve aparecer no relatório:

1. **Declarar o alvo como convenção, não como verdade.** "Definimos sucesso como *desempenho
   de bilheteria no quartil superior da sua coorte anual*" — uma frase que diz exatamente o
   que é medido, sem prometer o que não é.
2. **Escolher o corte com um critério que os dados sustentem**, não com conveniência: a
   fronteira entre as duas populações (P68,7 na base inteira) sustenta Q3; nada nos dados
   sustenta P50.
3. **Publicar a sensibilidade.** Reportar o resultado principal em Q3 e reportar o mesmo
   resultado em P50 e P90 como robustez. Uma conclusão que sobrevive aos três é uma conclusão;
   uma que só existe em um deles é um artefato da definição — e saber disso é resultado.

---

## 12. Conclusões diretas

**1. Nossa definição atual é adequada?**
**PARCIALMENTE.** `sucesso_global` **não** é adequada — mede período, não desempenho (85,6%
contra 26,3% de positivos entre a primeira e a última década). `sucesso_no_ano` é
metodologicamente defensável quanto ao tempo, mas **o corte na mediana não é defensável quanto
ao conceito**: aceita como sucesso um filme de 218 espectadores em 2020, e 20% dos seus
rótulos são estatisticamente indistinguíveis de ruído.

**2. Entre as duas, qual é mais defensável?**
**`sucesso_no_ano`, com folga** — e a decisão D4 acerta. Motivos, em ordem: (i) prevalência
estável por década (49,0 a 49,8) contra 85,6→26,3; (ii) prevalência idêntica em treino e teste
na partição temporal (49,7/49,7 contra 62,8/31,6), que é condição para o modelo ser útil; (iii)
não correlaciona com `ano` (ρ = 0,002 contra −0,364), eliminando o atalho de calendário; (iv) o
custo medido de −0,062 de AUC é o preço de não medir calendário, e é barato. A ressalva: ela
carrega vazamento de coorte (V4) e um corte conceitualmente frouxo.

**3. Existe definição melhor?**
**Sim.** Proposta:

> **`sucesso = público acima do percentil 75 dos filmes brasileiros lançados no ano anterior`**

Em código, sem tocar no resto do pipeline:

```python
# limiar conhecido ANTES da estreia: distribuicao do ano anterior, ja fechado
limiar = d.groupby("ano")["publico"].quantile(0.75).shift(1)
d["sucesso"] = (d["publico"] > d["ano"].map(limiar)).astype("Int64")
```

**4. Os dados sustentam essa definição?**
Sim, e por evidência específica — não por gosto:
- **A fronteira entre as duas populações da base está em P68,7** (mistura de duas gaussianas,
  BIC 8.260 vs. 8.358). Q3 é o quantil redondo mais próximo dessa fronteira empírica. A
  mediana cai *dentro* da população de circuito limitado.
- **O limiar resultante é interpretável em todo o período**: 154.940 espectadores em 1995,
  47.439 em 2014, 5.278 em 2024 — em cada ano, um número que alguém do mercado reconheceria.
- **A prevalência fica estável** (23,0 a 29,1% por década, contra 85,6→26,3 do alvo global) e
  praticamente igual em treino e teste (24,7/25,7), preservando a virtude de `sucesso_no_ano`.
- **Usar o ano anterior elimina o vazamento de coorte** e custa pouco: 9,2% de rótulos
  trocados, ~0,02 de AUC.
- **Não é desbalanceamento problemático**: 25/75 é razão 1:3, tratável com
  `class_weight="balanced"` e avaliação por PR-AUC — e, ao contrário do 50/50, **é a
  proporção que o fenômeno tem**, não a que impusemos.

**5. A escolha é robusta?**
**Não, e isso precisa estar escrito.** Entre P50 e P75 mudam de classe 24,6% dos filmes; entre
P50 e P90, 39,3% (κ = 0,21). Qualquer conclusão do projeto sobre "o que prevê sucesso" deve
ser reportada com a análise de sensibilidade da seção 8 ao lado. É por isso que a recomendação
inclui rodar o resultado final nos três cortes.

**6. Recomendação para a Entrega 1**
Como a entrega é exploratória e a base não deve ser alterada, a recomendação é **documental,
não corretiva**:

| # | ação | esforço |
|---|---|---|
| R1 | Manter `sucesso_global` e `sucesso_no_ano` na base — a comparação entre elas é resultado do trabalho. | zero |
| R2 | Reescrever a justificativa do alvo no relatório: sair de "a mediana equilibra as classes" para "a mediana é uma convenção conveniente cujos limites medimos". | texto |
| R3 | Incluir esta auditoria como seção/anexo, com as tabelas 7 e 8 (distribuição, duas populações, sensibilidade). | já pronto |
| R4 | Registrar as duas limitações novas no diagnóstico: **classe indeterminada em 20% dos filmes** e **vazamento de coorte (V4)**. | texto |
| R5 | Acrescentar `mediana_publico_do_ano` e `filmes_no_ano` à lista de colunas proibidas na modelagem. | 2 linhas |
| R6 | Anunciar `ano_P75 (do ano anterior)` como **alvo principal proposto para a Entrega 2**, com `ano_P50` reportado como comparação. | texto |
| R7 | Registrar como melhoria futura o **alvo ordinal de quatro faixas** (circuito limitado / médio / comercial / grande sucesso), inspirado nas 10 classes de Sen Sharma et al. | texto |

Só R5 toca em código, e é uma lista de exclusão — não muda a base.

---

## 13. Pensando como a professora

**A primeira pergunta será: "Por que acima da mediana significa sucesso?"** E a segunda,
inevitável: *"Então metade dos filmes brasileiros é um sucesso?"*

Perguntas prováveis, e a resposta curta de cada uma:

| pergunta | resposta |
|---|---|
| "Por que a mediana?" | Porque era conveniente. Testamos, e por isso estamos propondo Q3: é o quantil mais próximo da fronteira empírica entre as duas populações da base (P68,7). |
| "50/50 não é bom sinal?" | É tautologia: cortar na mediana devolve 50/50 em qualquer distribuição. O 50/50 não é evidência sobre o fenômeno. |
| "2.806 espectadores é sucesso?" | Não. Por isso mudamos de corte. |
| "E o filme de 218 espectadores em 2020?" | É o caso que reprovou a mediana anual. Com Q3, o corte de 2020 vai para 581. |
| "Dá para comparar 1995 com 2024?" | Não diretamente: 14 lançamentos contra 197, e público mediano 15x menor. Por isso o alvo é relativo ao ano. |
| "Vocês não estão usando o futuro?" | Estávamos: a mediana do ano fecha em dezembro. A proposta usa o ano anterior. |
| "E a pandemia?" | 2020 é quebra estrutural (−99,5% de público). O alvo relativo absorve; a análise de sensibilidade mostra quanto. |
| "Por que não regressão?" | A cauda domina (Gini 0,92; 1% dos filmes = 36% do público). Registramos regressão em log como extensão. |
| "Esse alvo é só gênero disfarçado?" | Risco real: com Q3, só 6,2% dos documentários são positivos. Precisa ser reportado, e o modelo avaliado também dentro de cada gênero. |

**A resposta de 10 minutos — "por que acima da mediana significa sucesso?":**

> "Não significa. Foi o que descobrimos ao auditar nosso próprio alvo.
> A mediana parecia boa porque dá classes equilibradas — mas esse equilíbrio é aritmética, não
> achado: cortar na mediana devolve 50/50 em qualquer distribuição. E o público brasileiro não
> é uma distribuição qualquer: 1% dos filmes concentra 36% do público e a metade inferior fica
> com 0,28%. Numa distribuição dessas, dizer que metade dos filmes é sucesso contraria os
> próprios dados.
> Então perguntamos onde os dados colocariam o corte. O público, em escala logarítmica, é uma
> mistura de duas populações: filmes de circuito limitado, em torno de 900 espectadores, e
> lançamentos comerciais, em torno de 51 mil. A fronteira entre as duas cai no percentil 69 —
> e a mediana cai dentro da primeira. Ou seja, nosso corte antigo separava circuito limitado
> bom de circuito limitado ruim.
> Nossa proposta é o quartil superior da safra do ano anterior. Quartil superior porque é o
> quantil que corresponde à fronteira entre as duas populações; do ano anterior porque é o
> único limiar que existe antes da estreia. Isso dá cortes que fazem sentido para quem é do
> mercado: 155 mil espectadores em 1995, 5,3 mil em 2024.
> E fomos honestas sobre o preço: mudar de mediana para quartil superior reclassifica um
> quarto dos filmes. Por isso vamos reportar o resultado nos três cortes — P50, P75 e P90.
> Se a conclusão sobrevive aos três, é conclusão; se só existe em um, é artefato da definição."

---

## Afinal, o que é sucesso de bilheteria neste projeto?

**Não existe definição objetiva de sucesso nesta base, e afirmar que existe seria o erro.** A
ANCINE nos dá desempenho de bilheteria — quantas pessoas compraram ingresso — e não nos dá
orçamento, meta comercial nem alcance fora das salas. Sem orçamento não há "se pagou"; logo,
qualquer noção de sucesso aqui é necessariamente **relativa a uma coorte de comparação**.

Escolhida a coorte, os dados têm sim uma coisa objetiva a dizer, e ela contraria nossa
definição atual: o público brasileiro não é uma distribuição contínua a ser partida ao meio,
e sim **duas populações distintas** — cerca de dois terços dos filmes em circuito limitado
(centro em ~900 espectadores) e um terço em lançamento comercial (centro em ~51 mil), com
fronteira no **percentil 69**. A mediana fica dentro da primeira população. O quartil superior
fica em cima da fronteira.

**Definição recomendada:** *sucesso = público acima do percentil 75 dos filmes brasileiros
lançados no ano anterior.* Relativa porque a base não sustenta absoluto; do ano anterior
porque é o único limiar existente antes da estreia; no quartil superior porque é onde os
dados, e não a conveniência, colocam a fronteira entre os dois mercados que esta base contém.

E com uma condição inseparável: **toda conclusão do projeto deve ser reportada também em P50 e
P90.** A definição é uma decisão nossa, defensável mas não única — e a robustez a essa decisão
é parte do resultado, não apêndice dele.
