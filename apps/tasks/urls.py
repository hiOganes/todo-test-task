from django.urls import path
from .views import (
    TaskListView,
    TaskCreateView,
    TaskStatusUpdateView,
    TaskDeleteView,
)


app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/status/', TaskStatusUpdateView.as_view(), name='task-status-update'),
    path('<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
]