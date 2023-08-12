from django.contrib import admin
from .models import Meme


@admin.register(Meme)
class MemeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "thumbnail",
        "meme_url",
        "all_tags",
        "visited",
        "favorite_count",
    )
