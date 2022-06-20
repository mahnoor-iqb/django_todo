from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, NotFound
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

    elif isinstance(exc, PermissionDenied):
        return Response({
            "payload": {},
            "success": False,
            "error": exc.detail,
            "description": "You do not have permission to perform this operation",
        }, status=status.HTTP_403_FORBIDDEN)

    elif isinstance(exc, NotFound):
        return Response({
            "payload": {},
            "success": False,
            "error": exc.detail,
            "description": "URL not found",
        }, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({
            "payload": {},
            "success": False,
            "error": {},
            "description": "Something went wrong",
        }, status=status.HTTP_400_BAD_REQUEST)
