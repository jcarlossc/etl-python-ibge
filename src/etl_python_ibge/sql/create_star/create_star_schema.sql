CREATE DATABASE IF NOT EXISTS ibge_database
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ibge_database;

CREATE TABLE IF NOT EXISTS dim_indicador (

    id_indicador INT PRIMARY KEY,

    indicador VARCHAR(255) NOT NULL

);

CREATE TABLE IF NOT EXISTS dim_unidade (

    id_unidade VARCHAR(30) PRIMARY KEY,

    classe CHAR(1),

    multiplicador INT

);

CREATE TABLE IF NOT EXISTS dim_pais (

    id_pais INT AUTO_INCREMENT PRIMARY KEY,

    sigla_pais CHAR(2) NOT NULL,

    pais VARCHAR(100) NOT NULL,

    UNIQUE(sigla_pais)

);

CREATE TABLE IF NOT EXISTS dim_tempo (

    id_tempo INT PRIMARY KEY,

    ano INT NOT NULL,

    UNIQUE(ano)

);

CREATE TABLE IF NOT EXISTS fato_indicador (

    id_fato BIGINT AUTO_INCREMENT PRIMARY KEY,

    id_indicador INT NOT NULL,

    id_unidade VARCHAR(30) NOT NULL,

    id_pais INT NOT NULL,

    id_tempo INT NOT NULL,

    valor DECIMAL(18,4),

    CONSTRAINT fk_indicador
        FOREIGN KEY (id_indicador)
        REFERENCES dim_indicador(id_indicador),

    CONSTRAINT fk_unidade
        FOREIGN KEY (id_unidade)
        REFERENCES dim_unidade(id_unidade),

    CONSTRAINT fk_pais
        FOREIGN KEY (id_pais)
        REFERENCES dim_pais(id_pais),

    CONSTRAINT fk_tempo
        FOREIGN KEY (id_tempo)
        REFERENCES dim_tempo(id_tempo)

);

CREATE INDEX idx_fato_indicador
ON fato_indicador(id_indicador);

CREATE INDEX idx_fato_pais
ON fato_indicador(id_pais);

CREATE INDEX idx_fato_tempo
ON fato_indicador(id_tempo);

CREATE INDEX idx_fato_unidade
ON fato_indicador(id_unidade);
