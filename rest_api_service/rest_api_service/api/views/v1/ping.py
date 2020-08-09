import flask
from rest_api_service.api.common import logging

logger = logging.get_logger()
v1_ping = flask.Blueprint('v1_ping', __name__)


@v1_ping.route('/ping', methods=['GET'])
def ping() -> str:
    """Default route"""

    logger.info(f'This is {ping.__name__}')
    return 'pong', 200
