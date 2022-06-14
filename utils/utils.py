from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BaseAPIView(APIView):

    def success_response(self, payload, description):
        return Response({
            "payload": payload,
            "success": True,
            "description": description,
            "error": {}
        }, status=status.HTTP_200_OK)

    def bad_request_response(self, error, description):
        return Response({
            "payload": {},
            "success": False,
            "error": error,
            "description": description,
        }, status=status.HTTP_400_BAD_REQUEST)

