# 5.3 · Interações

> Dona: Ana Laura · Orçamento: parte das 4,0 páginas da §5

O enunciado define interação como a técnica que só se mostra benéfica na presença de outra. A
análise compara cada opção com a sua referência dentro de cada recorte da outra etapa e marca
interação quando o veredito muda de recorte para recorte. Na AUC, dois pares foram marcados.

![AUC média em cada cruzamento de duas etapas](../../../reports/figuras/e2/fig-al-interacoes.png)

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
