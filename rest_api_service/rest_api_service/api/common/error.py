from . import logging
from .enumeration import ErrorType
from typing import Callable, Tuple, List, Union

logger = logging.get_logger()


class Error(Exception):
    def __init__(self, error_type, error_message):
        if isinstance(error_type, ErrorType):
            self.error_type = error_type
        if error_message:
            self.message = error_message
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"{self.message}."
        else:
            return "Error has been raised."


def handle_exception_commonly(func: Callable) -> Callable:
    def _func_wrapper(*args, **kwargs) -> Union[Callable, Error]:
        try:
            logger.info(f"This {func.__name__}'s args: {args}, kwargs: {kwargs}")
            return func(*args, **kwargs)
        except Exception as e:
            logger.debug(f"This {func.__name__} Error: {e}")
            if hasattr(e, 'error_type'):
                return e
            return Error(ErrorType.Unknown, f"{e}")
    return _func_wrapper
