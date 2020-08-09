import flask
from flask_log_request_id import RequestID
from rest_api_service.api.common.enumeration import ErrorType
from rest_api_service.api.views.v1 import (
    ping, post
)

def handle_400(Error):
    error = {
        'errorType': ErrorType.BadRequest.value,
        'errorMessage': 'The request is malformed, such as message body format error.'
    }
    return flask.jsonify(error), 400


def handle_404(Error):
    error = {
        'errorType': ErrorType.NotFound.value,
        'errorMessage': 'The requested resource could not be found but may be available in the future.'
    }
    return flask.jsonify(error), 404


def handle_500(Error):
    error = {
        'errorType': ErrorType.InternalError.value,
        'errorMessage': 'An unexpected condition prevented the server from fulfilling the request.'
    }
    return flask.jsonify(error), 500


def get_flask_app():
    flask_app = flask.Flask('rest-api')
    flask_app.register_error_handler(400, handle_400)
    flask_app.register_error_handler(404, handle_404)
    flask_app.register_error_handler(500, handle_500)

    flask_app.register_blueprint(ping.v1_ping, url_prefix='/v1')
    flask_app.register_blueprint(post.v1_post, url_prefix='/v1')

    RequestID(flask_app)
    return flask_app
