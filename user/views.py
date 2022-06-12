import imp
from user.models import User
import user.serializers
from rest_framework import status
from utils.utils import BaseAPIView

import logging
logger = logging.getLogger('django')


class UserApiView(BaseAPIView):
    serializer_class = user.serializers.UserSerializer

    # 1. List all
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        user_serializer = self.serializer_class(users, many=True)
        logger.info("Users retreived successfully")
        return self.success_response(payload=user_serializer.data, description="Users retreived successfully")

    # 2. Create
    def post(self, request, *args, **kwargs):
        user_serializer = self.serializer_class(data=request.data)

        if not user_serializer.is_valid():
            logger.error("Unable to add user")
            return self.bad_request_response(error=user_serializer.errors, description="Unable to add user")

        user_serializer.save()
        logger.info("User added successfully")
        return self.success_response(payload=user_serializer.data, description="User added successfully")


class UserDetailApiView(BaseAPIView):
    serializer_class = user.serializers.UserSerializer

    # 3. Retrieve
    def get(self, request, user_id, *args, **kwargs):
        user_instance = User.get_object(user_id)

        if not user_instance:
            logger.error("Object with user id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive user")

        user_serializer = self.serializer_class(user_instance)
        logger.info("User retreived successfully")
        return self.success_response(payload=user_serializer.data, description="User retrieved successfully")

    # 4. Update
    def put(self, request, user_id, *args, **kwargs):
        user_instance = User.get_object(user_id)

        if not user_instance:
            logger.error("Object with user id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive user")

        user_serializer = self.serializer_class(
            instance=user_instance, data=request.data, partial=True)

        if not user_serializer.is_valid():
            return self.bad_request_response(error=user_serializer.errors, description="Unable to update user")

        user_serializer.save()
        logger.info("User updated successfully")
        return self.success_response(payload=user_serializer.data, description="User updated successfully")

    # 5. Delete
    def delete(self, request, user_id, *args, **kwargs):
        user_instance = User.get_object(user_id)

        if not user_instance:
            logger.error("Object with user id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive user")

        user_instance.delete()
        logger.info("User deleted")
        return self.success_response(payload={}, description="User deleted successfully")
