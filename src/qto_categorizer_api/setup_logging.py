import logging

from qto_categorizer_api import __version__
from qto_categorizer_api.settings.defaults import LOG_LEVEL


def setup_logging(log_level: str = LOG_LEVEL) -> dict:
    """Setup logger."""
    log_format = "[\%(asctime)s] {\%(name)s} \%(levelname)s - \%(message)s"

    logging.basicConfig(level=log_level, format=log_format)

    logging.info("[API] Starting service with version %s...", __version__)
    logging.info("[API] Log level set to %s", log_level)

    log_config: dict = {
        "version": 1,
        "formatters": {"default": {"format": log_format}},
        "handlers": {
            "console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "level": log_level,
            }
        },
        "root": {"handlers": ["console"], "level": log_level},
        "loggers": {
            "gunicorn": {"propagate": True},
            "uvicorn": {"propagate": True},
            "uvicorn.access": {"propagate": True},
        },
    }

    return log_config
