from django.urls import path
from .views import GetUploadURL, Memes, DetailMeme

urlpatterns = [
    path("uploadURL/", GetUploadURL.as_view()),
    path("", Memes.as_view()),
    path("<int:pk>", DetailMeme.as_view()),
]
