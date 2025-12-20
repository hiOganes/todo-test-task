from drf_spectacular.utils import OpenApiParameter, OpenApiTypes
from drf_spectacular.openapi import OpenApiResponse

from apps.tasks.serializers import (
    TaskListSerializer, TaskCreateSerializer, TaskStatusUpdateSerializer
)
from apps.tasks.models import Task



tasks_tags = ['Tasks']

tasks_list_get_schema = {
    'tags': tasks_tags,
    'summary': 'This endpoint returns list user tasks',
    'responses': {200: TaskListSerializer},
}

tasks_create_schema = {
    'tags': tasks_tags,
    'summary': 'This endpoint creates a new tasks',
    'description': '''This point accepts tasks title and description, 
    and create new task''',
    'request': TaskCreateSerializer,
    'responses': {201: TaskCreateSerializer},
}

tasks_delete_schema = {
    'tags': tasks_tags,
    'summary': 'This endpoint deletes tasks',
    'request':None,
    'responses': {
            204: OpenApiResponse(description='Task deleted'),
        }
}

tasks_patch_schema = {
    'tags': tasks_tags,
    'summary': 'This endpoint change status tasks',
    'description': f'Select task id and one of these statuses: '
                   f'{Task.Status.choices}',
    'responses': {200: TaskStatusUpdateSerializer},
    'request': TaskStatusUpdateSerializer,
}
