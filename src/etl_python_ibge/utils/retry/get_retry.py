import logging
import time

import requests


def retry(connect, max_attempts=3, delay=2):
    logger = logging.getLogger(__name__)

    for attempt in range(max_attempts):
        try:
            return connect()

        except requests.RequestException as exc:
            logger.warning(
                "Tentativa %d/%d falhou: %s",
                attempt + 1,
                max_attempts,
                exc,
            )

            if attempt < max_attempts - 1:
                time.sleep(delay * (2**attempt))

            else:
                logger.error("Número máximo de tentativas atingido.")

                raise
