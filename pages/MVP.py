import streamlit as st
import pandas as pd
import plotly.express as px


dados = pd.read_csv('dados/preco_brent.csv')
dados = dados[dados['data'] >= '2000-01-01']
forecast = pd.read_csv('dados/last_forecast.csv')

#tipando coluna de data
dados['data'] = pd.to_datetime(dados['data'])

#configurando template do plotly
template = 'ggplot2'

#figuras

#série
fig = px.line(
    data_frame=dados, 
    x=dados.data,
    y=dados.preco,
    template=template,
    color_discrete_sequence=['#ef5350'],
    labels={
        'preco':'Preço (US$)',
        'data':'Data'
    }
    
)
fig.update_layout(
    title='Preço do Petróleo Brent (US$)',
    xaxis_title='Período',
    yaxis_title='Preço (US$)'
)

#série prevista
fig_previsao = px.line(
    data_frame=forecast, 
    x=forecast.data,
    y=forecast.preco_previsto,
    template=template,
    color_discrete_sequence=['#ef5350'],
    labels={
        'preco_previsto':'Preço previsto (US$)',
        'data':'Data'
    }
)
fig_previsao.update_layout(
    title='Preço Previsto do Petróleo Brent (US$)',
    xaxis_title='Período',
    yaxis_title='Preço Previsto (US$)'
)

#visualização no streamlit

#logo fiap
left, cent, right = st.columns(3)
with right:
    st.image('img/fiap.png')


#título
st.title('Petróleo Brent')
st.image('img/oil_barrel.png', width=100)


#série
st.plotly_chart(fig, use_container_width=True)
st.markdown('O gráfico acima ilustra a série histórica do preço do barril de petróleo Brent desde os anos 2000.')

#série prevista
st.plotly_chart(fig_previsao, use_container_width=True)
st.markdown('O gráfico acima mostra o forecast para as próximas 5 cotações do barril de petróleo Brent gerado com o modelo AutoARIMA implementado.')