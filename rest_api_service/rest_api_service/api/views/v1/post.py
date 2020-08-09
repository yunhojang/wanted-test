import flask
from rest_api_service.api.common import error
from rest_api_service.api.common.enumeration import ErrorType
from rest_api_service.api.common import logging
from rest_api_service.api.services import post_service
from . import validation

logger = logging.get_logger()
v1_post = flask.Blueprint('v1_post', __name__)


@v1_post.route('/company-name/autocomplete', methods=['POST'])
def post_company_name_autocomplete():
    request_body = flask.request.get_json()
    if request_body is None:
        error_ = error.Error(ErrorType.BadRequest, "The request body's type is Not JSON or Not Allowed.")
        flask.abort(400, error_)

    ret = validation.validate_request_body(request_body, type_='AUTOCOMPLETE')
    if isinstance(ret, error.Error):
        flask.abort(400, ret)

    request_body.update(startOffset=request_body.get('startOffset', 0))
    request_body.update(limit=request_body.get('limit', 10))
    request_body.update(orderBy=request_body.get('orderBy', 'desc'))

    response = {'result': {'totalCount': 0, 'gettedCount': 0, 'results': []}}

    if request_body['limit'] == 0:
        return flask.jsonify(response), 200

    serv_ret = post_service.get_autocompleted_companys(condition_params=request_body)
    if isinstance(serv_ret, error.Error):
        flask.abort(500, error.Error(ErrorType.InternalError, serv_ret.message))

    response.update(result=serv_ret)

    return flask.jsonify(response), 200


@v1_post.route('/company/search', methods=['POST'])
def post_company_search():
    request_body = flask.request.get_json()
    if request_body is None:
        error_ = error.Error(ErrorType.BadRequest, "The request body's type is Not JSON or Not Allowed.")
        flask.abort(400, error_)

    ret = validation.validate_request_body(request_body, type_='SEARCH')
    if isinstance(ret, error.Error):
        flask.abort(400, ret)

    request_body.update(tagCountry=request_body.get('tagCountry', 'all'))

    response = {'result': {'totalCount': 0, 'gettedCount': 0, 'results': []}}

    serv_ret = post_service.get_company(condition_params=request_body)
    if isinstance(serv_ret, error.Error):
        flask.abort(500, error.Error(ErrorType.InternalError, serv_ret.message))

    response.update(result=serv_ret)

    return flask.jsonify(response), 200


@v1_post.route('/company-tag/add', methods=['POST'])
def post_company_tag_add():
    request_body = flask.request.get_json()
    if request_body is None:
        error_ = error.Error(ErrorType.BadRequest, "The request body's type is Not JSON or Not Allowed.")
        flask.abort(400, error_)

    ret = validation.validate_request_body(request_body, type_='COMPANY_TAG')
    if isinstance(ret, error.Error):
        flask.abort(400, ret)

    serv_ret = post_service.add_company_tag(inputs=request_body)
    if isinstance(serv_ret, error.Error):
        flask.abort(500, error.Error(ErrorType.InternalError, serv_ret.message))

    return 'OK', 201


@v1_post.route('/company-tag/remove', methods=['POST'])
def post_company_tag_remove():
    request_body = flask.request.get_json()
    if request_body is None:
        error_ = error.Error(ErrorType.BadRequest, "The request body's type is Not JSON or Not Allowed.")
        flask.abort(400, error_)

    ret = validation.validate_request_body(request_body, type_='COMPANY_TAG')
    if isinstance(ret, error.Error):
        flask.abort(400, ret)

    serv_ret = post_service.remove_company_tag(condition_params=request_body)
    if isinstance(serv_ret, error.Error):
        flask.abort(500, error.Error(ErrorType.InternalError, serv_ret.message))

    return 'OK', 201


@v1_post.app_errorhandler(400)
def handle_400(Error):
    if hasattr(Error.description, 'error_type'):
        error_type, error_message = Error.description.error_type.value, Error.description.message
    else:
        error_type, error_message = ErrorType.Unknown.value, Error.description

    return flask.jsonify({'errorType': error_type, 'errorMessage': error_message}), 400


@v1_post.app_errorhandler(500)
def handle_500(Error):
    if hasattr(Error.description, 'error_type'):
        error_type, error_message = Error.description.error_type.value, Error.description.message
    else:
        error_type, error_message = ErrorType.Unknown.value, Error.description

    return flask.jsonify({'errorType': error_type, 'errorMessage': error_message}), 500
