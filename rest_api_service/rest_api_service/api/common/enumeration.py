from enum import Enum


class ErrorType(Enum):
    BadRequest = 'BadRequest'
    NotFound = 'NotFound'
    InternalError = 'InternalError'
    Unknown = 'Unknown'
