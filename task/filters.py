import django_filters
from task.models import Task


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'title': ["in", "exact"],
            'completion_status':["in", "exact"],
            'due_date':["in", "exact"]
        }