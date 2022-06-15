from email.policy import default
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

    def created_response(self, payload, description):
        return Response({
            "payload": payload,
            "success": True,
            "description": description,
            "error": {}
        }, status=status.HTTP_201_CREATED)

    def bad_request_response(self, error, description):
        return Response({
            "payload": {},
            "success": False,
            "error": error,
            "description": description,
        }, status=status.HTTP_400_BAD_REQUEST)

    def permission_denied_response(self, error, description):
        return Response({
            "payload": {},
            "success": False,
            "error": error,
            "description": description,
        }, status=status.HTTP_403_FORBIDDEN)

    def paginate_queryset(self, request, results):
        default_limit = 50
        max_limit = 100
        min_limit = 1

        default_offset = 0
        min_offset = 0
        max_offset = 10

        limit = int(request.GET.get("limit", default_limit))
        offset = int(request.GET.get("offset", default_offset))

        if min_limit > limit > max_limit:
            limit = default_limit

        if min_offset > offset > max_offset:
            offset = default_offset

        results = results[offset: offset + limit]
        
        return results
