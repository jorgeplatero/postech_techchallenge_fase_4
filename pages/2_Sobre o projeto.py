import streamlit as st


left, cent, right = st.columns(3)
with right:
    st.image('img/fiap.png')
st.title('Sobre o projeto')
st.image('img/oil_barrel.png', width=100)
st.markdown(
    '''
        <div style="text-align: justify;">
            <p>
                Para o desenvolvimento deste projeto, optou por seguir a metodologia CRISP-DM (CRoss Industry Standard Process for Data Mining), largamente utilizada em projetos de dados. A CRISP-DM é composta por 6 etapas, são elas:
                <ul>
                    <li>Análise do negócio (business understanding): essa etapa dedica-se ao entendimento do negócio, isto é, sua produto/serviço, público alvo e quais são as estratégias do setor;</li>
                    <li>Análise dos dados (data understanding): uma vez realizada a etapa anterior, inicia-se o entendimento dos dados, que compreende a seleção daqueles que são uteis à resolução da problemática requerida, bem como seu estado (fontes, formatos, etc)</li>
                    <li>Preparação dos dados (data preparation): essa etapa dedica-se ao pré-processamento dos dados, em acordo com o que é solicitado pelas soluções que se pretende implementar;</li>
                    <li>Modelagem (modeling): a modelagem é a etapa na qual se extrai informações de valor sobre os dados, possibilitando a geração de insights úteis ao negócio, capazes de solucionar a problemática;</li>
                    <li>Avaliação (evaluation): momento de avaliação do desempenho do modelo aplicado, isto é, verifica-se se esse respondeu as questões levantadas satisfatoriamente; e</li>
                    <li>Implementação (deployment): por fim, a implementação é a etapa em que se disponibiliza os resultados e insights obtidos as partes interessadas, comumente por meio de uma ferramenta de data viz ou relatório.</li>
                </ul>
        </div>
    ''',
    unsafe_allow_html=True
)
left, cent, right = st.columns(3)
with cent:
    st.image('img/CRISP_DM.png', caption='Fluxo da metodologia CRISP-DM')
st.markdown(
    '''
        <div style="text-align: justify;">
            <p>
                Os dados utilizados neste projeto estão disponibilizados em tabelas no site do IPEA (Instituto de Pesquisa Econômica Aplicada) e serão importados por meio da biblioteca Pandas do Python. A <b><a style='text-decoration:none', href='http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view'>tabela</a></b> fato disponibiliza os preços por barril do petróleo bruto tipo Brent, negociados em dias úteis, não incluindo despesa de frete e seguro. Também obtém-se uma <b><a style='text-decoration:none', href='http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38590&module=M'>tabela</a></b> com a série histórica do preço do dólar para o mesmo período. 
            </p>
            <p>
                Após as etapas de análise do negócio, análise dos dados e preparação de dados, deu-se início à modelagem, utilizando as bibliotecas Prophet e Statsforecast. O modelo melhor avaliado foi o AutoARIMA, disponível no Statsforecast, motivo pelo qual o mesmo foi selecionado para a etapa de implementação do projeto.
            </p>
            <p>
                A implementação produziu duas aplicações distintas: o presente MVP, com dashboard que disponibiliza a série histórica e forecast semanal e um <b><a style='text-decoration:none', href='https://app.powerbi.com/view?r=eyJrIjoiYjcxNGZlNmYtMDI4OS00NmJiLTk3Y2EtMWMyZWEyZWJmMTA4IiwidCI6IjExZGJiZmUyLTg5YjgtNDU0OS1iZTEwLWNlYzM2NGU1OTU1MSIsImMiOjR9'>dashboard</a></b> interativo desenvolvido no Power BI. Os dados consumidos pelas aplicações são tratados, processados e disponibilizados em um script web scraping Python que consulta, semanalmente, a série disponibilizada no endereço do IPEA supracitado. O dashboard desenvovido no Power BI consome um banco de dados PostgreSQL carregados pelo script referido, que também exporta arquivos CSV consultados pelo MVP Streamlit no repositório GitHub.
            </p>
        </div>
    ''',
    unsafe_allow_html=True
)
st.image('img/arquitetura.png', caption='Arquitetura do projeto')