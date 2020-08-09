import os
import multiprocessing
from typing import Mapping
from rest_api_service.api.common.logging import get_logger
from rest_api_service.api.common.error import handle_exception_commonly

logger = get_logger()

DEFAULT_APP_NAME = 'rest-api'
DEFAULT_NGINX_PORT = '3000'
DEFAULT_GUNICORN_PORT = '9700'
DEFAULT_NUMBER_OF_WORKERS = (multiprocessing.cpu_count() * 2) + 1
DEFAULT_NUMBER_OF_THREADS = abs((2 - (multiprocessing.cpu_count() * 4)))
DEFAULT_MONGO_URI = 'mongodb://mongo-1:27017/wanted'
DEFAULT_MONGO_TIMEOUT_MS = 200

configs = {
    'APP_NAME': os.environ.get('APP_NAME', DEFAULT_APP_NAME),
    'APP_ENV': os.environ.get('APP_ENV', 'prod'),
    'NGINX_PORT': os.environ.get('NGINX_PORT', DEFAULT_NGINX_PORT),
    'GUNICORN_PORT': os.environ.get('GUNICORN_PORT', DEFAULT_GUNICORN_PORT),
    'NUMBER_OF_WORKERS': os.environ.get('NUMBER_OF_WORKERS', DEFAULT_NUMBER_OF_WORKERS),
    'NUMBER_OF_THREADS': os.environ.get('NUMBER_OF_THREADS', DEFAULT_NUMBER_OF_THREADS),
    'MONGO_URI': os.environ.get('MONGO_URI', DEFAULT_MONGO_URI),
    'MONGO_TIMEOUT_MS': os.environ.get('MONGO_TIMEOUT_MS', DEFAULT_MONGO_TIMEOUT_MS)
}


@handle_exception_commonly
def print_configs():
    logger.info("Configs:")
    for key, val in configs.items():
        logger.info(f" {key}: {val}")


@handle_exception_commonly
def get_configs() -> Mapping:
    return configs
