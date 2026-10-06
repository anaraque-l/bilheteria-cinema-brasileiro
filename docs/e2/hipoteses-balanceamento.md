# Hipóteses do balanceamento — registradas antes da grade

Escritas antes de qualquer número da grade completa. Depois da rodada, cada uma
recebe o veredito ao lado, sem reescrever o texto original.

1. Balancear **sobe** revocação e F1 e **derruba** precisão e acurácia: o limiar
   efetivo de 4 em 7 vizinhos fica mais fácil de atingir.
2. A AUC muda **pouco**, provavelmente empate pela regra A.6: o balanceamento
   desloca quantos vizinhos são sucesso em quase todo bairro ao mesmo tempo, e a
   ordem dos filmes muda menos que o limiar. Se não empatar, é achado.
3. `smote` ganha de `subamostragem` em espaço contínuo, `alvo` ou `pca`; a
   diferença encolhe ou se inverte com `onehot` sem redução, onde o SMOTE cria
   dummies fracionárias.
4. Sem normalização, o SMOTE herda a distância distorcida e escolhe vizinhos pela
   coluna de maior amplitude: interação balanceamento × normalização.
5. Em P90, prevalência perto de 10%, o balanceamento pesa **mais** que em P75.

| hipótese | veredito | número |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
