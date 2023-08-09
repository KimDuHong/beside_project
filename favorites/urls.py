from django.urls import path
from .views import MemeFavoirtes

urlpatterns = [
    path("meme/<int:pk>/", MemeFavoirtes.as_view()),
]
