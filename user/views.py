from user.models import User
from utils.base import BaseAPIView
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password
from user.permissions import IsUserAdmin, IsInstanceOwner
from django.db.models import Q
from user.serializers import UserSerializer, UserLoginSerializer

import logging
logger = logging.getLogger('django')

class AdminView(BaseAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsUserAdmin]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        user_serializer = self.serializer_class(users, many=True)
        logger.info("Users retreived successfully")
        return self.success_response(payload=user_serializer.data, description="Ussers retreived successfully")


class AdminDetailView(BaseAPIView):
    permission_classes = [IsUserAdmin]

    # Delete
    def delete(self, request, user_id, *args, **kwargs):
        user_instance = User.get_object(Q(id=user_id))

        if not user_instance:
            logger.error("Object with user id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive user")

        user_instance.delete()
        logger.info("User deleted")
        return self.success_response(payload={}, description="User deleted successfully")


class UserDetailView(BaseAPIView):
    permission_classes = [IsInstanceOwner]
    serializer_class = UserSerializer
    
    # Retrieve
    def get(self, request, user_id, *args, **kwargs):
        
        user_instance = User.get_object(Q(id=user_id))

        if not user_instance:
            logger.error("Object with user id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive user")

        self.check_object_permissions(request, user_instance)
        user_serializer = self.serializer_class(user_instance)
        logger.info("User retreived successfully")

        return self.success_response(payload=user_serializer.data, description="User retrieved successfully")

    # Update
    def put(self, request, user_id, *args, **kwargs):
        user_instance = User.get_object(Q(id=user_id))

        if not user_instance:
            logger.error("Object with user id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive user")

        self.check_object_permissions(request, user_instance)
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

        logger.info("User updated successfully")
        return self.success_response(payload=user_serializer.data, description="User updated successfully")


class SignupView(BaseAPIView):
    permission_classes = ()
    serializer_class = UserSerializer

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
    serializer_class = UserLoginSerializer

    def post(self, request):
        login_serializer = self.serializer_class(data=request.data)

        if not login_serializer.is_valid():
            return self.bad_request_response(error=login_serializer.errors, description="Unable to log in user")

        user_instance = User.objects.get(email=request.data.get("email"))
        login(request, user_instance)
        return self.success_response(payload={}, description="Login successful")


class LogoutView(BaseAPIView):
    def get(self, request):
        logout(request)
        return self.success_response(payload={}, description="Logout successful")
