from django.urls import path
from .views import GetUploadURL

urlpatterns = [
    path("uploadURL", GetUploadURL.as_view()),
]
