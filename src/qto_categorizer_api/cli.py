"""CLI qt-categorizer-api"""

import logging
import uvicorn

from qto_categorizer_api.setup_logging import setup_logging
from qto_categorizer_api.settings.app_settings import Settings, get_settings


def start_api() -> None:
    settings: Settings = get_settings()
    log_config: dict = setup_logging(log_level=settings.log_level)

    logger = logging.getLogger(__name__)
    logger.setLevel(settings.log_level)
    logger.info("[API] Log level set to %s", {settings.log_level})
    logger.info(f"[API] API service starting on {settings.svr_host}:{settings.svr_port}")

    uvicorn.run(
        "qto_categorizer_api.app:app",
        host=settings.svr_host,
        port=settings.svr_port,
        root_path=settings.root_path,
        log_config=log_config,
        log_level=settings.log_level.lower(),
        workers=settings.workers,
    )


if __name__ == "__main__":
    start_api()
