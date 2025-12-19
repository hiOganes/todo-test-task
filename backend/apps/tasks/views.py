from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Task
from .serializers import (
    TaskListSerializer,
    TaskCreateSerializer,
    TaskStatusUpdateSerializer
)


class TaskListView(generics.ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskStatusUpdateView(generics.UpdateAPIView):
    serializer_class = TaskStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TaskListSerializer(instance).data)


class TaskDeleteView(generics.DestroyAPIView):
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj