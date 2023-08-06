from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "pk",
            "name",
            "type",
        )
