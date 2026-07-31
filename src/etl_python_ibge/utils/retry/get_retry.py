import logging
import time
from typing import Any

import requests


def retry(connect, max_attempts=3, delay=2) -> Any:
    """
    Executa uma função com nova tentativa automática em caso de falhas
    temporárias de comunicação com serviços externos.

    Utiliza backoff exponencial entre as tentativas para reduzir a carga
    sobre o servidor e aumentar as chances de sucesso em falhas transitórias.

    Args:
        connect (Callable):
            Função responsável por executar a operação.

        max_attempts (int, optional):
            Número máximo de tentativas. Default é 3.

        delay (int | float, optional):
            Tempo inicial (em segundos) entre as tentativas.
            O tempo é multiplicado exponencialmente.

    Returns:
        Any:
            Resultado retornado pela função executada.

    Raises:
        requests.RequestException:
            Relança a exceção caso todas as tentativas falhem.
    """

    logger = logging.getLogger(__name__)

    # Executa a operação até atingir o número máximo de tentativas.
    for attempt in range(max_attempts):
        try:
            # Retorna imediatamente caso obtenha sucesso.
            return connect()

        except requests.RequestException as exc:
            logger.warning(
                "Tentativa %d/%d falhou: %s",
                attempt + 1,
                max_attempts,
                exc,
            )

            # Aguarda somente se ainda existirem tentativas restantes.
            if attempt < max_attempts - 1:
                # Backoff exponencial:
                # tentativa 1 -> delay
                # tentativa 2 -> delay * 2
                # tentativa 3 -> delay * 4
                time.sleep(delay * (2**attempt))

            else:
                logger.error("Número máximo de tentativas atingido.")

                # Relança a exceção original para quem chamou a função.
                raise
