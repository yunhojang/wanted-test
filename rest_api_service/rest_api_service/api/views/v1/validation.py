import fastjsonschema
from collections.abc import Mapping
from typing import Union
from rest_api_service.api.common import error
from rest_api_service.api.common.enumeration import ErrorType

REQ_BODY_SCHEMA = {
    'AUTOCOMPLETE': {
        'type': 'object',
        'required': ['companyName'],
        'properties': {
            'companyName': {'type': 'string', 'nullable': False},
            'startOffset': {'type': 'integer'},
            'limit': {'type': 'integer'},
            'orderBy': {'type': 'string', 'nullable': False, 'enum': ['desc', 'asc']}
        },
        'additionalProperties': False
    },
    'SEARCH': {
        'type': 'object',
        'required': ['tagName'],
        'properties': {
            'tagName': {'type': 'string', 'nullable': False},
            'tagCountry': {'type': 'string', 'nullable': False, 'enum': ['all', 'ko', 'ja']}
        },
        'additionalProperties': False
    },
    'COMPANY_TAG': {
        'type': 'object',
        'required': ['companyName', 'tagConuntry', 'tag'],
        'properties': {
            'companyName': {'type': 'string', 'nullable': False},
            'tagCountry': {'type': 'string', 'nullable': False},
            'tag': {'type': 'string', 'nullable': False}
        },
        'additionalProperties': False
    }
}


@error.handle_exception_commonly
def validate_request_body(request_body: Mapping, type_: str = None) -> Union[error.Error, None]:
    if not isinstance(request_body, Mapping):
        return error.Error(ErrorType.BadRequest, "Not allowed: request body's schema.")

    validate = fastjsonschema.compile(REQ_BODY_SCHEMA.get(type_, None))
    if validate is None:
        return error.Error(ErrorType.BadRequest, "No exist: request body's schema.")

    try:
        validate(request_body)
    except Exception as e:
        return error.Error(ErrorType.BadRequest, f"Invalid: request body's {e}.")
    return
