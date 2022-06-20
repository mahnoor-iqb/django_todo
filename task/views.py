from task.models import Task
from utils.base import BaseAPIView
from django_filters.rest_framework import DjangoFilterBackend
from task.filters import TaskFilter
from django.db.models import Q
from task.serializers import TaskSerializer

import logging
logger = logging.getLogger('django')


class TaskApiView(BaseAPIView):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    # 1. List all
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.select_related('user').filter(user=request.user.id).order_by('due_date').all()

        filtered_tasks = self.filterset_class(request.GET, queryset=tasks)

        paginated = self.paginate_queryset(request, filtered_tasks.qs)
        task_serializer = self.serializer_class(paginated, many=True)

        logger.info("Tasks retreived successfully")
        return self.success_response(payload=task_serializer.data, description="Tasks retreived successfully")

    # 2. Create
    def post(self, request, *args, **kwargs):
        
        task_data = {
            'title': request.data.get('title'), 
            'description': request.data.get('description'), 
            'creation_date': request.data.get('creation_date'), 
            'due_date': request.data.get('due_date'),
            'completion_date':request.data.get('completion_date'),
            'completion_status:':request.data.get('completion_status'),
            'file_attachment':request.data.get('file_attachment'),
            'user': request.user.id
        }

        task_serializer = self.serializer_class(data=task_data)

        if not task_serializer.is_valid():
            logger.error("Unable to add task")
            return self.bad_request_response(error=task_serializer.errors, description="Unable to add task")

        task_serializer.save()
        logger.info("Task added successfully")
        return self.created_response(payload=task_serializer.data, description="Task added successfully")


class TaskDetailApiView(BaseAPIView):
    serializer_class = TaskSerializer

    # 3. Retrieve
    def get(self, request, task_id, *args, **kwargs):
        task_instance = Task.get_object(Q(id=task_id) & Q(user=request.user.id))

        if not task_instance:
            logger.error("Object with task id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive task")

        task_serializer = self.serializer_class(task_instance)
        logger.info("Task retreived successfully")
        return self.success_response(payload=task_serializer.data, description="Task retrieved successfully")

    # 4. Update
    def put(self, request, task_id, *args, **kwargs):
        task_instance = Task.get_object(Q(id=task_id) & Q(user=request.user.id))

        if not task_instance:
            logger.error("Object with task id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive task")

        task_serializer = self.serializer_class(
            instance=task_instance, data=request.data, partial=True)

        if not task_serializer.is_valid():
            return self.bad_request_response(error=task_serializer.errors, description="Unable to update task")

        task_serializer.save()
        logger.info("Task updated successfully")
        return self.success_response(payload=task_serializer.data, description="Task updated successfully")

    # 5. Delete
    def delete(self, request, task_id, *args, **kwargs):
        task_instance = Task.get_object(Q(id=task_id) & Q(user=request.user.id))

        if not task_instance:
            logger.error("Object with task id does not exist")
            return self.bad_request_response(error="Object with provided id does not exist", description="Unable to retreive task")

        task_instance.delete()
        logger.info("Task Deleted")
        return self.success_response(payload={}, description="Task deleted successfully")
