from user.models import User
import user.serializers
from utils.base import BaseAPIView
from rest_framework import permissions
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password

import logging
logger = logging.getLogger('django')


class UserApiView(BaseAPIView):
    serializer_class = user.serializers.UserSerializer

    def get(self, request, *args, **kwargs):

        if not request.user.is_admin:
            return self.permission_denied_response(error="Permission denied", description="Only Admin can view other users")

        users = User.objects.all()
        user_serializer = self.serializer_class(users, many=True)
        data = user_serializer.data

        # Exclude password from response
        for i in range(len(data)):
            del data[i]['password']

        logger.info("Users retreived successfully")
        return self.success_response(payload=data, description="Ussers retreived successfully")


class UserDetailApiView(BaseAPIView):
    serializer_class = user.serializers.UserSerializer

    # Retrieve
    def get(self, request, user_id, *args, **kwargs):
        user_instance = User.get_object(user_id)

        if not user_instance:
            logger.error("Object with user id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive user")

        if user_instance.id != request.user.id:
            return self.permission_denied_response(error="Permission denied", description="You are not allowed to view other users")

        user_serializer = self.serializer_class(user_instance)
        logger.info("User retreived successfully")

        # Exclude password from response
        data = user_serializer.data
        data.pop('password')

        return self.success_response(payload=data, description="User retrieved successfully")

    # Update
    def put(self, request, user_id, *args, **kwargs):
        user_instance = User.get_object(user_id)

        if not user_instance:
            logger.error("Object with user id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive user")

        if user_instance.id != request.user.id:
            return self.permission_denied_response(error="Permission denied", description="You are not allowed to update other users")

        password = make_password(request.data.get('password'))

        user_data = {
            'email': request.data.get('email'),
            'password': password,
        }
        user_serializer = self.serializer_class(
            instance=user_instance, data=user_data, partial=True)

        if not user_serializer.is_valid():
            return self.bad_request_response(error=user_serializer.errors, description="Unable to update user")

        user_serializer.save()

        # Exclude password from response
        data = user_serializer.data
        data.pop('password')

        logger.info("User updated successfully")
        return self.success_response(payload=data, description="User updated successfully")

    # Delete
    def delete(self, request, user_id, *args, **kwargs):
        if not request.user.is_admin:
            return self.permission_denied_response(error="Permission denied", description="Only admin can delete users")
            
        user_instance = User.get_object(user_id)

        if not user_instance:
            logger.error("Object with user id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive user")

        user_instance.delete()
        logger.info("User deleted")
        return self.success_response(payload={}, description="User deleted successfully")


class SignupView(BaseAPIView):
    serializer_class = user.serializers.UserSerializer
    permission_classes = ()

    # Create
    def post(self, request, *args, **kwargs):
        password = make_password(request.data.get('password'))

        data = {
            'email': request.data.get('email'),
            'password': password,
        }

        user_serializer = self.serializer_class(data=data)

        if not user_serializer.is_valid():
            logger.error("Unable to add user")
            return self.bad_request_response(error=user_serializer.errors, description="Unable to add user")

        user_serializer.save()
        logger.info("User added successfully")
        return self.created_response(payload=user_serializer.data, description="Signup Successful!")


class LoginView(BaseAPIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return self.bad_request_response(error="User email or password provided", description="Unable to log in user")

        user_instance = User.objects.get(email=email)

        if not user_instance:
            return self.bad_request_response(error="User email does not exist", description="Unable to log in user")

        if not check_password(password, user_instance.password):
            return self.bad_request_response(error="User password does not match", description="Unable to log in user")

        # user_instance = authenticate(email=email, password=password)
        login(request, user_instance)

        return self.success_response(payload={}, description="Login successful")


class LogoutView(BaseAPIView):
    def get(self, request):
        logout(request)
        return self.success_response(payload={}, description="Logout successful")
