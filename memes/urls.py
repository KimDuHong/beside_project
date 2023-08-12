from django.urls import path
from .views import (
    GetUploadURL,
    Memes,
    DetailMeme,
    MemeSearchByTag,
    DetailMemeComment,
    MemesSortedVisited,
    getBlob,
)

urlpatterns = [
    path("uploadURL/", GetUploadURL.as_view()),
    path("download/", getBlob.as_view()),
    path("", Memes.as_view(), name="meme-list"),
    path("top-visited/", MemesSortedVisited.as_view()),
    path("<int:pk>/", DetailMeme.as_view()),
    path("<int:pk>/comment", DetailMemeComment.as_view()),
    path("search/tag/", MemeSearchByTag.as_view()),
]
