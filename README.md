# Rosmann Predict Sales

## Contextualização. 

A Rossmann é uma das maiores redes de drograria da europa, e seu CEO deseja realizar uma reforma em suas lojas, com o objetivo de melhorar a experiencia com o cliente. 

Para alcançar este objetivo, é necessário definir quanto de orçamento poderá ser reservado para a reforma de cada loja. Com isso em mente, ter a estimativa do valor a ser vendido por cada uma dessas lojas é 
fundamental para definir este orçamneto de maneira mais assertiva, por isso, fora solicitado uma previsão, do quanto cada loja irá obter de faturamento nas próximas 6 semanas. 

## Etapas do projeto. 
O projeto foi desenvolvido com a metodologia Crisp-DS, uma metodologia cíclica, que busca iterar sobre 9 ciclos, cada etapa do projeto, sendo elas: 
   
   1 . [Questão de negócio](1-questão-de-negócio)
   2 . Entendimento do negócio]
   3 . Coleta dos dados
   4 . Limpeza dos dados 
   5 . EDA - Analise exploratória dos dados
   6 . Modelagem dos dados 
   7 . Modelos de Machine Learning
   8 . Avaliação e tunagem dos modelos de Machine Learning 
   9 . Modelo em produção 


 ### 1 Questão de negócio
  - O projeto começa com uma indagação, do tipo quanto vamos vender nas próximas 6 semanas?

 ### 2 - Entendimento do Negócio. 
   - Toda questão de negócio surge a partir de uma dor, que em nosso caso é: como definir
da maneira mais assertiva possível o budget para as reformas. Entender o problema real de negócio, ajuda-nos a saber se a questão de negócio, é realmente a mais adequada para lidar com aquela dor.

### 3 - Coleta dos dados. 
  - Aqui que, efetivamente inicia-se a execução do projeto, para o nosso projeto, esta etapa foi realizada extraindo dos dados da base:

### 4 - Limpeza dos dados.
  - Nesta etapa buscamos entender a qualidade dos nossos dados respondendo algumas perguntas do tipo:
   -  Quanto registros temos registros temos?
   -  Quais estão nulos? Por que?
    -  É possível preencher esses registros nulos? Se sim, como?
   - Os dados estão realmente assertivos? Fazem sentido com a realidade/contexto do negócio (avaliação de coêrencia)
     - Se os dados não estão assertivos, por que? Há erros no processo de lançamento das informações? Ou erros no processo de coleta dos dados?

   - **A resposta de cada uma dessas perguntas, geralmente devem vir com uma proposta de solução para os problemas encontratos.**  

   **Resultados**
  Em nosso projeto, não fora possível avaliar a coerencia dos dados, uma vez que tratam-se de dados do kaggle, no entanto, foram identificados valores nulos, e utlizadas premissas de negócio para seu preenchimento, aqui também poderiam ser algumas técnicas estátisticas.   

### 5 - Exploração dos dados: 
  - Aqui que começa a real geração de valor para o negócio, com o entendimento dos fenomeno (vendas das lojas) e os fatores que o influenciam. Fora forumado um conjunto de hipóteses, cujo os princiapsi
**insights** gerados foram:
- ...

### 6 - Modelagem dos dados. 
  - É neste momento em que começamos realmente a pensar nos modelos de Machine Learning, aqui são podem ser construidas novas features (feature enginnering) assim transformações em nossos dados, nas quais podemos pensar em dois tipos de subdivisoes para nossas transformações:
  
  - **Orientadas ao fenomeno modelado (problema de negócio):**
   -  As transformações aplicadas nas variaveis categoricas podem possuir como orientação inicial a busca por realizar transformações que sejam capazes de obter a menor perda possível de informação,
     por exemplo, ao transformarmos os dias da semana em valores numeros de 1 a 7, perdemos a informação ciclica, de que o dia 7 (sabado) esta proximo ao dia 1 (domingo).
  
  - **Orientadas aos modelos de machine learning:**.
   -Modelos de machine Learning são construídos com base em certas premissas, isso quer dizer, em certas características que os dados devem possuir, para que eles funcionem bem, exemplo:
     - Modelos baseados em distância, como KNN, KMeans são modelos extremamente sensível as escalas dos dados de entrada, dados com escalas diferentes, enviesam o modelo a aprender mais de uma ou outra caracteristica, sendo necessário técnicas de normalização.
     - A maiordos modelos de ML como KNN, RandomForest, Redes Neurais por exemplo, funcionam melhor quando os dados da variável objetivo apresentam uma distribuição normal.

     Neste projeto, fora aplicado trnasformações de one hot encoding, transformações ciclcias de seno e cosseno e transformação logratimica na variavel alvo (sales).

### 7 - Algoritmos de Machine Learning 

### 8 - Avaliação do Algoritmo 

### 9 - Deploy do Modelo

