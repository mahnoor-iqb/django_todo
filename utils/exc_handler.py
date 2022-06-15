from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        return Response({
            "payload": {},
            "success": False,
            "error": exc.detail,
            "description": "Unauthorized users are not allowed on this path",
        }, status=status.HTTP_401_UNAUTHORIZED)

    return exception_handler(exc, context)