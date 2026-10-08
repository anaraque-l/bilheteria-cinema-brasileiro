# Anexo · Tabela das 144, ambiente, folds, atributos e tabelas de apoio

> Dona: Laura · Orçamento: não conta

## A · Tabela completa das 144 combinações

A tabela está em `reports/e2/anexo_144.md`, gerada por `python src/e2/anexo.py` a partir do
arquivo de resultados, e tem uma linha por combinação com o identificador, a opção adotada em cada
uma das cinco etapas, média e desvio das seis métricas, o número de colunas que chegaram ao
classificador, o tempo de execução e a coluna de erro. A mesma tabela em valores separados por
vírgula, no mesmo diretório, serve para importar no documento final sem digitação. A coluna de
erro está vazia nas 144 linhas: nenhuma combinação falhou.

<!-- tabela: reports/e2/anexo_144.md -->

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
