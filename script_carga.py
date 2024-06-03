import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import json

# Ler parâmetros
with open('parametros.json', 'r') as arquivo:
    parametros = json.load(arquivo)

# Carregar o CSV gerado
df = pd.read_csv('dados_tratados.csv')

# Parametros de onexão com banco 
db_usuario = parametros['db_usuario']
db_senha = parametros['db_senha']
db_host = parametros['db_host']
db_porta = parametros['db_porta']
db_nome = parametros['db_nome']

engine = create_engine(f'postgresql+psycopg2://{db_usuario}:{db_senha}@{db_host}:{db_porta}/{db_nome}')

# dicionários para localidade
localidades = pd.concat([df['Origem'], df['Destino']]).unique()
localidade_df = pd.DataFrame(localidades, columns=['NOME'])
localidade_df['ID'] = range(1, len(localidade_df) + 1)

# Inserir localidades na tabela Localidade
localidade_df.to_sql('LOCALIDADE', engine, if_exists='append', index=False)

# Criar um dicionário para mapear nome da localidade para o ID
localidade_dict = dict(zip(localidade_df['NOME'], localidade_df['ID']))

# Preparar dados para a tabela Clima e Transito
clima_data = []
transito_data = []

for index, row in df.iterrows():
    # Clima origem
    clima_data.append({
        'ID': len(clima_data) + 1,
        'LOCALIDADE_ID': localidade_dict[row['Origem']],
        'TEMPERATURA': row['Clima_Orig_Temp'],
        'SENSACAO_TERMICA': row['Clima_Orig_Sensacao'],
        'TEMPERATURA_MIN': row['Clima_Orig_Min'],
        'TEMPERATURA_MAX': row['Clima_Orig_Max'],
        'PRESSAO': row['Clima_Orig_Pressao'],
        'UMIDADE': row['Clima_Orig_Umidade'],
        'VELOCIDADE_VENTO': row['Clima_Orig_Vento'],
        'DESCRICAO': row['Clima_Orig_Desc'],
        'DATA_HORA': pd.to_datetime('now')  
    })
    
    # Clima destino
    clima_data.append({
        'ID': len(clima_data) + 1,
        'LOCALIDADE_ID': localidade_dict[row['Destino']],
        'TEMPERATURA': row['Clima_Dest_Temp'],
        'SENSACAO_TERMICA': row['Clima_Dest_Sensacao'],
        'TEMPERATURA_MIN': row['Clima_Dest_Min'],
        'TEMPERATURA_MAX': row['Clima_Dest_Max'],
        'PRESSAO': row['Clima_Dest_Pressao'],
        'UMIDADE': row['Clima_Dest_Umidade'],
        'VELOCIDADE_VENTO': row['Clima_Dest_Vento'],
        'DESCRICAO': row['Clima_Dest_Desc'],
        'DATA_HORA': pd.to_datetime('now') 
    })
    
    # Transito
    transito_data.append({
        'ID': len(transito_data) + 1,
        'ORIGEM_ID': localidade_dict[row['Origem']],
        'DESTINO_ID': localidade_dict[row['Destino']],
        'DISTANCIA': row['Transito_Dist'],
        'DURACAO': row['Transito_Duracao'],
        'INICIO': row['Transito_Inicio'],
        'FIM': row['Transito_Fim'],
        'PASSOS': row['Transito_Passos'],
        'DATA_HORA': pd.to_datetime('now') 
    })

# Converter para DataFrame e inseri
clima_df = pd.DataFrame(clima_data)
transito_df = pd.DataFrame(transito_data)

clima_df.to_sql('CLIMA', engine, if_exists='append', index=False)
transito_df.to_sql('TRANSITO', engine, if_exists='append', index=False)

print("Dados inseridos com sucesso no banco.")
