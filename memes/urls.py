from django.urls import path
from .views import GetUploadURL, Memes, DetailMeme, MemeSearchByTag

urlpatterns = [
    path("uploadURL/", GetUploadURL.as_view()),
    path("", Memes.as_view(), name="meme-list"),
    path("<int:pk>/", DetailMeme.as_view()),
    path("search/tag/", MemeSearchByTag.as_view()),
]
