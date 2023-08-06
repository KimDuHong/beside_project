from django.contrib import admin
from .models import Meme


@admin.register(Meme)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "thumbnail",
        "meme_url",
        "all_tags",
    )
