# 5.3 · Interações

> Dona: Ana Laura · Orçamento: parte das 4,0 páginas da §5

O enunciado define interação como a técnica que só se mostra benéfica na presença de outra. O
módulo de análise procura isso sem intervenção: para cada opção, compara-a com a sua referência
dentro de cada recorte da outra etapa e marca interação quando o veredito muda de recorte para
recorte. Dois pares foram marcados, e eles contam histórias diferentes.

## A redução depende da normalização

| PCA contra não reduzir, dentro de cada normalização | vitórias, empates, derrotas | ganho médio | veredito |
|---|---|---|---|
| com padronização | 0, 12, 0 | +0,000 | empate |
| com escala por intervalo | 0, 12, 0 | −0,003 | empate |
| com escala robusta | 0, 12, 0 | −0,003 | empate |
| sem normalização | 0, 0, 12 | **−0,065** | perde |

O PCA empata com não reduzir em todos os 36 contextos em que há normalização e perde em todos os
12 em que não há. O veredito depende inteiramente da etapa anterior, e a causa não é conjetura: a
grade registra quantas colunas chegam ao classificador, e nas combinações de PCA sem normalização
esse número é 2,0. O corte de 95% da variância sai em dois componentes. Faz sentido, porque sem
correção de escala a variância total da matriz é quase toda da contagem de filmes anteriores da
distribuidora e do ano, que são as colunas de maior amplitude; dois componentes bastam para
reproduzir essas duas colunas, e os demais atributos cabem nos 5% descartados. O classificador
recebe então um espaço de duas dimensões que sabe apenas o porte da distribuidora e o ano do
filme, e as seis piores combinações do ranking são exatamente essas.

A consequência é uma regra de ordem, não uma preferência de técnica: num pipeline com kNN, a
redução por componentes principais precisa vir depois de uma escala, e um pipeline que inverta
essa ordem não é apenas subótimo, é um erro de construção. A seleção por informação mútua não
apresenta esse comportamento, porque escolhe colunas por associação com o alvo, e associação não
depende da unidade em que a coluna está medida.

## A normalização rende mais com o encoding pelo alvo

| normalização contra não normalizar | com encoding pelo alvo | com one-hot |
|---|---|---|
| padronização | 15, 3, 0 · ganho +0,047 · vence | 7, 11, 0 · ganho +0,035 · empate |
| escala por intervalo | 17, 1, 0 · ganho +0,049 · vence | 6, 12, 0 · ganho +0,024 · empate |
| escala robusta | 15, 3, 0 · ganho +0,042 · vence | 8, 10, 0 · ganho +0,033 · empate |

As três normalizações vencem no espaço do encoding pelo alvo e apenas empatam no espaço do
one-hot, e é essa mudança de veredito que caracteriza a interação. Nenhuma delas chega a perder em
qualquer recorte, de modo que a recomendação de normalizar não muda; o que muda é quanto se ganha
com ela.

Esse resultado tem forma diferente da que prevíamos na §3.3. Esperávamos que a padronização
sofresse no one-hot por causa do fator 9,9 nas colunas binárias raras, e que a escala por
intervalo fosse a mais segura ali. O medido mostra que a escala por intervalo é justamente a que
mais perde ao sair do encoding pelo alvo para o one-hot, de 0,049 para 0,024 de ganho, enquanto a
padronização cai menos, de 0,047 para 0,035.

A explicação que propomos inverte o nosso próprio argumento. A escala por intervalo não mexe nas
colunas binárias, que continuam valendo zero ou um, mas comprime as colunas numéricas de cauda
longa para uma faixa estreita perto de zero, já que são governadas pelo máximo; as cerca de 84
colunas de indicadores passam então a ter amplitude efetiva maior que as numéricas, e são elas que
dominam a distância. A padronização iguala a dispersão de todas as colunas, inclusive as binárias,
e com isso impede que qualquer grupo domine. Quanto ao fator 9,9 que temíamos, a explicação
provável para a sua ausência está numa decisão da etapa anterior: o one-hot agrupa as categorias
com menos de dez filmes, de modo que as colunas raríssimas das quais o argumento dependia não
chegam a existir na matriz. Isso é hipótese compatível com o medido, e não efeito que tenhamos
isolado; isolá-lo exigiria rodar a grade sem esse agrupamento, o que fica como extensão na §7.

## O que não é interação

O par balanceamento e normalização não foi marcado: as duas técnicas empatam com não balancear em
todos os recortes, e o que muda é só a magnitude. Ainda assim há uma inversão de ordem que merece
nota, porque ilustra o mesmo mecanismo das outras duas interações. Sem normalização, a
subamostragem tem ganho médio de −0,013 contra não balancear; com padronização, de +0,007. A
subamostragem descarta cerca de metade dos filmes de cada treino, e com isso a densidade de
vizinhos cai. Num espaço mal escalado, em que a vizinhança já é decidida por duas colunas, perder
metade dos pontos agrava o problema; num espaço escalado, o ganho de equilíbrio no voto compensa a
perda de densidade.
