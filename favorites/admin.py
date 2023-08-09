from django.contrib import admin
from .models import Favoirte_meme


@admin.register(Favoirte_meme)
class Favoirte_meme_Admin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "meme",
    )
