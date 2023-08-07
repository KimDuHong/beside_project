from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.UserMe.as_view(), name="self_user_profile"),
    path("naver/", views.NaverLogin.as_view(), name="naver_login"),
    path(
        "naver/request", views.NaverLoginRequest.as_view(), name="naver_login_request"
    ),
    path("kakao/", views.KakaoLogin.as_view(), name="kakao_login"),
    path(
        "kakao/request", views.KakaoLoginRequest.as_view(), name="kakao_login_request"
    ),
    path("logout/", views.LogOut.as_view(), name="logout"),
]
