# 7 · Lições, limitações e conclusão

> Dona: Laura · Orçamento: 0,75 página

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
