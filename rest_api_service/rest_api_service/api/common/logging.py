import os
import logging
import logging.config

LOG_FORMAT = ('%(asctime)s | %(levelname)s | %(process)d.%(thread)d | %(module)s.%(funcName)s():%(lineno)d ' +
              '| %(request_id)s | %(message)s')
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': LOG_FORMAT
        },
    },
    'filters': {
        'request': {
            '()': 'flask_log_request_id.filters.RequestIDLogFilter'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['request']
        },
    },
    'root': {
        'handlers': ['console'],
        'filters': ['request'],
        'level': 'INFO'
    }
}


def singleton(cls_):
    instances = {}

    def _getinstance(*args, **kwargs):
        if cls_ not in instances:
            instances[cls_] = cls_(*args, **kwargs)
        return instances[cls_]

    return _getinstance


@singleton
def get_logger() -> logging.Logger:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    return logger
