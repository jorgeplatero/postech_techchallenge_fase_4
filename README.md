# Dataviz com Modelo Preditivo de Preços do Petróleo Brent

![logo do projeto](https://github.com/jorgeplatero/postech_techchallenge_fase_4/assets/99737345/2aa76bfc-1d97-4916-8de5-cc17b40d64ed)

## Descrição do Projeto

Este projeto tem por objetivo o desenvolvimento de um dashboard interativo capaz de gerar insights relevantes para tomada de decisão no que diz respeito ao negócio do petróleo brent, o que inclui a implementação de um modelo de Machine Learning que traga o forecasting dos preços.
  
Os dados utilizados neste projeto estão disponibilizados em tabelas no site do IPEA (Instituto de Pesquisa Econômica Aplicada) e serão importados por meio da biblioteca Pandas do Python. A tabela fato disponibiliza os preços por barril do petróleo bruto tipo Brent, negociados em dias úteis, não incluindo despesa de frete e seguro. Também obteve-se uma tabela com a série histórica do preço do dólar para o mesmo período.  

A etapa de modelagem utiliza-se das bibliotecas Prophet e Statsforecast. O modelo melhor avaliado foi o AutoARIMA, disponível no Statsforecast, motivo pelo qual o mesmo foi selecionado para a etapa de implementação do projeto.

A implementação produziu duas aplicações distintas: um MVP, com dashboard que disponibiliza a série histórica e forecast semanal e um dashboard interativo desenvolvido no Power BI que conta com outras métricas para análise e tomada de decisão. Os dados consumidos pelas aplicações são tratados, processados e disponibilizados em um script web scraping Python que consulta, semanalmente, a série disponibilizada no endereço do IPEA supracitado. O dashboard desenvovido no Power BI consome um banco de dados PostgreSQL carregado pelo script referido, que também exporta arquivos CSV consultados pelo MVP Streamlit no repositório GitHub.

**Arquitetura do projeto**

![imagem da arquitetura do prejeto](https://github.com/jorgeplatero/postech_techchallenge_fase_4/assets/99737345/63949593-e1bf-4129-89c2-45d8bc4c27e2)

## Tecnologias Utilizadas

- Python
- Streamlit
- PostgreSQL
- Power BI

## Fontes de Dados

Série de preços do petróleo brent: http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view

Série de preços do dólar: http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38590&module=M

## Links para as Aplicações

Dashboard Power BI: https://app.powerbi.com/view?r=eyJrIjoiYjcxNGZlNmYtMDI4OS00NmJiLTk3Y2EtMWMyZWEyZWJmMTA4IiwidCI6IjExZGJiZmUyLTg5YjgtNDU0OS1iZTEwLWNlYzM2NGU1OTU1MSIsImMiOjR9

MVP Streamlit: https://postechtechchallengefase4-ceqwpwmwrl4eucsnvjjsjm.streamlit.app/

## Colaboradores

https://github.com/mateus-albuquerque

https://github.com/adriellytsilva
