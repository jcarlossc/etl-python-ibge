import logging
from functools import partial
from pathlib import Path

from etl_python_ibge.converts.convert_to_df import get_convert
from etl_python_ibge.database.get_connection import get_engine
from etl_python_ibge.ibge_api.api_ibge import get_ibge_api
from etl_python_ibge.load.load_schema.load_table_schema import load_star_schema
from etl_python_ibge.sql.execute.execute_sql import execute_sql
from etl_python_ibge.star_schema.get_star_schema import create_star_schema
from etl_python_ibge.utils.config_settings.Settings import get_settings
from etl_python_ibge.utils.load_yaml.loader_yaml import load_all_configs
from etl_python_ibge.utils.loggers.logger import setup_logger
from etl_python_ibge.utils.retry.get_retry import retry


def run_pipeline() -> None:
    """
    Executa o pipeline completo de ETL dos dados do IBGE.

    O pipeline executa as seguintes etapas:

    1. Carrega as configurações do projeto.
    2. Configura o sistema de logging.
    3. Consulta a API do IBGE.
    4. Converte os dados recebidos para DataFrame.
    5. Cria o modelo dimensional (Star Schema).
    6. Cria a conexão com o banco de dados.
    7. Executa o script SQL de criação das tabelas.
    8. Carrega as dimensões e fatos no banco de dados.
    9. Libera a conexão com o banco.

    Raises
    ------
    Exception
        Propaga qualquer erro ocorrido durante a execução do pipeline
        após registrar o erro no log.
    """

    from rich.console import Console
    from rich.progress import (
        BarColumn,
        Progress,
        SpinnerColumn,
        TextColumn,
        TimeElapsedColumn,
    )

    console = Console()

    # ==============================================================
    # Rich Progress
    # ==============================================================
    with Progress(
        SpinnerColumn(
            style="cyan",
        ),
        TextColumn(
            "[bold]{task.description}",
        ),
        BarColumn(
            complete_style="cyan",
            finished_style="green",
            pulse_style="yellow",
        ),
        TextColumn(
            "[dim]{task.completed}/{task.total}[/dim]",
        ),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(
            "[cyan]Iniciando pipeline ETL...",
            total=8,
        )

        # ------------------------------------------------------------------
        # 1. Carrega as configurações
        # ------------------------------------------------------------------

        logger = logging.getLogger(__name__)

        try:
            # Rich de entrada
            progress.update(
                task,
                description="[cyan]Carregando configurações...",
            )

            config_path = Path("config")

            # Rich de saída
            progress.advance(task)
            console.log("[green]✓ Configurações carregadas")

        except Exception:
            logger.exception("Erro ao carregar as configurações.")

            # Rich de falha
            progress.update(
                task,
                description="[red]✗ Erro nas configurações",
            )

            raise

        # ------------------------------------------------------------------
        # 2. Configura o logger
        # ------------------------------------------------------------------

        try:
            # Rich de entrada
            progress.update(
                task,
                description="[cyan]Configurando logger...",
            )

            configs = load_all_configs(config_path)

            setup_logger(
                configs["logging"],
                configs["paths"]["logs"]["file"],
            )

            # Rich de saída
            progress.advance(task)
            console.log("[green]✓ Logger configurado")

        except Exception:
            logger.exception("Erro ao configurar o logger.")

            # Rich de falha
            progress.update(
                task,
                description="[red]✗ Erro no logger",
            )

            raise

        # ------------------------------------------------------------------
        # 3. Consome a API do IBGE
        # ------------------------------------------------------------------

        logger.info("Iniciando pipeline ETL do IBGE")

        try:
            logger.info("Iniciando coleta dos dados do IBGE.")

            # Rich de entrada
            progress.update(
                task,
                description="[cyan]Consultando API do IBGE... Aguarde...",
            )

            ibge_data = retry(
                partial(
                    get_ibge_api,
                    configs["identifiers"]["identifiers"],
                    configs["identifiers"]["url"],
                ),
                max_attempts=3,
                delay=2,
            )

            logger.info("Dados obtidos com sucesso da API do IBGE.")

            # Rich de saída
            progress.advance(task)
            console.log("[green]✓ Dados obtidos da API do IBGE")

        except Exception:
            logger.exception("Erro durante a coleta dos dados do IBGE.")

            # Rich de falha
            progress.update(
                task,
                description="[red]✗ Erro na API do IBGE",
            )

            raise

        # ------------------------------------------------------------------
        # 4. Converte os dados para DataFrame
        # ------------------------------------------------------------------

        try:
            logger.info("Convertendo dados para DataFrame.")

            # Rich de entrada
            progress.update(
                task,
                description="[cyan]Convertendo dados para DataFrame...",
            )

            ibge_df = get_convert(ibge_data)

            logger.info(
                "Conversão concluída. Total de registros: %s",
                len(ibge_df),
            )

            # Rich de saída
            progress.advance(task)
            console.log("[green]✓ DataFrame criado ")

        except Exception:
            logger.exception("Erro durante a conversão dos dados.")

            # Rich de falha
            progress.update(
                task,
                description="[red]✗ Erro na conversão",
            )

            raise

        # ------------------------------------------------------------------
        # 5. Cria o Star Schema
        # ------------------------------------------------------------------

        try:
            logger.info("Criando modelo dimensional Star Schema.")

            # Rich de entrada
            progress.update(
                task,
                description="[cyan]Criando Star Schema...",
            )

            ibge_star_schema = create_star_schema(ibge_df)

            logger.info(
                "Star Schema criado com sucesso. Tabelas: %s",
                list(ibge_star_schema.keys()),
            )

            # Rich de saída
            progress.advance(task)
            console.log("[green]✓ Star Schema criado")

        except Exception:
            logger.exception("Erro ao criar o Star Schema.")

            # Rich de falha
            progress.update(
                task,
                description="[red]✗ Erro no Star Schema",
            )

            raise

        # ------------------------------------------------------------------
        # 6. Cria conexão com o banco de dados
        # ------------------------------------------------------------------

        engine = None

        try:
            logger.info("Criando conexão com o banco de dados.")

            # Rich de entrada
            progress.update(
                task,
                description="[cyan]Conectando ao banco de dados...",
            )

            # Representa as configurações da aplicação (.env).
            settings = get_settings()

            engine = get_engine(settings)

            logger.info("Conexão com o banco de dados criada com sucesso.")

            # Rich de saída
            progress.advance(task)
            console.log("[green]✓ Conectado ao banco")

            # --------------------------------------------------------------
            # 7. Cria as tabelas do Star Schema
            # --------------------------------------------------------------

            logger.info("Executando script de criação do Star Schema.")

            # Rich de entrada
            progress.update(
                task,
                description="[cyan]Criando tabelas no banco...",
            )

            execute_sql(
                engine=engine,
                sql_file=Path(
                    "src/etl_python_ibge/sql/create_star/create_star_schema.sql"
                ),
            )

            logger.info("Estrutura do banco criada com sucesso.")

            # Rich de saída
            progress.advance(task)
            console.log("[green]✓ Tabelas criadas")

            # --------------------------------------------------------------
            # 8. Carrega os dados no banco
            # --------------------------------------------------------------

            logger.info("Iniciando carga do Star Schema.")

            # Rich de entrada
            progress.update(
                task,
                description="[cyan]Carregando dados no banco...",
            )

            load_star_schema(
                star_schema=ibge_star_schema,
                engine=engine,
            )

            logger.info("Carga do Star Schema concluída com sucesso.")

            # Rich de saída
            progress.advance(task)
            console.log("[green]✓ Dados carregados")

        except Exception:
            logger.exception("Erro durante a criação ou carga do banco de dados.")

            # Rich de falha
            progress.update(
                task,
                description="[red]✗ Erro no banco de dados",
            )

            raise

        finally:
            # --------------------------------------------------------------
            # 9. Libera os recursos
            # --------------------------------------------------------------

            if engine is not None:
                engine.dispose()

                logger.info("Conexão com o banco de dados encerrada.")

            # Rich de saída
            progress.advance(task)
            console.log("[green]✓ Conexão finalizada.")

        logger.info("Pipeline ETL finalizado com sucesso.")

        # Finaliza visualmente o Progress
        progress.update(
            task,
            description="[bold green]✓ Pipeline concluído",
        )
