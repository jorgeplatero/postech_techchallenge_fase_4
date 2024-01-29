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

#layout do aplicativo
tab1, tab2 = st.tabs(['Forecast', 'Histórico'])

with tab1:
    #série prevista
    st.plotly_chart(fig_previsao, use_container_width=True)
    st.markdown('O gráfico acima mostra o forecast para as próximas 5 cotações do barril de petróleo Brent gerado com o modelo AutoARIMA implementado.')

with tab2:
    #série
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        '''
        <div style='text-align: justify;'>
            <p>
                O gráfico acima ilustra a série histórica do preço do barril de petróleo Brent desde os anos 2000. Verifica-se três grandes oscilações negativas na série, com inícios em 2008, 2014 e 2020.
            </p>
            <ul>
                <li>2008: a chamada terceira crise do petróleo está relacionada à especulação imobiliária nos Estados Unidos, o subprime, que provocou um aumento abusivo nos valores dos imóveis, fazendo com que as hipotecas acabassem não tendo a liquidez esperada, elevando juros e inflação. A consequência desse desastre econômico que colocou em xeque o capitalismo foi desemprego em massa, retração financeira internacional, principalmente na Europa. Com isso, houve o aumento da dívida pública externa por conta da necessidade de empréstimos junto ao Fundo Monetário Internacional (FMI). Esse cenário causou uma queda drástica no valor e nas demandas por commodities, como o petróleo. Ademais, no primeiro semestre desse ano, uma soma de fatores levou os preços: tensões geopolíticas, do Irã à Nigéria passando pelo Paquistão, o equilíbrio tenso entre uma oferta limitada e uma demanda puxada pelos países emergentes, a conscientização de que as reservas são limitadas e de acesso cada vez mais difícil e uma febre dos fundos de investimento por matérias-primas. Esses fundos usaram o petróleo de investimento contra a inflação da commodity. Temendo a alta dos preços, eles acabaram por alimentá-la, fazendo subir os preços do petróleo, mas depois da falência do banco americano Lehman Brothers em setembro, esta lógica se inverte. Temendo a deflação, os investidores abandonam o petróleo, porque precisam urgentemente de liquidez. Ao mesmo tempo, o petróleo caro do primeiro semestre derruba o consumo de combustível dos países industrializados, o que derrubou ainda mais a demanda.</li>
                <li>2014: é o pior tombo de preços desde 2008, causada pelo aumento de produção, em especial nas áreas de xisto dos EUA, uma demanda menor que a esperada na Europa e na Ásia e a recusa dos países da Organização dos Países Exportadores de Petróleo (OPEP) em reduzir seu teto de produção, independentemente do preço no mercado internacional. Com a superprodução, oriunda sobretudo do petróleo de xisto dos EUA, os membros da OPEP, visando não perder mercado, mantiveram suas produções afim de tornar insustentável a produção norte-americana. Alguns países sofrem particularmente com a redução dos preços do petróleo, sobretudo Venezuela, Rússia e Irã, em razão do grande peso das exportações da commodity em suas economias.</li>
                <li>2020: o setor petrolífero viveu um momento de instabilidade em razão da pandemia do novo coronavírus. Nesta perspectiva, as medidas de contenção do contágio do vírus, como o isolamento social, afetaram todo o mercado mundial em uma crise generalizada na demanda de produtos e consequente distorção de preços (SILVEIRA, 2020). No caso do petróleo, presente em diversos mercados, houve drástica redução do consumo - principalmente, o West Texas Intermediate (WTI). Essa diminuição causou uma distorção nos preços da commodity, que caíram excessivamente, gerando um desequilíbrio entre oferta e demanda. Essa redução expressiva do consumo atingiu os grandes produtores membros da OPEP, cujos membros vinham, desde 2016, discutindo a possibilidade de redução do volume de produção para alavancar os preços da commodity e drenar a alta quantidade em estoque. Diante do cenário gerado pela COVID-19, a necessidade da medida se tornou ainda mais evidente e a Arábia Saudita propôs um acordo com a Rússia que previa a redução na produção em 1,5 milhão de barris, visando estabilizar o preço do petróleo e manter a competitividade dos dois gigantes do mercado petrolífero. Entretanto, a Rússia, não concordou em reduzir sua produção, pelo receio em perder espaço no mercado competitivo para o petróleo WTI. Em resposta à Rússia, a Arábia Saudita decidiu rebaixar seus preços a níveis de 20 anos atrás e, ao mesmo tempo, aumentar sua produção para 12,3 milhões de barris por dia a partir de abril, dando início ao que é conhecido como “a guerra dos preços”.</li>
            </ul>
        </div>
        ''',
        unsafe_allow_html=True
    )