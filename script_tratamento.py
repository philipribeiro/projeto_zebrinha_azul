import pandas as pd
import unidecode

# Carregar o CSV
df = pd.read_csv('dados_tabulados.csv')

# Adicionar coluna ID para indicar as linhas com problemas.
df.insert(0, 'ID', range(1, len(df) + 1))

# Função padroniza texto
def padronizar_texto(texto):
    if pd.isna(texto):
        return texto
    texto = str(texto).upper()
    texto = unidecode.unidecode(texto)
    return texto

# aplica função de patronização
df = df.applymap(padronizar_texto)

# Verificar duplicadas
duplicados = df[df.duplicated(subset=df.columns.difference(['ID']))]

# Criar DataFrame sem duplicados
df_sem_duplicados = df.drop_duplicates(subset=df.columns.difference(['ID']))

# Verificar ausentes e nulos
ausentes_nulos = df_sem_duplicados.isnull()

# Criar log
log_geral = []

# Registrar duplicados
for index, row in duplicados.iterrows():
    log_geral.append({'ID': row['ID'], 'Tipo': 'Duplicado', 'Linha': index, 'Coluna': ''})

# Registrar nulos
for index, row in ausentes_nulos.iterrows():
    for col, is_null in row.items():
        if is_null:
            log_geral.append({'ID': df_sem_duplicados.at[index, 'ID'], 'Tipo': 'Ausente/Nulo', 'Linha': index, 'Coluna': col})

# Verificar se se esta ok
if not log_geral:
    log_geral.append({'ID': '', 'Tipo': 'Nenhum erro encontrado', 'Linha': '', 'Coluna': ''})

# Salvar DataFrame atualizado sem duplicados
df_sem_duplicados.to_csv('dados_tratados.csv', index=False)

# Criar DataFrame para log
df_log_geral = pd.DataFrame(log_geral)

# Salvar log em CSV
df_log_geral.to_csv('log_erro.csv', index=False)

print("Tratamento de dados concluído. Arquivos 'dados_tratados.csv' e 'log_erro.csv' foram gerados.")
