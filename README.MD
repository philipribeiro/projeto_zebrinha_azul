
# README

## Descrição

Este projeto consiste em scripts Python para extrair, tratar e armazenar dados de clima e trânsito em um banco de dados PostgreSQL. O projeto inclui:

1. **Extração de dados**: Coleta informações de APIs de clima e trânsito.
2. **Tratamento de dados**: Padroniza, remove duplicatas e detecta valores ausentes.
3. **Armazenamento de dados**: Insere os dados tratados em um banco de dados PostgreSQL.
4. **Geração de logs**: Cria logs para duplicatas e valores ausentes.

## Requisitos

Instale as seguintes bibliotecas antes de executar os scripts:


pip install pandas unidecode sqlalchemy psycopg2-binary


executar na sequencia

script_extracao.py >>> script_tratamento.py >>> script_carga.py

## Estrutura do Projeto

- `parametros.json`: Arquivo JSON contendo parâmetros e credenciais de conexão ao banco de dados.

## Scripts

### 1. `script_extracao.py`

- **Função**: Extrai dados de APIs de clima e trânsito e os salva em um arquivo CSV (`dados_tabulados.csv`).

### 2. `script_tratamento.py`

- **Função**: Trata e padroniza os dados extraídos, remove duplicatas e detecta valores ausentes/nulos. Salva os dados tratados em um arquivo CSV (`dados_tabulados_tratados.csv`) e cria um arquivo de log (`log_tratamento.csv`).

### 3. `script_carga.py`

- **Função**: Carrega os dados tratados do CSV para um banco de dados PostgreSQL, garantindo que os IDs sejam únicos e sequenciais.

### 4. `script_modelo.sql`

- **Função**: Criação do esquema de banco de dados PostgreSQL, incluindo a definição de tabelas, relacionamentos, PK e FK.

## Script Geram

- `dados_tabulados.csv`: Arquivo CSV com dados extraídos e tratados.
- `dados_tabulados_tratados.csv`: Arquivo CSV com dados tratados, sem duplicatas.
- `log_tratamento.csv`: Arquivo CSV de log com informações sobre duplicatas e valores ausentes/nulos.
