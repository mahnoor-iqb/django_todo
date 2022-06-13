from rest_framework import serializers
from user.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'is_admin', 'is_active', 'is_staff', 'is_superuser')
