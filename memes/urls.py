from django.urls import path
from .views import GetUploadURL, Memes

urlpatterns = [
    path("uploadURL/", GetUploadURL.as_view()),
    path("", Memes.as_view()),
]
