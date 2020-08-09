import os
import multiprocessing
from typing import (
    Callable
)

import gunicorn.app.base
from nginx.config.api import Section, Location

from rest_api_service import config
from rest_api_service.api.common import logging
from rest_api_service.api.common.error import handle_exception_commonly
from rest_api_service.api import app

flask_app = app.get_flask_app()
logger = logging.get_logger()


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    # ref : http://docs.gunicorn.org/en/stable/custom.html
    def __init__(self, flask_app, options=None):
        self.options = options or {}
        self.flask_app = flask_app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.flask_app


@handle_exception_commonly
def run_nginx(configs: dict):
    if not isinstance(configs, dict):
        configs = {}
    nginx_port = configs.get('NGINX_PORT', '3000')
    gunicorn_port = configs.get('GUNICORN_PORT', '9700')
    server = Section('server',
                     Location('/', proxy_pass=f'http://127.0.0.1:{gunicorn_port}'),
                     listen=nginx_port,
                     server_name='rest-api-web-server'
                     )
    with open('/etc/nginx/sites-available/default', 'w+') as f:
        f.write(server.__str__())
    os.system("nginx -g 'daemon on;'")


@handle_exception_commonly
def run_gunicorn(configs: dict):
    if not isinstance(configs, dict):
        configs = {}

    gunicorn_port = configs.get('GUNICORN_PORT', '9700')
    number_of_workers = configs.get('NUMBER_OF_WORKERS', (multiprocessing.cpu_count() * 2) + 1)
    number_of_threads = configs.get('NUMBER_OF_THREADS', abs((2 - (multiprocessing.cpu_count() * 4))))
    options = {
        'bind': f'127.0.0.1:{gunicorn_port}',
        'workers': number_of_workers,
        # 'worker_class': 'sync',
        'threads': number_of_threads,
        # 'keepalive': 2,
        # 'reload': False,
        # 'access_log_format': '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"',
        # 'loglevel': 'info',
        'daemon': True
    }
    StandaloneApplication(flask_app, options).run()


if __name__ == "__main__":
    logger.info("REST API Server Configs Initialization...")
    configs = config.get_configs()
    config.print_configs()

    run_nginx(configs)
    run_gunicorn(configs)
    logger.info("REST API Server Run Completed.")
