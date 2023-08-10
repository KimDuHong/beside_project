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
        operation_summary="Request user info",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.PrivateUserSerializer(),
            ),
            403: "Permission denied",
        },
    )
    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Delete user",
        responses={
            200: "Success",
            403: "Permission denied",
        },
    )
    def delete(self, request):
        user = request.user
        user.delete()
        return Response("Success", 204)


class KakaoLoginRequest(APIView):
    @swagger_auto_schema(
        operation_summary="KaKao Login Request",
        responses={
            200: openapi.Response(
                description="Successful response",
                examples={
                    "application/json": {
                        "url": "https://kauth.kakao.com/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code"
                    }
                },
            ),
        },
    )
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
        operation_summary="KaKao Login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="URL parameter code in redirect URL",
            required=["code"],
            properties={
                "code": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="URL parameter code in redirect URL",
                )
            },
        ),
        responses={
            200: openapi.Response(
                description="Successful login",
            ),
            201: openapi.Response(
                description="Create user",
            ),
            400: "Bad request",
        },
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
                        "client_id": settings.KAKAO_CLIENT_ID,
                        "redirect_uri": settings.KAKAO_REDIRECT_URI,
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
                    sns_type="Kakao",
                )
            user.set_unusable_password()
            user.save()
            login(request, user)
            return Response(status=201)
        except Exception as e:
            return Response(status=400)


class NaverLoginRequest(APIView):
    @swagger_auto_schema(
        operation_summary="Naver Login Request",
        responses={
            200: openapi.Response(
                description="Successful response",
                examples={
                    "application/json": {
                        "url": "https://nid.naver.com/oauth2.0/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code"
                    }
                },
            ),
        },
    )
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
        operation_summary="Naver Login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="URL parameter code in redirect URL",
            required=["code", "state"],
            properties={
                "code": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="URL parameter code in redirect URL",
                ),
                "state": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="miimgoo",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Successful response",
            ),
            201: openapi.Response(
                description="Create user ",
            ),
            400: "Bad request",
        },
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
        operation_summary="Log out",
        operation_description="Log out a user",
        responses={200: "OK", 403: "Forbidden"},
    )
    def post(self, request):
        logout(request)
        return Response({"LogOut": True})
