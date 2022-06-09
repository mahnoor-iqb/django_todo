from rest_framework import serializers
from task.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'creation_date', 'due_date',
                  'completion_date', 'completion_status', 'file_attachment', 'user')