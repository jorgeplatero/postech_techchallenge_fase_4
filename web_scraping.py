import requests #realiza requisições em base de dados via HTTP 
from bs4 import BeautifulSoup #inspeciona e extrai conteúdo HTML, umas das principais ferramentas de web scraping do Python
import pandas as pd
import numpy as np
import psycopg2 as ps
import pandas.io.sql as sqlio
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA
import warnings


warnings.filterwarnings(action = 'ignore')

#função que insere e atualiza dados do IPEA no banco local
def update_database(data, table):
    tuples = list(set([tuple(x) for x in data.to_numpy()])) #cria lista de tuplas a partir dos dados do DataFrame
    columns = ','.join(list(data.columns)) #colunas do DataFrame separadas por vírgula
    insert = 'INSERT INTO %s(%s) VALUES(%%s,%%s)' % (table, columns) #SQL para inserção de dados
    cursor = conn.cursor() #cria cursor
    #insere dados
    try:
        #testa se base de dados local é a mesma do web scrapping, excluindo dados caso seja para não haver duplicação em jobs de teste
        sql = f'SELECT * FROM {table}'
        existing_database_data = sqlio.read_sql_query(sql, conn)
        print(f'Número de registros encontrados na tabela {table} local: {existing_database_data.shape[0]}')
        if existing_database_data.shape[0] == data.shape[0]:
            clear = 'TRUNCATE TABLE ipea.preco_brent'
            cursor.execute(clear)
            conn.commit() 
        else:
            pass
        cursor.executemany(insert, tuples)
        conn.commit()
        existing_database_data = sqlio.read_sql_query(sql, conn)
        print(f'Número de registros atualizados na tabela {table} local: {existing_database_data.shape[0]}')
    except (Exception, ps.DatabaseError) as error:
        print('Error: %s' % error)
        conn.rollback()


#função que atualiza o DataFrame com dados atualizados do IPEA
def update_dataframe(existing_data, new_data, table):
    #realiza busca da data mais recente do DataFrame atual
    last_date = existing_data['data'].max()
    #filtra registros mais recentes que o DataFrame atual no DataFrame atualizado
    new_rows = new_data[new_data['data'] > last_date]
    new_rows['data'] = new_rows['data'].astype(str).replace(' 00:00:00', '')

    #concatena os novos dados no DataFrame atual, se houver novos registros na requisição
    if not new_rows.empty:
        #realiza carga incremental no csv
        updated_data = pd.concat([new_rows, existing_data], ignore_index=True)
        #realiza carga incremental no banco
        print(f'Constam {new_rows.shape[0]} novos registros na base do IPEA')
        update_database(new_rows, table)
    else:
        #realiza carga no csv
        updated_data = existing_data
        #realiza carga no banco
        print(f'Não constam novos registros na base do IPEA ou não há registros na base local')
        update_database(updated_data, table)
    return updated_data

#função que insere dados do forecast no banco local
def update_database_forecast(forecast):
    table  = 'ipea.preco_previsto_brent'
    tuples = list(set([tuple(x) for x in forecast.to_numpy()])) #cria lista de tuplas a partir dos dados do DataFrame
    columns = ','.join(list(forecast.columns)) #colunas do DataFrame separadas por vírgula
    insert = 'INSERT INTO %s(%s) VALUES(%%s,%%s)' % (table, columns) #SQL para inserção de dados
    cursor = conn.cursor() #cria cursor
    #insere dados
    try:
        clear = 'TRUNCATE TABLE ipea.preco_previsto_brent'
        cursor.execute(clear)
        cursor.executemany(insert, tuples)
        conn.commit()
    except (Exception, ps.DatabaseError) as error:
        print('Error: %s' % error)
        conn.rollback()


#função para validação dos modelos
def wmape(y_true, y_pred):
    wmape = np.abs(y_true - y_pred).sum() / np.abs(y_true).sum()
    return wmape


#função que insere dados do forecast no banco local
def update_database_wmape(wmape):
    cursor = conn.cursor() #cria cursor
    #insere dados
    try:
        sql = f'INSERT INTO ipea.wmape(data, wmape) VALUES(cast(now() AS date), {wmape})'
        cursor.execute(sql)
        conn.commit()
    except (Exception, ps.DatabaseError) as error:
        print('Error: %s' % error)
        conn.rollback()

    
#conectando-se ao banco
conn = ps.connect(
    dbname = 'postech',
    user ='postgres',
    password = 'postgres',
    host = 'localhost',
    port = '5432'
)

#realizando web scraping

#url do IPEA para série de preços do petróleo brent
url_brent = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view'
#requisitando dados
res_brent = requests.get(url_brent)
#realiza teste da requisição e captura da série de preços do petróleo brent
if res_brent.status_code == 200:
    #cria objeto BeautifulSoup do HTML da página
    soup = BeautifulSoup(res_brent.text, 'html.parser')
    #obtem tabela no HTML
    table = soup.find('table', {'id': 'grd_DXMainTable'})
    #cria DataFrame a partir da tabela
    new_brent_data = pd.read_html(str(table), skiprows=0)[0]
    #seleciona dados úteis da tabela
    new_brent_data.columns = new_brent_data.iloc[0]
    new_brent_data = new_brent_data.drop(0)
    #tratando tipagem e renomeando colunas
    new_brent_data['Data'] = new_brent_data['Data'].str.replace('/','-')
    new_brent_data['Data'] = pd.to_datetime(new_brent_data['Data'], format='%d-%m-%Y')
    new_brent_data['Preço - petróleo bruto - Brent (FOB)'] = new_brent_data['Preço - petróleo bruto - Brent (FOB)'].astype(int)/100
    new_brent_data.rename(columns={'Data': 'data', 'Preço - petróleo bruto - Brent (FOB)': 'preco'}, inplace=True)
    #verifica existência de arquivo csv, carregando-o ou atribuindo o DataFrame do HTML
    brent_data_path = 'dados/preco_brent.csv'
    try:
        existing_brent_data = pd.read_csv(brent_data_path)
    except FileNotFoundError:
        existing_brent_data = new_brent_data
    #atualiza DataFrame
    brent_table = 'ipea.preco_brent' #especificando tabela no banco de dados
    updated_data = update_dataframe(existing_brent_data, new_brent_data, brent_table)
    #exporta dados atualizados em arquivo csv
    updated_data.to_csv(brent_data_path, index=False)
else:
    #exibe erro HTTP
    print('Falha ao acessar a página: Status Code', res_brent.status_code)

#url do IPEA para série de preços do dólar
url_dolar = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38590&module=M'
#requisitando dados
res_dolar = requests.get(url_dolar)
#realiza teste da requisição e captura da série de preços do dólar
if res_dolar.status_code == 200:
    #cria objeto BeautifulSoup do HTML da página
    soup = BeautifulSoup(res_dolar.text, 'html.parser')
    #obtem tabela no HTML
    table = soup.find('table', {'id': 'grd_DXMainTable'})
    #cria DataFrame a partir da tabela
    new_dolar_data = pd.read_html(str(table), skiprows=0, thousands='.', decimal=',')[0]
    #seleciona dados úteis da tabela
    new_dolar_data.columns = new_dolar_data.iloc[0]
    new_dolar_data = new_dolar_data.drop(0)
    #tratando tipagem e renomeando colunas
    new_dolar_data['Data'] = new_dolar_data['Data'].str.replace('/','-')
    new_dolar_data['Data'] = pd.to_datetime(new_dolar_data['Data'], format='%d-%m-%Y')
    new_dolar_data['Taxa de câmbio - R$ / US$ - comercial - compra - média'] = new_dolar_data['Taxa de câmbio - R$ / US$ - comercial - compra - média'].astype(float)
    new_dolar_data.rename(columns={'Data': 'data', 'Taxa de câmbio - R$ / US$ - comercial - compra - média': 'preco'}, inplace=True)
    new_dolar_data = new_dolar_data[new_dolar_data['data'] >= '1987-05-20']
    #verifica existência de arquivo csv, carregando-o ou atribuindo o DataFrame do HTML
    dolar_data_path = 'dados/preco_dolar.csv'
    try:
        existing_dolar_data = pd.read_csv(dolar_data_path)
    except FileNotFoundError:
        existing_dolar_data = new_dolar_data
    #atualiza DataFrame
    dolar_table = 'ipea.preco_dolar' #especificando tabela no banco de dados
    updated_dolar_data = update_dataframe(existing_dolar_data, new_dolar_data, dolar_table)
    #exporta dados atualizados em arquivo csv
    updated_dolar_data.to_csv(dolar_data_path, index=False)
else:
    #exibe erro HTTP
    print('Falha ao acessar a página: Status Code', res_dolar.status_code)

#obtendo wmape
    
try: #testa se há previsão ja realizada para calcular acurácia
    last_forecast = pd.read_csv('dados/last_forecast.csv')
    wmape = wmape(updated_data['preco'].head().values, last_forecast['preco_previsto'].values)
    update_database_wmape(wmape)
except FileNotFoundError:
    print('Não há dados suficientes para calcular erro do modelo')

#realizando previsões

#preparando dados para a biblioteca statsforecast
df_statsforecast = updated_data[['data', 'preco']].rename(columns={'data': 'ds', 'preco': 'y'})
df_statsforecast['unique_id'] = 'Preco'
df_statsforecast.dropna(inplace=True)

#definindo dados de treino
treino = df_statsforecast.loc[(df_statsforecast['ds'] >= '2000-01-01')]
h = 5

#implementando modelo
modelo = StatsForecast(models=[AutoARIMA(season_length=5)], freq='B', n_jobs=-1)
modelo.fit(treino)
forecast = modelo.predict(h=5, level=[90])
forecast = forecast[['ds', 'AutoARIMA']].reset_index(drop=True).rename(columns={'ds': 'data', 'AutoARIMA': 'preco_previsto'})
forecast['preco_previsto'] = [int(n * 100) / 100 for n in forecast['preco_previsto']]
forecast = forecast.sort_values('data', ascending=False)
#salvando dados previstos
last_forecast_path = 'dados/last_forecast.csv'
forecast.to_csv(last_forecast_path, index=False)

#atualizando tabela de forecast no banco local
update_database_forecast(forecast)

#encerra conexão com o banco
conn.close() 