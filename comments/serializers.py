from rest_framework.serializers import ModelSerializer
from .models import Comment
from users.serializers import TinyUserSerializer


class CommentSerializer(ModelSerializer):
    user = TinyUserSerializer

    class Meta:
        model = Comment
        fields = (
            "pk",
            "created_at",
            "updated_at",
            "description",
            "user",
        )
