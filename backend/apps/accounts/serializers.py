from rest_framework import serializers
from django.core.exceptions import ValidationError

from apps.accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email exists", code=400)
        return value

    def validate_password(self, value):
        if len(value) <= 5:
            raise ValidationError("Short password", code=400)
        return value
