from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse, urlunparse
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from .models import Meme
from tags.models import Tag
from tags.serializers import TagSerializer
from comments.serializers import CommentSerializer
from favorites.models import Favoirte_meme


class MemeSerializer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Meme
        fields = (
            "pk",
            "title",
            "thumbnail",
            "meme_url",
            "tags",
            "visited",
            "favorites",
            "is_favorite",
        )

    def get_is_favorite(self, data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Favoirte_meme.objects.filter(user=request.user, meme=data).exists()
        return False

    def validate_tags(self, tags):
        if isinstance(tags, list):
            return True
        else:
            raise ValidationError("Tags must be a list")

    def create(self, validated_data):
        with atomic():
            tags_data = validated_data.pop("tags", [])
            if not tags_data:
                raise ValidationError("Tags is required")
            self.validate_tags(tags_data)

            url = validated_data.pop("meme_url")
            parsed_url = urlparse(url)
            cleaned_url = urlunparse(parsed_url._replace(query=""))
            validated_data["meme_url"] = cleaned_url

            meme = Meme.objects.create(**validated_data)

            for tag_data in tags_data:
                tag = get_object_or_404(Tag, name=tag_data)
                meme.tags.add(tag)

            return meme


class MemeDetailSerailizer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    comment = CommentSerializer(read_only=True, many=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Meme
        fields = (
            "pk",
            "tags",
            "title",
            "meme_url",
            "visited",
            "is_favorite",
            "comment",
            "created_at",
            "updated_at",
        )

    def get_is_favorite(self, data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Favoirte_meme.objects.filter(user=request.user, meme=data).exists()
        return False
