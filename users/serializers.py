from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "name",
        )


class PrivateUserSerializer(ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        exclude = (
            "first_name",
            "last_name",
            "last_login",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )
