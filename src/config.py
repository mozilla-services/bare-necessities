import sys


class Config(object):
    DEBUG = False
    TESTING = False
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
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "json",
                "stream": sys.stdout,
            }
        },
        "loggers": {
            "web.api": {"handlers": ["console"], "level": "DEBUG"},
            "request.summary": {"handlers": ["console"], "level": "INFO"},
        },
    }


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False


class StagingConfig(Config):
    ENV = "staging"
    DEBUG = False


class DevConfig(Config):
    ENV = "dev"
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
