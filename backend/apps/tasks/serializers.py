from rest_framework import serializers
from .models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': False, 'allow_blank': True},
        }


class TaskListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at']
        read_only_fields = fields


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Task.Status.choices)

    class Meta:
        model = Task
        fields = ['status']

    def validate_status(self, value):
        return value