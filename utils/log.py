import os
os.makedirs('logs', exist_ok=True)

import logging.config
config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s[%(levelname)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/pcrd-discordbot.log',
            'level': 'DEBUG',
            'formatter': 'simple',
            'when': 'D',
            'interval': 1,
            'backupCount': 10,
            'encoding': 'utf-8'
        }
    },
    'loggers':{
        'StreamLogger': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'FileLogger': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        }
    }
}
logging.config.dictConfig(config)
StreamLogger = logging.getLogger("StreamLogger")
FileLogger = logging.getLogger("FileLogger")