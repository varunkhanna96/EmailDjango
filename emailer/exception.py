import logging
from functools import wraps

from django.contrib import messages
from django.shortcuts import HttpResponseRedirect

LOGGER = logging.getLogger(__name__)


def exception_handler(errors=(Exception, )):
    """
    This function is used to return a new dict with mapped keys.
    Usage::
        #>>> import exception_handler
        #>>> @exception_handler(errors=(ParticipantResolutionError, Exception))
        #>>> foo(self, request, context)

    :param errors: tuple: tuple of exception classes that is needed to be handled.
    """
    def check_exception(func):
        @wraps(func)
        def wrapper(request):
            """
            This wrapper function wraps the decorated function with try and except
            """
            try:
                return func(request)
            except errors as exception:
                LOGGER.error("Some unknown exception occured", exc_info=True)
                messages.info(request, f"Unexpected {exception.__class__.__name__} : {exception}!")
                return HttpResponseRedirect('/error')
        return wrapper
    return check_exception
