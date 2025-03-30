import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": "app.log",
            "level": "DEBUG",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
    "loggers": {
        "app": { 
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
