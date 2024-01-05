import streamlit as st


st.image('img/fiap.png')
st.title('O projeto')
st.markdown(
    '''
        <div style="text-align: justify;">
            <p>
                Os dados utilizados neste projeto estão disponibilizados em uma tabela no site do IPEA (Instituto de Pesquisa Econômica Aplicada) e serão importados por meio da biblioteca pandas do python. A tabela disponibiliza os preços por barril do petróleo bruto tipo Brent, não incluindo despesa de frete e seguro. Os dados serão então exportados para um arquivo em formato csv, a partir do qual serão trabalhados, evitando problemas de indisponibilidade na fonte.
            </p>
            <p>
                Texto.
            </p>
        </div>
    ''',
    unsafe_allow_html=True
)