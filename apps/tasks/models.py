from django.db import models

from apps.common.models import BaseModel
from apps.accounts.models import User


class Task(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Не выполнена'
        COMPLETED = 'completed', 'Выполнена'

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(choices=Status.choices, default=Status.PENDING)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='tasks')

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
