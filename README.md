<div align="center">

<img src="https://github.com/jcarlossc/etl-python-ibge/blob/main/images/etl_python_ibge_01.jpg">

### Pipeline ETL

Pipeline ETL desenvolvido em Python para coleta, transformação, modelagem e carga de dados públicos do IBGE em um banco de dados dimensional utilizando Star Schema.

O projeto foi desenvolvido com foco em boas práticas de Engenharia de Dados, incluindo separação de responsabilidades, configuração externa, logging, retry,
tratamento de exceções, testes automatizados, validação estática, linting e integração contínua.

<img src="https://img.shields.io/badge/Python-276DC3?style=for-the-badge&logo=r&logoColor=white" />
<img src="https://img.shields.io/badge/STATUS-EM%20DESENVOLVIMENTO-success?style=for-the-badge" />
<img src="https://img.shields.io/badge/LICENSE-MIT-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/TESTS-pytest-orange?style=for-the-badge" />

![Poetry](https://img.shields.io/badge/Poetry-1.8+-60A5FA?style=for-the-badge&logo=poetry)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas)
![Ruff](https://img.shields.io/badge/Ruff-D7FF64?style=for-the-badge)
![MyPy](https://img.shields.io/badge/MyPy-2A6DB2?style=for-the-badge)
![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF?style=for-the-badge&logo=github-actions)
![Release Please](https://img.shields.io/badge/Release-Please-4285F4?style=for-the-badge)
![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge&logo=pre-commit)
![Typed](https://img.shields.io/badge/Typing-MyPy-blue?style=for-the-badge)
![Code Style](https://img.shields.io/badge/code%20style-ruff-black?style=for-the-badge)
</div>

---

## 📌 Imagens do Projeto
<table>
  <tr>
    <td>
      <figure>
        <img src="https://github.com/jcarlossc/etl-python-ibge/blob/main/images/fluxo.JPG" alt="Imagem Testes" width="250" target="_blank"/>
        <figcaption>
          <p><b>Diagrama</b></p>
        </figcaption>
      <figure>
    </td>
    <td>
      <figure>
        <img src="https://github.com/jcarlossc/etl-python-ibge/blob/main/images/cobertura_testes.JPG" alt="Imagem Testes" width="250" target="_blank"/>
        <figcaption>
          <p><b>Cobertura de Testes</b></p>
        </figcaption>
      <figure>
  </td>
  <td>
    <figure>
      <img src="https://github.com/jcarlossc/etl-python-ibge/blob/main/images/precommit.JPG" alt="Imagem Testes" width="250" target="_blank" />
      <figcaption>
          <p><b>Pre-commit</b></p>
      </figcaption>
    <figure>
  </td>
    <td>
      <figure>
        <img src="https://github.com/jcarlossc/etl-python-ibge/blob/main/images/pytest.JPG" alt="Imagem Relatório" width="250" target="_blank"/>
        <figcaption>
          <p><b>Testes Unitários</b></p>
        </figcaption>
      <figure>
    </td>
    <td>
      <figure>
        <img src="https://github.com/jcarlossc/etl-python-ibge/blob/main/images/rich.jpg" alt="Imagem Relatório" width="250" target="_blank"/>
        <figcaption>
          <p><b>Monitoramento - Rich</b></p>
        </figcaption>
      <figure>
    </td>
    <td>
      <figure>
        <img src="https://github.com/jcarlossc/etl-python-ibge/blob/main/images/star_schema.png" alt="Imagem Relatório" width="250" target="_blank"/>
        <figcaption>
          <p><b>Star Schema</b></p>
        </figcaption>
      <figure>
    </td>
  </tr>
</table>

## 📌 Visão geral
O fluxo principal é:

1. Carregamento das configurações
2. Configuração do logging
3. Consulta à API do IBGE
4. Retry automático em caso de falha
5. Conversão dos dados para DataFrame
6. Transformação e padronização
7. Criação do Star Schema
8. Conexão com o MySQL
9. Criação das tabelas dimensionais
10. Carga das dimensões
11. Carga da tabela fato
12. Liberação dos recursos

## 🎯 Objetivos do projeto
Este projeto foi desenvolvido para demonstrar conhecimentos práticos em:

* Engenharia de Dados
* Desenvolvimento de pipelines ETL
* Consumo de APIs REST
* Manipulação de dados com Pandas
* Modelagem dimensional
* Data Warehouse
* Star Schema
* SQL e MySQL
* SQLAlchemy
* Logging
* Retry e tolerância a falhas
* Testes automatizados
* Qualidade de código
* CI/CD
* Gerenciamento de dependências com Poetry
* Tipagem estática com MyPy
* Linting com Ruff

## ⭐ Modelo dimensional
Os dados são organizados em um modelo dimensional baseado em Star Schema.

### Dimensões
* dim_indicador
* dim_unidade
* dim_pais
* dim_tempo

### Fato
* fato_indicador

Estrutura simplificada:
```
                  dim_indicador
                        │
                        │
                        ▼
dim_unidade ─────► fato_indicador ◄───── dim_pais
                        │
                        │
                        ▼
                    dim_tempo
```
Esse modelo facilita consultas analíticas e permite organizar os dados de forma adequada para cenários de Data Warehouse, por exemplo.

## 📂 Estrutura do projeto
```
etl-python-ibge/
├── .github/
│    └── workflows
│         ├── ci.yml
│         └── release-please.yml
├── config/
│   ├── identifiers.yaml
│   ├── logging.yaml
│   └── paths.yaml
├── htmlcov/
├── images/
├── logs/
│   └── app.log
├── src/
│   └── etl_python_ibge/
│       ├── converts/
│       │    └── convert_to_df.py
│       ├── database/
│       │    └── get_connection.py
│       ├── ibge_api/
│       │    └── api_ibge.py
│       ├── load/
│       │   ├── load_schema/
│       │   │   └── load_table_schema.py
│       │   └── table_load/
│       │       └── load_tabble.py
│       ├── pipeline/
│       │       └── get_pipeline.py
│       ├── sql/
│       │   ├── create_star/
│       │   │   └── create_star_schema.sql
│       │   └── execute/
│       │       └── execute_sql.py
│       ├── star_schema/
│       │       └── get_star_schema.py
│       ├── utils/
│       │   ├── config_settings/
│       │   │   └── Settings.py
│       │   ├── load_yaml/
│       │   │   └── .py
│       │   ├── loggers/
│       │   │   └── logger.py
│       │   └── retry/
│       │       └── get_retry.py
│       └── main.py
├── tests/
│    ├── test_convert_to_df
│    ├── test_execute_sql.py
│    ├── test_get_engine.py
│    ├── test_get_ibge_api.py
│    ├── test_get_pipeline.py
│    ├── test_get_star_schema.py
│    ├── test_load_all_config.py
│    ├── test_load_table_schema.py
│    ├── test_load_table.py
│    ├── test_main.py
│    ├── test_get_retry.py
│    └── test_setup_logger.py
├── .coverage
├── .env
├── .env.example
├── test_get_retry.py.gitignore
├── .pre-commit-config.yaml
├── .release-please-manifest.json
├── CHANGELOG.md
├── LICENSE
├── poetry.lock
├── pyproject.toml
├── README.md
└── release-please-config.json
```

## ⚙️ Tecnologias
| Tecnologia | Utilização |
| ---------- | ---------- |
| Python | Desenvolvimento do ETL |
| Poetry | Gerenciamento de dependências |
| Pandas | Manipulação e transformação |
| Requests | Consumo da API |
| SQLAlchemy | Conexão com banco de dados |
| MySQL | Armazenamento |
| Pydantic | Settings	Configurações da aplicação |
| PyYAML | Configurações YAML |
| Rich | Interface visual do pipeline |
| Pytest | Testes automatizados |
| Pytest-Cov | Cobertura de testes |
| Ruff | Linting e formatação |
| MyPy | Verificação estática |
| Pre-commit | Automação de validações |
| GitHub Actions | CI/CD |
| Release Please | Automatização de releases |
| XAMPP | Servidor web local |

## 🔁 CI/CD
O projeto utiliza GitHub Actions para automatizar validações.

O pipeline de CI executa tarefas como:
```
Checkout
   ↓
Setup Python
   ↓
Poetry
   ↓
Instalação das dependências
   ↓
Ruff
   ↓
MyPy
   ↓
Pytest
   ↓
Coverage
```
A automação reduz a possibilidade de alterações com problemas chegarem à branch principal.

## 🔎 Qualidade de código
As validações são utilizadas para manter consistência, tipagem e qualidade do código.

* App: Executa aplicação. ```poetry run task app```
* Ruff:
    * format: altera os arquivos para deixá-los formatados. ```poetry run task format```
    * check: apenas verifica se os arquivos estão formatados. Não altera nada. ```poetry run task check```
    * lint: procura problemas como imports incorretos, código desnecessário, variáveis não utilizadas, etc. ```poetry run task lint```
    * fix: procura esses problemas e tenta corrigi-los automaticamente. ```poetry run task fix```
* Pytest: executa testes unitários. ```poetry run task pytest```
* Covhtml: executa os testes e gera relatório de cobertura em HTML. ```poetry run task covhtml```
* Covcmd: Executa testes mostrando cobertura no terminal. ```poetry run task covcmd```
* Mypy: Faz verificação estática de tipos. ```poetry run task mypy```
* Precommit</span>: Executa todos os hooks do pre-commit. ```poetry run task precommit```

## 🧪 Testes
Os testes são desenvolvidos com pytest.

Executar os testes:

```
poetry run task pytest
```

Executar com cobertura:

```
poetry run task covhtml
```

O pipeline utiliza mocks para isolar dependências externas, permitindo testar sua orquestração sem depender diretamente da API do IBGE ou de um banco MySQL real.

## 📦 Versionamento e Releases
O projeto utiliza versionamento semântico e Release Please.

Exemplo:

v0.13.0<br />
v0.14.0<br />
v0.15.0<br />
v0.15.1<br />

## 📝 Logging
O projeto possui sistema de logging configurável.

Os registros podem incluir:

* Início e término do pipeline;
* Quantidade de registros processados;
* Etapas de transformação;
* Conexão com banco;
* Criação de tabelas;
* Carga dos dados;
* Erros;
* Traceback de exceções.

Exemplo:

```
2026-08-12 15:06:31,900 - INFO - etl_python_ibge.ibge_api.api_ibge - Consultando indicador 77829.
2026-08-12 15:06:34,435 - INFO - etl_python_ibge.ibge_api.api_ibge - Consultando indicador 77834.
2026-08-12 15:06:37,004 - INFO - etl_python_ibge.ibge_api.api_ibge - Coleta finalizada com sucesso.
2026-08-12 15:06:37,017 - INFO - etl_python_ibge.pipeline.get_pipeline - Dados obtidos com sucesso da API do IBGE.
2026-08-12 15:06:37,055 - INFO - etl_python_ibge.pipeline.get_pipeline - Convertendo dados para DataFrame.
2026-08-12 15:06:37,057 - INFO - etl_python_ibge.converts.convert_to_df - Iniciando convrsão e limpeza dos dados.
2026-08-12 15:06:37,162 - INFO - etl_python_ibge.converts.convert_to_df - Finalizando a conversão e limpeza dos dados.
2026-08-12 15:06:37,173 - INFO - etl_python_ibge.pipeline.get_pipeline - Conversão concluída. Total de registros: 734
2026-08-12 15:06:37,181 - INFO - etl_python_ibge.pipeline.get_pipeline - Criando modelo dimensional Star Schema.
2026-08-12 15:06:37,186 - INFO - etl_python_ibge.star_schema.get_star_schema - Iniciando modelagem dos dados.
2026-08-12 15:06:37,187 - INFO - etl_python_ibge.star_schema.get_star_schema - Iniciando modelagem da dimensão indicador.
2026-08-12 15:06:37,199 - INFO - etl_python_ibge.star_schema.get_star_schema - Iniciando modelagem da dimensão unidade.
2026-08-12 15:06:37,216 - INFO - etl_python_ibge.star_schema.get_star_schema - Iniciando modelagem da dimensão país.
```

## 🔄 Retry e tolerância a falhas
A comunicação com a API utiliza mecanismo de retry para situações transitórias de rede.

Exemplo:
```
ibge_data = retry(
    partial(
        get_ibge_api,
        identifiers,
        url,
    ),
    max_attempts=3,
    delay=2,
)
```
Isso reduz o impacto de falhas temporárias de conexão.

Além disso, o pipeline registra exceções utilizando logging e garante o fechamento da conexão com o banco através de finally.

## 🔐 Configuração
As credenciais do banco de dados não são armazenadas no código.

Utilize um arquivo .env:

MYSQL_HOST=localhost<br />
MYSQL_PORT=3306<br />
MYSQL_USER=usuário<br />
MYSQL_PASSWORD=sua_senha<br />
MYSQL_DATABASE=ibge_database<br />

O arquivo .env deve permanecer fora do controle de versão.

Existe um arquivo de exemplo:

.env.example

## 🎯 Principais práticas aplicadas
O projeto busca aplicar princípios utilizados em ambientes profissionais:

* Separação de responsabilidades;
* Funções pequenas e reutilizáveis;
* Configuração externa;
* Gerenciamento seguro de credenciais;
* Logging estruturado;
* Tratamento de exceções;
* Retry para operações externas;
* Modelagem dimensional;
* Testes automatizados;
* Cobertura de código;
* Linting;
* Tipagem estática;
* Pre-commit;
* CI/CD;
* Versionamento semântico;
* Documentação técnica.

## 🛠️ Modo de Utilização
1. Execute o XAMPP
* Caso não o tenha, baixe-o: <a href="https://www.apachefriends.org/pt_br/download.html">https://www.apachefriends.org/pt_br/download.html</a>
* Instale-o normalmente
* Execute o Painel de Controle
* Acione o Apache e o MySQL/MariaDB

2. Com a linguagem Python instalada: <a href="https://www.python.org/downloads/" target="_blank">https://www.python.org/downloads/</a>
3. Instale o pipx:
```
pip install pipx
```
4. Em seguida:
```
pipx ensurepath
```
5. E, por fim, o gerenciador Poetry:
```
pipx install poetry
```
6. Clone o repositório e acesse o diretório
```
git clone https://github.com/jcarlossc/etl-python-ibge.git
cd etl-python-ibge
```
7. Instalação das dependências:
```
poetry install
```
9. Para executar o projeto:
```
poetry run task app
```

## 📚 Licença
Este projeto está licenciado sob MIT License.

## 🎯 Desenvolvedor focado em:

- Data Engineering
- Analytics
- R Programming
- Python Programming
- Automação de processos
- Engenharia de Software

## 📝 Contato
* Autor: Carlos da Costa
* Recife, PE - Brasil
* Telefone: +55 81 99712 9140
* Telegram: @jcarlossc
* Blogger linguagem R: https://informaticus77-r.blogspot.com/
* Blogger linguagem Python: https://informaticus77-python.blogspot.com/
* Email: jcarlossc1977@gmail.com
* LinkedIn: https://www.linkedin.com/in/carlos-da-costa-669252149/
* GitHub: https://github.com/jcarlossc
* Kaggle: https://www.kaggle.com/jcarlossc/
* Twitter/X: https://x.com/jcarlossc1977
