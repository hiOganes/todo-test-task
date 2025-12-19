from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.common.models import BaseModel


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
