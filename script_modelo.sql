-- Criar tabelas Banco Local
\c Gold

-- Criação da tabela Localidade
CREATE TABLE Localidade (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

-- Criação da tabela Clima
CREATE TABLE Clima (
    id SERIAL PRIMARY KEY,
    localidade_id INTEGER REFERENCES Localidade(id),
    temperatura FLOAT,
    sensacao_termica FLOAT,
    temperatura_min FLOAT,
    temperatura_max FLOAT,
    pressao INTEGER,
    umidade INTEGER,
    velocidade_vento FLOAT,
    descricao VARCHAR(255),
    data_hora TIMESTAMP
);

-- Criação da tabela Transito
CREATE TABLE Transito (
    id SERIAL PRIMARY KEY,
    origem_id INTEGER REFERENCES Localidade(id),
    destino_id INTEGER REFERENCES Localidade(id),
    distancia VARCHAR(255),
    duracao VARCHAR(255),
    inicio VARCHAR(255),
    fim VARCHAR(255),
    passos TEXT,
    data_hora TIMESTAMP
);
