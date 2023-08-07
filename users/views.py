from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.status import HTTP_409_CONFLICT
from django.conf import settings
from . import serializers
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests


class UserMe(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="요청한 유저의 정보를 가져오는 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.PrivateUserSerializer(),
            ),
        },
    )
    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class KakaoLoginRequest(APIView):
    def get(self, request):
        kakaoParams = {
            "client_id": settings.KAKAO_CLIENT_ID,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "response_type": "code",
        }
        response = requests.get(
            "https://kauth.kakao.com/oauth/authorize",
            params=kakaoParams,
        )

        return Response({"url": response.url})


class KakaoLogin(APIView):
    @swagger_auto_schema(
        operation_summary="카카오 로그인 api",
        responses={
            200: openapi.Response(
                description="Successful response",
            ),
            201: openapi.Response(
                description="Create user",
            ),
            400: "Bad request",
        },
        manual_parameters=[
            openapi.Parameter(
                name="code",
                in_=openapi.IN_QUERY,
                description="카카오톡에서 제공해주는 code",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = (
                requests.post(
                    "https://kauth.kakao.com/oauth/token",
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    data={
                        "grant_type": "authorization_code",
                        "client_id": "69ba16ba77556c01d4a4ea9911fc06ad",
                        "redirect_uri": "https://bangsam.site/social/kakao",
                        "code": code,
                    },
                )
                .json()
                .get("access_token")
            )
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                },
            ).json()
            # print(user_data)
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                login(request, user)

                return Response(status=200)
            except:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                    gender=kakao_account.get("gender"),
                    is_kakao=True,
                )
            user.set_unusable_password()
            user.save()
            login(request, user)
            return Response(status=201)
        except Exception as e:
            return Response(status=400)


class NaverLoginRequest(APIView):
    def get(self, request):
        naverParams = {
            "client_id": settings.NAVER_CLIENT_ID,
            "redirect_uri": settings.NAVER_REDIRECT_URI,
            "response_type": "code",
            "state": "miimgoo",
        }
        response = requests.get(
            "https://nid.naver.com/oauth2.0/authorize?",
            params=naverParams,
        )

        return Response({"url": response.url})


class NaverLogin(APIView):
    @swagger_auto_schema(
        operation_summary="네이버 로그인 api",
        responses={
            200: openapi.Response(
                description="Successful response",
            ),
            201: openapi.Response(
                description="Create user ",
            ),
            400: "Bad request",
        },
        manual_parameters=[
            openapi.Parameter(
                name="code",
                in_=openapi.IN_QUERY,
                description="네이버에서 제공해주는 code",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                name="state",
                in_=openapi.IN_QUERY,
                description="miimgoo",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
    )
    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response("code is NULL", status=400)

        state = request.data.get("state")
        if not state:
            return Response("state is NULL", status=400)

        if state == "miimgoo":
            access_token = (
                requests.post(
                    "https://nid.naver.com/oauth2.0/token",
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    data={
                        "grant_type": "authorization_code",
                        "client_id": settings.NAVER_CLIENT_ID,
                        "client_secret": settings.NAVER_CLIENT_SECRET,
                        "code": code,
                        "state": state,
                    },
                )
                .json()
                .get("access_token")
            )
            user_data = requests.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={"Authorization": f"Bearer {access_token}"},
            ).json()
            if (
                user_data.get("resultcode") == "00"
                and user_data.get("message") == "success"
            ):
                response = user_data.get("response")
                try:
                    user = User.objects.get(email=response.get("email"))
                    login(request, user)
                    return Response(status=200)
                except User.DoesNotExist:
                    user = User.objects.create(
                        username=response.get("id")[:10],
                        name=response.get("name"),
                        email=response.get("email"),
                        sns_type="Naver",
                    )
                    user.set_unusable_password()
                    user.save()
                    login(request, user)
                    return Response(
                        status=201,
                    )

            return Response("code is invalid", status=400)
        else:
            raise ParseError("state is invalid")


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="로그아웃 api",
        operation_description="로그아웃",
        responses={200: "OK", 403: "Forbidden"},
    )
    def post(self, request):
        logout(request)
        return Response({"LogOut": True})
