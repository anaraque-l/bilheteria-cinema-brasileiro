# Decisões e escopo

Cada decisão do projeto, com a alternativa que foi descartada e o motivo. Quem discordar
de uma delas encontra aqui o argumento a atacar.

---

## D1 — Nenhuma fonte com credencial

**Decisão.** Só fontes públicas que não exijam cadastro, chave de API ou aceite de
termos.

**Alternativa descartada.** TMDB e OMDb trariam duração, orçamento e elenco — atributos
valiosos que a ANCINE não publica.

**Por quê.** Reprodutibilidade. Um trabalho de quatro pessoas em que só uma tem a chave
é um trabalho que só uma pessoa roda. Vale mais um conjunto de atributos menor que
qualquer integrante e o professor reproduzem numa máquina limpa.

**Custo.** Ficamos sem duração e sem orçamento. Registrado em `01-fontes-de-dados.md`
e como melhoria M1/M6.

---

## D2 — Unidade de análise é o filme

**Decisão.** Uma linha = um filme brasileiro de longa-metragem lançado comercialmente.

**Alternativa descartada.** Painel filme × semana, que permitiria modelar a curva de
carreira.

**Por quê.** A ANCINE publica só o acumulado da carreira nesta listagem. O dado semanal
existe em outro conjunto (bilheteria diária) com granularidade e chave diferentes, e
juntá-lo seria um projeto próprio.

**Consequência importante.** Sem a curva semanal, **não dá para separar** as salas
decididas na estreia das salas ganhas por bom desempenho. É a raiz de D6.

---

## D3 — Classificação, não regressão

**Decisão.** Alvo binário.

**Alternativa descartada.** Regressão sobre o público em nível.

**Por quê.** A assimetria é 10,0 e a curtose 135,3; o máximo é 4.342 vezes a mediana.
Uma regressão nesse regime seria dominada por meia dúzia de blockbusters, e o erro
médio diria mais sobre eles do que sobre os 2.600 filmes restantes.

Regressão sobre `log(publico)` seria defensável e fica registrada como M5 — mas o
enunciado do tema pedia classificação, e a leitura "acima ou abaixo da mediana" é
diretamente interpretável por quem decide fomento.

---

## D4 — Dois alvos na base, `sucesso_no_ano` como principal

**Decisão.** `build_dataset.py` cria `sucesso_global` **e** `sucesso_no_ano`. A
recomendação do grupo para a Entrega 2 é usar **`sucesso_no_ano`** como principal, com
`sucesso_global` reportado como comparação.

**Alternativa descartada.** Só `sucesso_global`, que é a leitura literal do enunciado.

**Por quê.** A mediana global embute o ano. Medido:

| década | `sucesso_global` | `sucesso_no_ano` |
|---|---|---|
| 1990 | 0,856 | 0,490 |
| 2000 | 0,757 | 0,495 |
| 2010 | 0,502 | 0,498 |
| 2020 | 0,263 | 0,497 |

Um classificador com acesso a `ano` encontra esse atalho, atinge AUC alto e não aprende
nada sobre cinema.

**Custo medido (S2).** AUC cai de 0,832 para 0,770 — **−0,062**. Essa queda *é* a
medida do atalho. Perder 0,06 para não medir calendário é um bom negócio.

**Por que manter os dois na base.** Porque a comparação é um resultado do trabalho, não
um rascunho. Apagar `sucesso_global` esconderia a evidência que sustenta a decisão.

---

## D5 — `renda` é vazamento e sai

**Decisão.** `renda_corrente` e `renda_deflacionada_2024` nunca entram como atributo.

**Por quê.** Renda é público × preço do ingresso. ρ de Spearman com `publico` = **0,994**.
É a mesma variável em outra unidade.

**Custo medido (S1).** Incluí-la leva o AUC de 0,832 para **0,993** — o modelo
praticamente não erra porque está lendo a resposta.

**Por que fica na base.** Porque valida a consistência dos dados: renda ÷ público dá o
preço médio implícito do ingresso, e ele fica sempre entre R$ 1,39 e R$ 31,43, mediana
R$ 11,16. É uma verificação de domínio que só é possível com a coluna presente.

---

## D6 — `max_salas` é vazamento provável e sai do conjunto principal

**Decisão.** Excluir do conjunto principal; reportar em separado quanto valeria.

**Por quê.** O campo é o **máximo de salas atingido durante a carreira**, não o número
de salas na estreia. Distribuidoras expandem um filme que está indo bem e recolhem um
que não está — o número de salas é, em parte, **consequência** do sucesso.

**Este é o ponto mais discutível do trabalho, e é assim de propósito.** Parte de
`max_salas` é decisão comercial anterior à estreia, e essa parte seria um atributo
legítimo. Sem a data de estreia e sem a curva semanal (ver D2), **não é possível
separar as duas parcelas**.

**Custo medido (S1).** +0,108 de AUC — grande demais para um atributo de lançamento, e
consistente com a hipótese de que carrega o desempenho.

**Posição.** Diante de uma dúvida que os dados não resolvem, escolhemos a versão que não
pode inflar o resultado, e publicamos o número da outra. Quem discordar tem o valor
exato do que está em jogo.

---

## D7 — Validação temporal

**Decisão.** Recomendar partição temporal (treino até 2017, teste de 2018 em diante)
como protocolo principal da Entrega 2.

**Alternativa descartada.** *k-fold* aleatório estratificado.

**Por quê.** No *k-fold* aleatório, filmes de 2019 aparecem no treino e filmes de 2015
no teste: o modelo enxerga o futuro. O uso real é prever um filme que ainda não estreou.

**Custo medido (S3).** A validação aleatória é **+0,087 otimista** (0,832 contra 0,745).
Custa 0,09 de AUC e não custa nada de implementação.

---

## D8 — Atributos de histórico contam só o passado

**Decisão.** `filmes_diretor_antes`, `filmes_distribuidora_antes` e
`filmes_produtora_antes` contam filmes de anos **estritamente anteriores**.

**Por quê.** Contar o próprio filme e os do mesmo ano carregaria informação que só
existe depois do lançamento. Um diretor que estreou em 2024 tem histórico 0 em 2024,
não 1.

**Detalhe.** Filmes do mesmo ano não contam entre si — a base tem só o ano, não a data
exata, e na dúvida escolhemos o lado que não vaza.

---

## D9 — Parsing sim, correção não

**Decisão.** `build_dataset.py` extrai `uf_maj` de `uf_bruto`, mas **preserva** o campo
original e não imputa nada.

**Por quê.** Extrair `RJ` de `RJ/RJ` é ler o que já está escrito — parsing. Preencher
uma UF ausente com a moda seria inventar — imputação. A Entrega 1 faz o primeiro e não
faz o segundo.

**Fronteira.** Quando o parsing não encontra código de duas letras, o resultado é `NaN`,
nunca um palpite.

---

## O que ficou fora do escopo desta entrega

| item | por quê |
|---|---|
| Escolha do melhor modelo | é a Entrega 2 |
| Ajuste de hiperparâmetros | idem |
| Imputação, normalização, codificação, balanceamento | a Entrega 1 é exploratória |
| Remoção de *outlier* | e além disso a cauda é o fenômeno, não anomalia |
| Consolidar `Downtown`/`Paris`/`Downtown-Paris` | decisão de negócio, não de estatística; registrada como M4 |
