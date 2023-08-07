from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.UserMe.as_view()),
    path("naver/", views.NaverLogin.as_view()),
    path("naver/request", views.NaverLoginRequest.as_view()),
    path("kakao/", views.KakaoLogin.as_view()),
    path("kakao/request", views.KakaoLoginRequest.as_view()),
    path("logout/", views.LogOut.as_view()),
]
