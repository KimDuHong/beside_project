from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Tag
from rest_framework.exceptions import ValidationError


class GroupTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name", "type"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {representation["type"]: representation["name"]}


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "name",
            "type",
        )
