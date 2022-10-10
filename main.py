# IMPORTANDO AS BIBLIOTECAS NECESSARIAS
import streamlit as st
import yfinance as yf
from datetime import date
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go


Data_Inicio = '2017-01-01'
Data_Fim = date.today().strftime('%Y-%m-%d')

# TRABALHANDO COM STREAMLIT
st.title('Analise de Ações')

# CRIANDO SIDEBAR (BARRA LATERAL)
st.sidebar.header('Escolha a ação')

# VARIAVEL PARA ESCOLHER QUANTOS DIAS SERÁ REALIZADA A PREVISÃO
# SLIDER É O COMPONENTE PARA DEFINIR QUANTOS DIAS A PREVISÃO
n_dias = st.slider('Quantidade de dias de previsão', 30, 365)


path = 'acoes.csv'
# FUNÇÃO BUSCA O NOME DA AÇÃO E O TICKET DA AÇÃO
# ESTA SENDO CONCATENADO O NOME DA AÇÃO COM O TICKET DA MESMA PARA SE A PESSOA SOUBER O NOME OU O TICKET FIQUE MAIS FACIL IDENTIFICAR A AÇÃO.
def pegar_dados_acoes(path):
    #path = 'https://drive.google.com/file/d/1EQp5u_v0IkdoROp8_FbD6hr_JtYxuA64/view?usp=sharing'
    return pd.read_csv(path, delimiter=';')

# CHAMANDO A FUNÇÃO
df = pegar_dados_acoes(path)

# BUSCANDO A AÇÃO
acao = df['snome']
nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação: ', acao)

# RODANDO O STREAMLIT
# Digitar no terminal:
# streamlit run main.py

df_acao = df[df['snome'] == nome_acao_escolhida]
acao_escolhida = df_acao.iloc[0]['sigla_acao']
acao_escolhida = acao_escolhida + '.SA'


# CRIANDO CACHE TORNANDO ASSIM MAIS RAPIDO O DASHBOARD
@st.cache
def pegar_valores_online(sigla_acao):
    df = yf.download(sigla_acao, Data_Inicio, Data_Fim)
    df.reset_index(inplace=True)
    return df

df_valores = pegar_valores_online(acao_escolhida)

# CRIANDO TABELA PARA MOSTRAR A TABELA DE VALORES ABAIXO
st.subheader('Tabela de valores - ' + nome_acao_escolhida)

# CRIANDO A TABELA COM OS ULTIMOS 10 VALORES
st.write(df_valores.tail(10))

# CRIANDO O GRAFICO
st.subheader('Gráfico de preços')
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_valores['Date'],
                         y=df_valores['Close'],
                         name='Preco Fechamento',
                         line_color='yellow'))
fig.add_trace(go.Scatter(x=df_valores['Date'],
                         y=df_valores['Open'],
                         name='Preco Abertura',
                         line_color='blue'))
st.plotly_chart(fig)

# REALIZANDO A PREVISÃO DE FECHAMENTO
df_treino = df_valores[['Date', 'Close']]

# RENOMEANDO AS COLUNAS PARA TRABALHAR COM PROPHET
df_treino = df_treino.rename(columns = {'Date' : 'ds', 'Close' : 'y' })

# CRIANDO UM MODELO
modelo = Prophet()
modelo.fit(df_treino)

# VARIAVEL QUE ARMAZENA AS PREVISOES
# ANOTAÇÃO IMPORTANTE A LETRA "B" EM FREQUENCIA REPRESENTA BUSSINES FREQUENCIE PARA QUE O MODELO NAO ERRE AS PREVISOES TENTANDO PREVER TAMBEM EM FINAIS DE SEMANA, POIS A BOVESPA NAO FUNCIONA EM FINAIS DE SEMANA.
futuro = modelo.make_future_dataframe(periods = n_dias, freq = 'B')
previsao = modelo.predict(futuro)

# YHAT É A PREVISAO
# YHAT.LOWER SERIA O MINIMO
# YHAT_UPPER O MAXIMO
st.subheader('Previsão')
st.write(previsao[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(n_dias))

# CRIANDO UM GRAFICO DAS PREVISOES
grafico1 = plot_plotly(modelo, previsao)
st.plotly_chart(grafico1)

grafico2 = plot_components_plotly(modelo, previsao)
st.plotly_chart(grafico2)
