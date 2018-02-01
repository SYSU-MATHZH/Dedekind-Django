from rest_framework.views import exception_handler
from rest_framework import status

from django.http import HttpResponseRedirect
from django.conf import settings

def redirect_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN):
            return HttpResponseRedirect('/?status=%s' % response.status_code)

    return response
