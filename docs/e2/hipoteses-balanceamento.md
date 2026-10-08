# Hipóteses do balanceamento

Estas hipóteses foram escritas antes de rodarmos a grade completa. Depois da rodada, cada
uma recebe um veredito na tabela do fim, e o texto original não é alterado. Assim fica
registrado o que esperávamos e o que de fato aconteceu.

**1. Balancear aumenta a revocação e o F1 e diminui a precisão e a acurácia.**
O kNN prevê sucesso quando pelo menos 4 dos 7 vizinhos são sucesso. Com mais sucessos no
treino, esse número fica mais fácil de alcançar. O modelo passa a apontar mais filmes como
sucesso: acerta mais sucessos, mas também erra mais fracassos.

**2. A AUC muda pouco, e a diferença deve ficar dentro do empate.**
O balanceamento aumenta o número de vizinhos de sucesso em quase todos os filmes ao mesmo
tempo. A ordem dos filmes, do mais provável ao menos provável, quase não muda, e a AUC mede
justamente essa ordem. Se a AUC mudar além do empate, isso precisa ser explicado.

**3. O SMOTE funciona melhor que a subamostragem quando os atributos são contínuos.**
O SMOTE cria filmes novos no meio do caminho entre dois sucessos. Isso faz sentido com
números contínuos, como no encoding pelo alvo ou depois do PCA. Com one-hot sem redução,
ele cria filmes que não existem, como "metade de uma distribuidora e metade de outra".
Nesse caso, a vantagem do SMOTE deve diminuir ou desaparecer.

**4. Sem normalização, o SMOTE escolhe vizinhos ruins.**
Sem normalização, a coluna com os maiores números domina a distância. O SMOTE usa essa
mesma distância para achar sucessos parecidos, então herda a distorção. Esperamos ver
balanceamento e normalização interagindo.

**5. Com o corte em P90, o balanceamento faz mais diferença do que em P75.**
Em P90 só cerca de 10% dos filmes são sucesso. Quanto mais rara a classe, mais difícil
chegar a 4 votos de 7, e mais o balanceamento deve ajudar.

| hipótese | veredito | número |
|---|---|---|
| 1 | confirmada, com F1 parcial | revocação +0,19, precisão −0,15 e acurácia −0,05 nos 48 contextos, sem exceção; em F1 a subamostragem vence 15 e empata 33, o SMOTE vence 9 e perde 7 |
| 2 | confirmada | AUC: subamostragem com 44 empates e 4 derrotas em 48, todas as derrotas sem normalização; SMOTE com 1 vitória, 41 empates e 6 derrotas |
| 3 | refutada | o SMOTE não supera a subamostragem em nenhum dos dois encodings; em F1 contra não balancear, com o encoding pelo alvo, SMOTE 5 vitórias e 4 derrotas, subamostragem 6 e 0; com one-hot, 4 e 3 contra 9 e 0 |
| 4 | refutada no sentido | há interação no F1, mas ao contrário: sem normalização o SMOTE vence em 9 de 12 contextos, ganho +0,055; com padronização perde em 5 de 12, ganho −0,018 |
| 5 | indício a favor, sem teste pareado | revocação média das combinações sem balanceamento cai de 0,50 em P75 para 0,24 em P90, e a das balanceadas fica entre 0,72 e 0,79 nos dois cortes; as doze da robustez não formam pares com e sem balanceamento |
