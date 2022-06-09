from django.db import models
from user.models import User

class Task(models.Model):
    class Meta:
        db_table = 'tasks'

    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    completion_date = models.DateTimeField()
    completion_status = models.BooleanField(default=False)

    file_attachment = models.CharField(max_length=500)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
