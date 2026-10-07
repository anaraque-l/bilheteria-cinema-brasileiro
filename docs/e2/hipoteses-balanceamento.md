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
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
