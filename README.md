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
