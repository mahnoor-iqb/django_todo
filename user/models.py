from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager


class User(AbstractBaseUser):

    class Meta:
        db_table = 'users'
        

    id = models.AutoField(primary_key = True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=500)  
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    def get_object(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
