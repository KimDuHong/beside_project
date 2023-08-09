from rest_framework.serializers import ModelSerializer
from .models import Favoirte_meme
from memes.serializers import MemeSerializer


class FavoriteMemeSerializer(ModelSerializer):
    meme = MemeSerializer(read_only=True)

    class Meta:
        model = Favoirte_meme
        fields = ("meme",)
