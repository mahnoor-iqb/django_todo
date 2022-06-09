from django.db import models

# Create your models here.

class User(models.Model):
    class Meta:
        db_table = 'users'

    id = models.AutoField(primary_key = True)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=500)  
