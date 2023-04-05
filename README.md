Análise de Ações
Este é um projeto simples para análise de ações utilizando Python e as bibliotecas Streamlit, yfinance, pandas, fbprophet e Plotly.

O objetivo deste projeto é permitir que o usuário selecione uma ação e visualize seus valores históricos em um gráfico interativo, além de ter uma previsão de seus valores futuros utilizando o Prophet.

Como utilizar
Para utilizar esta aplicação, basta executar o script main.py. Em seguida, o navegador será aberto e a aplicação estará disponível para uso.

Na barra lateral esquerda, é possível selecionar a ação desejada a partir de uma lista de ações disponíveis. O gráfico de valores históricos será exibido na área central da página. Na parte inferior da página, é possível visualizar a previsão dos valores futuros da ação selecionada.

Pré-requisitos
Para utilizar esta aplicação, é necessário ter as seguintes bibliotecas instaladas:

streamlit
yfinance
pandas
fbprophet
plotly
Além disso, é necessário ter um arquivo acoes.csv contendo uma lista de ações com suas respectivas siglas. O arquivo deve ter a seguinte estrutura:
snome;sigla_acao
Empresa A;EMPA3
Empresa B;EMPB4
Empresa C;EMPC5
...
Desenvolvimento
Este projeto foi desenvolvido utilizando a linguagem de programação Python e as bibliotecas mencionadas acima. O código está organizado em funções para facilitar a leitura e manutenção.

As previsões de valores futuros foram feitas utilizando o Prophet, que é uma biblioteca para análise de séries temporais desenvolvida pelo Facebook. O Prophet é capaz de modelar tendências sazonais e feriados, além de permitir a inclusão de dados externos que possam influenciar no comportamento da série temporal.
