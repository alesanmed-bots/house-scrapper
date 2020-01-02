# encoding: utf-8
import logging.config
from os import path

PROJECT_ROOT = path.abspath(path.join(path.dirname(__file__), '../'))

# Logger config
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)-5s %(levelname)-8s '
            + '%(funcName)-8s:%(lineno)-4d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
        'deb_file': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8',
            'filename': path.join(PROJECT_ROOT, 'logs', 'app.log')
        },
        'err_file': {
            'level': 'ERROR',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8',
            'filename': path.join(PROJECT_ROOT, 'logs', 'error.log')
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'deb_file', 'err_file'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
})
