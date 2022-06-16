from rest_framework import serializers
from user.models import User
from django.contrib.auth.hashers import check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'is_admin', 'is_active', 'is_staff', 'is_superuser')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=500)

    def validate(self, data):
    
        email = data.get("email", None)
        password = data.get("password", None)

        if not email or not password:
            raise serializers.ValidationError("Email or password missing")

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with provided email not found.'
            )

        if not check_password(password, user.password):
            raise serializers.ValidationError(
                'Invalid Password'
            )

        return user