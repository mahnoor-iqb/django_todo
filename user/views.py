from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

import logging
logger = logging.getLogger('django')


class UserApiView(APIView):
    # 1. List all
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)

        logger.info("Users retreived successfully")
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=data)

        if user_serializer.is_valid():
            user_serializer.save()
            logger.info("User added successfully")
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        logger.error("Unable to add user")
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailApiView(APIView):

    # Helper method
    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, user_id, *args, **kwargs):
        user_instance = self.get_object(user_id)
        if not user_instance:
            logger.error("Object with user id does not exist")
            return Response(
                {"message": "Object with user id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(user_instance)

        logger.info("User retreived successfully")
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, user_id, *args, **kwargs):
        user_instance = self.get_object(user_id)
        if not user_instance:
            logger.error("Object with user id does not exist")
            return Response(
                {"message": "Object with user id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = JSONParser().parse(request)
        serializer = UserSerializer(
            instance=user_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("User updated successfully")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, user_id, *args, **kwargs):
        user_instance = self.get_object(user_id)
        if not user_instance:
            logger.error("Object with user id does not exist")
            return Response(
                {"message": "Object with user id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_instance.delete()
        logger.info("User deleted")
        return Response(
            {"message": "Object deleted!"},
            status=status.HTTP_200_OK
        )
