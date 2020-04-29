import sys
from decouple import config

HOST = config("HOST", default="0.0.0.0")  # nosec
PORT = config("PORT", default=8000, cast=int)
DEBUG = config("FLASK_DEBUG", default=False, cast=bool)
TESTING = config("FLASK_TESTING", default=False, cast=bool)

LOG_LEVEL = config("LOG_LEVEL", default="INFO").upper()
LOG_FORMAT = config("LOG_FORMAT", default="json")
LOGGING = {
    "version": 1,
    "formatters": {
        "text": {
            "format": "%(name)s [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": "dockerflow.logging.JsonLogFormatter",
            "logger_name": "web.api",
        },
    },
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": LOG_FORMAT,
            "stream": sys.stdout,
        }
    },
    "loggers": {
        "web.api": {"handlers": ["console"], "level": "DEBUG"},
        "request.summary": {"handlers": ["console"], "level": "INFO"},
    },
}

SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI", default="", cast=str)
SQLALCHEMY_TRACK_MODIFICATIONS = config(
    "SQLALCHEMY_TRACK_MODIFICATIONS", default=False, cast=bool
)
