DROP DATABASE IF EXISTS ibge_database;

CREATE DATABASE ibge_database
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ibge_database;

-- ==========================
-- DIM_INDICADOR
-- ==========================
CREATE TABLE dim_indicador (

    id_indicador_sk INT PRIMARY KEY,

    id_indicador INT NOT NULL,

    indicador VARCHAR(255) NOT NULL,

    UNIQUE(id_indicador)

);

-- ==========================
-- DIM_UNIDADE
-- ==========================
CREATE TABLE dim_unidade (

    id_unidade_sk INT PRIMARY KEY,

    unidade VARCHAR(50) NOT NULL,

    classe CHAR(1),

    multiplicador INT

);

-- ==========================
-- DIM_PAIS
-- ==========================
CREATE TABLE dim_pais (

    id_pais_sk INT PRIMARY KEY,

    sigla_pais CHAR(2) NOT NULL,

    pais VARCHAR(100) NOT NULL,

    UNIQUE(sigla_pais)

);

-- ==========================
-- DIM_TEMPO
-- ==========================
CREATE TABLE dim_tempo (

    id_tempo INT PRIMARY KEY,

    ano INT NOT NULL,

    UNIQUE(ano)

);

-- ==========================
-- FATO_INDICADOR
-- ==========================
CREATE TABLE fato_indicador (

    id_fato BIGINT PRIMARY KEY,

    id_indicador_sk INT NOT NULL,

    id_unidade_sk INT NOT NULL,

    id_pais_sk INT NOT NULL,

    id_tempo INT NOT NULL,

    valor DECIMAL(18,4),

    CONSTRAINT fk_indicador
        FOREIGN KEY (id_indicador_sk)
        REFERENCES dim_indicador(id_indicador_sk),

    CONSTRAINT fk_unidade
        FOREIGN KEY (id_unidade_sk)
        REFERENCES dim_unidade(id_unidade_sk),

    CONSTRAINT fk_pais
        FOREIGN KEY (id_pais_sk)
        REFERENCES dim_pais(id_pais_sk),

    CONSTRAINT fk_tempo
        FOREIGN KEY (id_tempo)
        REFERENCES dim_tempo(id_tempo)

);

-- ==========================
-- ÍNDICES
-- ==========================
CREATE INDEX idx_fato_indicador
ON fato_indicador(id_indicador_sk);

CREATE INDEX idx_fato_unidade
ON fato_indicador(id_unidade_sk);

CREATE INDEX idx_fato_pais
ON fato_indicador(id_pais_sk);

CREATE INDEX idx_fato_tempo
ON fato_indicador(id_tempo);
