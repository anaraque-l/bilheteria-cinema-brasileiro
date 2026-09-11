# Melhorias, trade-offs e sensibilidades

Este documento responde a três perguntas para cada decisão em aberto: **quanto vale**,
**quanto custa** e **dá para fazer?**

A primeira parte (S1–S6) traz o que já foi **medido**. A segunda (M1–M8) traz melhorias
propostas, com impacto estimado e viabilidade avaliada.

---

## Parte I — O que já foi medido

**Protocolo.** Floresta aleatória (300 árvores), 5-fold estratificado, semente 42, todo
o pré-processamento dentro dos folds via `Pipeline`. O que se compara é sempre a
**diferença** entre duas versões da base.

> O modelo é **instrumento de medida**, como um termômetro. Nenhum número desta seção é
> "o desempenho do nosso modelo" — a modelagem é a Entrega 2. A base entregue em
> `data/processed/filmes.csv` permanece sem imputação, sem remoção de *outlier* e sem
> codificação.

Reproduzir: `python src/sensibilidades.py`

### Quadro-resumo

| # | decisão | efeito no AUC | veredito |
|---|---|---|---|
| S1 | incluir `renda` | **+0,161** | vazamento — excluir |
| S1 | incluir `max_salas` | **+0,108** | vazamento provável — excluir |
| S2 | alvo relativo ao ano | **−0,062** | adotar mesmo assim |
| S3 | validação aleatória | **+0,087** (otimismo) | usar temporal |
| S4 | agrupar categorias raras | **−0,009** | adotar (`min_frequency` 5–15) |
| S5 | `log1p` | **+0,024** linear · **0,000** árvore | só onde faz diferença |
| S6 | remover `n_ufs` | **0,000** | remover (é ruído) |

### S1 — Vazamento: o que cada atributo posterior entrega

| conjunto de atributos | AUC | Δ |
|---|---|---|
| honesto (só o que se sabe antes de estrear) | 0,832 ± 0,012 | — |
| + `max_salas` | 0,940 ± 0,003 | **+0,108** |
| + `renda_deflacionada_2024` | 0,993 ± 0,002 | **+0,161** |
| + ambos | 0,995 ± 0,001 | +0,163 |

**Leitura.** A renda sozinha praticamente resolve o problema — porque é a resposta.
O salto de 0,12 do `max_salas` é grande demais para um atributo de lançamento.

**Peso da decisão.** Excluir os dois custa **0,17 de AUC**, e é o que separa um
resultado honesto de um resultado inflado.

### S2 — Definição do alvo

| alvo | AUC | taxa de positivos por década |
|---|---|---|
| `sucesso_global` | 0,832 | 0,86 / 0,76 / 0,50 / 0,26 |
| `sucesso_no_ano` | 0,770 | 0,49 / 0,50 / 0,50 / 0,50 |

**Trade-off.** `sucesso_global` dá o número mais bonito e é a leitura literal do
enunciado. `sucesso_no_ano` responde à pergunta que interessa — *este filme foi bem
para o seu tempo?*

**Recomendação.** `sucesso_no_ano` como principal. A queda de 0,062 **é** a medida do
atalho temporal: era o quanto o modelo ganhava só por saber o ano.

### S3 — Partição aleatória × temporal

| protocolo | AUC (`sucesso_global`) | AUC (`sucesso_no_ano`) |
|---|---|---|
| 5-fold aleatório | 0,832 | 0,770 |
| treino < 2018 / teste ≥ 2018 | 0,745 | 0,725 |
| **otimismo** | **+0,087** | **+0,045** |

**Viabilidade.** Custa uma linha de código. É a mudança de melhor relação
custo-benefício do trabalho.

### S4 — Cardinalidade da distribuidora

| `min_frequency` | colunas | AUC |
|---|---|---|
| 1 (todas as 467) | 508 | 0,843 ± 0,013 |
| 5 | 126 | 0,834 ± 0,011 |
| 15 | 79 | 0,834 ± 0,012 |
| 30 | 59 | 0,832 ± 0,012 |
| 60 | 45 | 0,826 ± 0,012 |

A faixa inteira cabe em **0,017**, e o desvio entre folds é ~0,012 em toda ela. O ganho
de manter tudo vem de colunas que identificam distribuidoras com pouquíssimos filmes —
memorização, que não sobrevive a dados novos.

**Recomendação.** `min_frequency` entre 5 e 15: custa 0,009 de AUC e corta de 508 para
~100 colunas, ordem de grandeza compatível com 2.626 linhas.

### S5 — Transformação logarítmica

| modelo | cru | `log1p` | Δ |
|---|---|---|---|
| regressão logística | 0,926 | 0,950 | **+0,024** |
| floresta aleatória | 0,940 | 0,940 | **0,000** |

**Por que zero na árvore.** Árvore particiona por limiar e só enxerga a **ordem** dos
valores; `log1p` é monotônica, logo as partições possíveis são idênticas.

**Consequência prática.** A transformação não deve ser aplicada à base, e sim entrar
como etapa do `Pipeline` **dos modelos que precisam dela**. É o argumento contra
"normalizar tudo por precaução".

### S6 — Atributo de variância quase nula

`n_ufs` tem a moda concentrando **97,1%** dos registros. Removê-lo **não muda o AUC**
(0,832 nos dois casos), com desvio entre folds de 0,012 — indistinguível de zero.

**Recomendação.** Remover, por parcimônia. É a decisão de menor risco do trabalho, e o
ponto metodológico é que agora sabemos disso por medição, não por intuição.

---

## Parte II — Melhorias propostas

Impacto estimado, custo e viabilidade. Ordenadas por relação impacto/custo.

| # | melhoria | impacto esperado | custo | viabilidade |
|---|---|---|---|---|
| **M7** | **data de estreia + salas na 1ª semana** | **muito alto** | médio | 🟢 **destravada** |
| M9 | ordinais a partir do histórico | médio | baixo | ✅ **IMPLEMENTADA** |
| ~~M1~~ | ~~fomento público (FSA / leis de incentivo)~~ | alto | baixo | ✅ **IMPLEMENTADA** |
| M2 | histórico de **sucesso** (não só de contagem) | alto | baixo | 🟢 imediata |
| M3 | validação temporal com janela deslizante | médio | baixo | 🟢 imediata |
| M4 | consolidar entidade fragmentada | médio | médio | 🟡 exige critério |
| M5 | alvo alternativo: regressão em `log(publico)` | médio | baixo | 🟢 imediata |
| M8 | share do público do ano como alvo contínuo | baixo | baixo | 🟢 imediata |
| M6 | duração via Wikidata | médio | baixo | 🔴 bloqueada aqui |

> **Atualização de 10/09/2026 — M1 e M7 foram destravadas.** As duas dependiam de
> arquivos que não estão no portal do OCA nem aparecem no HTML do dados.gov.br. O
> catálogo é uma SPA e sua API devolve 401 para cliente externo; **renderizando a página
> num navegador, a mesma API responde 200** e o campo `resources[].url` aponta para
> **`dados.ancine.gov.br`** — um domínio separado, que não é linkado de lugar nenhum.
> As três URLs estão testadas e registradas em `fontes.PARA_ENTREGA_2`. Licença de todas:
> **CC-BY**.

### ~~M1 — Fomento público recebido~~ ✅ **IMPLEMENTADA**

> Entrou na base em 11/09/2026. Cobre **67,1%** dos filmes com CPB (31,2% FSA, 54,1%
> leis de incentivo) e gerou seis atributos: `recebeu_fsa`, `recebeu_incentivo`,
> `contratos_fsa`, `projetos_incentivo` e a nominal `origem_do_fomento`.
>
> **O que se aprendeu com ela:** o gradiente de sucesso é forte (32,6% sem fomento
> contra 77,3% com os dois mecanismos), mas o grupo *só FSA* tem público mediano de
> 535 espectadores — abaixo do grupo sem fomento. E `recebeu_fsa` tem ρ = 0,511 com o
> ano, porque o FSA foi criado em 2006; o efeito sobrevive dentro da década, mas a
> variável exige `ano` no modelo (hipótese H14).

O registro original, mantido para quem quiser auditar a decisão:

**URLs testadas em 10/09/2026** (registradas em `fontes.ANCINE_FSA` e
`fontes.ANCINE_FOMENTO_INDIRETO`):

```
https://dados.ancine.gov.br/dados-abertos/obras-nao-pub-brasileiras-investimento-fsa.csv
https://dados.ancine.gov.br/dados-abertos/obras-nao-pub-brasileiras-fomento-indireto.csv
```

138 KB e 140 KB. Licença **CC-BY**. Esquema:

| arquivo | colunas |
|---|---|
| FSA | `TITULO_ORIGINAL` · `CPB` · `NUMERO_CONTRATO_FSA` |
| fomento indireto | `TITULO_ORIGINAL` · `CPB` · `NUMERO_SALIC` |

**A limitação que muda o plano: não há valor.** Os arquivos trazem o **número do
contrato**, não o montante. Ou seja, dá para derivar `recebeu_fsa` (binária),
`recebeu_incentivo` (binária) e `n_contratos` (contagem) — **não o orçamento**.
A hipótese original de "orçamento é o preditor ausente mais óbvio" continua sem fonte
pública; o que ganhamos é um proxy mais grosso.

**Em compensação, o risco de vazamento evaporou.** A versão anterior deste documento
alertava que o valor podia ser liberado ao longo da produção, e portanto posterior à
estreia. Como o que existe é aprovação de projeto — que precede a obra — a variável é
**legitimamente anterior à estreia**. Nenhuma checagem de data é necessária.

**Custo.** Baixo: dois CSVs pequenos. Dois cuidados: **agregue por CPB antes de juntar**
(uma obra aparece uma vez por contrato, e a junção crua duplicaria a listagem); e os 14
filmes com CPB `-` ficam de fora.

**O que isso habilita.** A pergunta de política pública que justifica o projeto:
*o dinheiro público está indo para filmes que encontram plateia?* Agora é respondível.

### M1b — Obras registradas na ANCINE *(descoberta lateral)*

`https://dados.ancine.gov.br/dados-abertos/obras-nao-pub-brasileiras-csv.zip` (2,7 MB,
CC-BY) é o registro completo de obras não publicitárias. Vale inspecionar: pode conter
atributos de produção que a listagem de lançados não traz — possivelmente **duração**,
o que resolveria M6 sem depender do Wikidata. Não foi aberto ainda.

### M2 — Histórico de sucesso, não só de contagem

**O que.** Hoje temos *quantos* filmes o diretor fez antes. Falta *como eles foram*:
público mediano dos filmes anteriores, taxa de sucesso anterior, maior público anterior
— sempre restrito a anos estritamente anteriores, como em D8.

**Por que.** Contagem mede experiência; média anterior mede **reputação**. A correlação
de `filmes_diretor_antes` com o público é só 0,29 — provavelmente porque contar filmes
mistura o diretor consagrado com o prolífico de circuito limitado.

**Cuidado.** É o atributo com maior risco de vazamento do trabalho. Qualquer descuido
na janela temporal e o alvo entra pela porta dos fundos. Exige teste explícito.

**Viabilidade.** 🟢 Imediata — a lógica de `_historico_anterior()` já existe e só
precisa agregar valor em vez de contar linhas.

### M3 — Validação temporal com janela deslizante

**O que.** Em vez de um corte único em 2018, várias origens (treino até 2014 → testa
2015; até 2015 → testa 2016; …) e a média dos resultados.

**Por que.** O corte único mede um ponto só, e esse ponto inclui a pandemia no teste.
Janela deslizante dá estimativa mais estável e mostra se o desempenho **degrada** com o
tempo — que é a pergunta prática.

**Viabilidade.** 🟢 `TimeSeriesSplit` do sklearn, com atenção a agrupar por ano.

### M4 — Consolidar entidade fragmentada

**O que.** `Downtown` (65), `Paris` (59) e `Downtown/Paris` (92) são a mesma operação em
arranjos distintos. Padronizar nome de distribuidora e produtora.

**Por que.** Reduz cardinalidade **e** melhora os atributos de histórico: hoje o
histórico de `Downtown/Paris` ignora os 124 filmes das duas separadas.

**Trade-off.** Consolidar é uma decisão de negócio, não de estatística. Agrupar duas
empresas que de fato operam separado introduz erro. Exige uma regra escrita e revisada
pelo grupo — por isso ficou fora da Entrega 1.

**Viabilidade.** 🟡 Precisa de critério humano, não de código.

### M5 — Regressão em `log(publico)`

**O que.** Alvo contínuo `log10(publico)` em paralelo à classificação.

**Por que.** A distribuição é aproximadamente log-normal (fig. 1). Em log, regressão é
apropriada — e a métrica em log tem leitura direta: erro de 0,5 é errar por um fator de
3.

**Ganho.** Elimina a arbitrariedade do corte na mediana e dá um trabalho com duas
tarefas, classificação e regressão.

**Viabilidade.** 🟢 A coluna já existe.

### M6 — Duração via Wikidata

**O que.** Propriedade P2047, casada por título e ano.

**Por que.** Duração era um atributo previsto na proposta original e a ANCINE não a
publica. Licença CC0 — sem qualquer fricção.

**Bloqueio.** `query.wikidata.org` **não resolve DNS** neste ambiente. Reabrir numa rede
que alcance o endpoint.

**Risco.** Casamento por título é impreciso: homônimos e variação de grafia. A cobertura
provavelmente cai muito para documentários de circuito limitado — e essa cobertura
seria **enviesada justamente pelo alvo** (filme popular tem verbete). Um atributo com
ausência correlacionada ao sucesso é armadilha, não melhoria. Precisaria de indicadora
de ausência e de teste.

**Viabilidade.** 🔴 Bloqueada aqui; 🟡 mesmo desbloqueada, exige cuidado.

### M7 — Data de estreia e salas na primeira semana 🟢 **destravada — a melhoria mais valiosa**

**URL testada em 10/09/2026** (registrada em `fontes.ANCINE_BILHETERIA_DIARIA`):

```
https://dados.ancine.gov.br/dados-abertos/bilheteria-diaria-obras-por-distribuidoras-csv.zip
```

486 MB comprimido, **152 CSV mensais** (latin-1, `;`), ~3,8 GB abertos. Licença
**CC-BY**. Uma linha por **obra × sala × dia**:

| campo | o que habilita |
|---|---|
| `DATA_EXIBICAO` | **data exata de estreia** = `min()` por CPB |
| `CPB_ROE` | chave de junção — a mesma da listagem |
| `REGISTRO_SALA` | **salas na 1ª semana** = distintos nos 7 primeiros dias |
| `PUBLICO` | público por sala por dia |
| `MUNICIPIO_SALA_COMPLEXO`, `UF_SALA_COMPLEXO` | dispersão geográfica do lançamento |

**Por que é a melhoria mais valiosa: ela resolve D6.** `max_salas` é vazamento porque é
o máximo atingido *durante* a carreira — distribuidora expande filme que vai bem.
**Salas na primeira semana é decidida antes de o desempenho ser conhecido.** Trocar uma
pela outra converte o atributo de mais forte poder preditivo (+0,108 de AUC em S1) de
vazamento em atributo legítimo. Nenhuma outra melhoria chega perto disso.

Junto vêm três atributos de estratégia de lançamento que hoje não existem: **mês de
estreia** (sazonalidade — férias, fim de ano), **número de UFs na estreia** e
**lançamento amplo × limitado**.

**A limitação: cobertura parcial.** A série começa em **2014-01** (vai até 2026-08).
Cobre **1.617 dos 2.626 filmes — 61,6%**, todos com CPB válido. Os filmes de 1995–2013
ficariam sem esses atributos.

Isso força uma decisão de escopo para a Entrega 2, e as duas saídas são defensáveis:

| opção | efeito |
|---|---|
| **restringir a base a 2014–2024** | 1.617 filmes com atributos ricos; perde-se metade do período e a comparação entre décadas — que é o achado central deste relatório |
| **manter 1995–2024 com indicadora de ausência** | preserva o achado, mas a ausência é 100% correlacionada com o período, o que é exatamente o tipo de armadilha que este trabalho documenta |

**Custo de implementação.** Médio, e é engenharia, não pesquisa: não carregue os 152
arquivos de uma vez. Processe mês a mês, filtre pelos CPBs da listagem, agregue e
descarte. O pico de memória fica em ~26 MB, não em 3,8 GB.

### M8 — Share do público do ano

**O que.** `publico / publico_total_do_ano` como alvo contínuo.

**Por que.** Normaliza pelo tamanho do mercado de forma mais fina que a mediana do ano.

**Limite.** Concentra quase tudo perto de zero — 90% dos filmes ficariam abaixo de
0,5% de share. Provavelmente precisaria de log de qualquer forma, e aí M5 já resolve.

**Viabilidade.** 🟢 Imediata, mas o ganho sobre M5 é pequeno.

---

## O que **não** vamos fazer, e por quê

Decidir não aplicar uma técnica exige a mesma evidência que decidir aplicá-la.

| técnica | por que não |
|---|---|
| **SMOTE / undersampling / `class_weight`** | as classes já estão em 50,0/49,7 por construção do alvo. Não há minoria a reforçar. Aplicar aqui seria cumprir tabela |
| **Remover *outlier* de público** | o IQR marca ~15% dos filmes, mas num regime de lei de potência a cauda **é o fenômeno**. Removê-la elimina justamente o que o modelo precisa reconhecer |
| **PCA** | com 7 numéricas úteis, das quais só um par é redundante, PCA custa interpretabilidade e não resolve o problema real, que é cardinalidade categórica |
| **Imputar `max_salas` pela mediana** | a ausência é MNAR: filmes sem `max_salas` têm público mediano muito menor. Imputar apagaria o sinal. Melhor uma indicadora de ausência (H5) |
| **Imputar os 22 filmes sem `publico`** | seriam rótulos inventados. Descartar, com registro |
