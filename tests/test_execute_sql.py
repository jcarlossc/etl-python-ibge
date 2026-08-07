from pathlib import Path

import pytest
from sqlalchemy import create_engine

from etl_python_ibge.sql.execute.execute_sql import execute_sql


def test_execute_sql_success(tmp_path: Path) -> None:
    """
    Deve executar um script SQL sem lançar exceções.
    """

    sql_file = tmp_path / "script.sql"

    sql_file.write_text(
        """
        CREATE TABLE teste(
            id INTEGER PRIMARY KEY
        );
        """,
        encoding="utf-8",
    )

    engine = create_engine("sqlite:///:memory:")

    execute_sql(
        engine=engine,
        sql_file=sql_file,
    )


def test_execute_sql_file_not_found() -> None:
    """
    Deve lançar FileNotFoundError quando o arquivo
    não existir.
    """

    engine = create_engine("sqlite:///:memory:")

    with pytest.raises(FileNotFoundError):
        execute_sql(
            engine=engine,
            sql_file=Path("arquivo_inexistente.sql"),
        )
