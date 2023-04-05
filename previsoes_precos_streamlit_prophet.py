# IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go

# Define as constantes do projeto
DATA_INICIO = '2017-01-01'
DATA_FIM = date.today().strftime('%Y-%m-%d')
N_DIAS_PADRAO = 30
PATH_ARQUIVO_ACOES = 'acoes.csv'

# Configura as credenciais do Plotly de forma segura
import plotly.io as pio
import plotly.express as px
pio.renderers.default = "plotly"
pio.templates.default = "plotly_white"
px.defaults.template = "plotly_white"

# Define uma função para pegar os dados das ações
def pegar_dados_acoes(path):
return pd.read_csv(path, delimiter=';')

# Define uma função para pegar os valores online das ações
@st.cache
def pegar_valores_online(sigla_acao):
df = yf.download(sigla_acao, DATA_INICIO, DATA_FIM)
df.reset_index(inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
return df

# Define a função principal do Streamlit
def main():
# Define o título da aplicação
st.title('Análise de Ações')

# Lê o arquivo CSV das ações
df_acoes = pegar_dados_acoes(PATH_ARQUIVO_ACOES)

# Exibe a barra lateral para selecionar a ação
st.sidebar.header('Escolha a ação')
acoes = df_acoes['snome'].tolist() # Converter para lista
nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação:', acoes)

# Filtra o dataframe para a ação escolhida
df_acao = df_acoes[df_acoes['snome'] == nome_acao_escolhida]
sigla_acao_escolhida = df_acao.iloc[0]['sigla_acao'] # Concatenação desnecessária removida

# Carrega os dados da ação selecionada
df_acao = pegar_valores_online(sigla_acao_escolhida)

# Exibe os valores das ações em um gráfico
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_acao['Date'], y=df_acao['Close'], name='Valor de fechamento'))
fig.add_trace(go.Scatter(x=df_acao['Date'], y=df_acao['Open'], name='Valor de abertura'))
fig.layout.update(title={'text': 'Valores das Ações', 'font': {'size': 28}, 'x': 0.5, 'xanchor': 'center'},
                  xaxis_title='Data', yaxis_title='Valor (USD)', font=dict(size=18))
st.plotly_chart(fig)

# Define o período de previsão
n_dias = st.sidebar.slider('Selecione o número de dias para a previsão', 1, 365, N_DIAS_PADRAO)

# Cria um novo dataframe com as datas da previsão
df_futuro = pd.DataFrame({'Date': pd.date_range(start=df_acao['Date'].iloc[-1], periods=n_dias + 1, freq='D

 # Cria um gráfico com o histórico de preços
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_acao['data'], y=df_acao['preco'], name='Histórico de preços'))
    fig1.update_layout(title=f'Histórico de preços da ação {sigla_acao_escolhida}',
                       xaxis_title='Data',
                       yaxis_title='Preço')
    st.plotly_chart(fig1, use_container_width=True)

    # Exibe a barra lateral para escolher a quantidade de dias para previsão
    st.sidebar.header('Escolha a quantidade de dias para a previsão')
    n_dias = st.sidebar.slider('Dias', 30, 365)

    # Faz a previsão de preços usando o Prophet
    df_predicao = df_acao[['data', 'preco']].rename(columns={'data': 'ds', 'preco': 'y'})
    modelo = Prophet()
    modelo.fit(df_predicao)
    futuro = modelo.make_future_dataframe(periods=n_dias)
    forecast = modelo.predict(futuro)

    # Cria um gráfico com a previsão de preços
    fig2 = plot_plotly(modelo, forecast)
    fig2.update_layout(title=f'Previsão de preços da ação {sigla_acao_escolhida}',
                       xaxis_title='Data',
                       yaxis_title='Preço')
    st.plotly_chart(fig2, use_container_width=True)

    # Cria um gráfico com os componentes da previsão
    fig3 = plot_components_plotly(modelo, forecast)
    st.plotly_chart(fig3, use_container_width=True)

if __name__ == '__main__':
    main()
