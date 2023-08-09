from django.urls import path
from .views import MemeFavoirtes, MyFavoirtes

urlpatterns = [
    path("meme/<int:pk>/", MemeFavoirtes.as_view()),
    path("me/", MyFavoirtes.as_view()),
]
