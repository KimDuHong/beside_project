from django.urls import path
from .views import TagDetailVeiw, AllTagView

urlpatterns = [
    path("", AllTagView.as_view()),
    path("<int:pk>/", TagDetailVeiw.as_view()),
]
