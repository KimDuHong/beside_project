import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .models import User
from unittest.mock import Mock, patch
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestUserProfileAPI:
    def setup_method(cls):
        cls.client = APIClient()
        cls.test_user = User.objects.create(username="TestUser")
        cls.url = reverse("self_user_profile")

    def test_view_user_profile_non_login(self):
        response = self.client.get(self.url)
        assert response.status_code == 403

    def test_view_user_profile_login_user(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.data.get("id") == self.test_user.id


@pytest.mark.django_db
class TestKakaoLoginRequest:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("kakao_login_request")

    def test_kakao_login_request(self):
        response = self.client.get(self.url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestNaverLoginRequest:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("naver_login_request")

    def test_kakao_login_request(self):
        response = self.client.get(self.url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestKakaoLogin:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("kakao_login")

    @patch("requests.post")
    @patch("requests.get")
    def test_kakao_login_request_new_user(self, mock_get, mock_post):
        url = reverse("self_user_profile")
        response = self.client.get(url)
        assert response.status_code == 403
        # Set up mock responses
        mock_post_response = Mock()
        mock_post_response.json.return_value = {"access_token": "test_token"}
        mock_post.return_value = mock_post_response

        mock_get_response = Mock()
        mock_get_response.json.return_value = {
            "kakao_account": {
                "email": "test@example.com",
                "profile": {
                    "nickname": "Test User",
                },
            },
        }
        mock_get.return_value = mock_get_response

        # Send the request
        response = self.client.post(self.url, {"code": "test_code"})

        # Check that the user was created and logged in
        user = User.objects.get(email="test@example.com")
        assert user is not None
        assert user.username == "Test User"
        assert user.sns_type == "Kakao"
        assert response.status_code == status.HTTP_201_CREATED

        url = reverse("self_user_profile")
        response = self.client.get(url)
        assert response.status_code == 200

    @patch("requests.post")
    @patch("requests.get")
    def test_kakao_login_request_existing_user(self, mock_get, mock_post):
        url = reverse("self_user_profile")
        response = self.client.get(url)
        assert response.status_code == 403
        # Create an existing user
        User.objects.create(
            email="test@example.com",
            username="Test User",
            name="Test User",
            sns_type="Kakao",
        )

        # Set up mock responses
        mock_post_response = Mock()
        mock_post_response.json.return_value = {"access_token": "test_token"}
        mock_post.return_value = mock_post_response

        mock_get_response = Mock()
        mock_get_response.json.return_value = {
            "kakao_account": {
                "email": "test@example.com",
                "profile": {
                    "nickname": "Test User",
                },
            },
        }
        mock_get.return_value = mock_get_response

        # Send the request
        response = self.client.post(self.url, {"code": "test_code"})

        # Check that the user was logged in
        assert response.status_code == status.HTTP_200_OK

        url = reverse("self_user_profile")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_kakao_login_non_field(self):
        response = self.client.post(self.url, {})
        assert User.objects.count() == 0
        assert response.status_code == 400


@pytest.mark.django_db
class TestNaverLogin:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("naver_login")

    @patch("requests.post")
    @patch("requests.get")
    def test_naver_login_request_new_user(self, mock_get, mock_post):
        url = reverse("self_user_profile")
        response = self.client.get(url)
        assert response.status_code == 403
        # Set up mock responses
        mock_post_response = Mock()
        mock_post_response.json.return_value = {"access_token": "test_token"}
        mock_post.return_value = mock_post_response

        mock_get_response = Mock()
        mock_get_response.json.return_value = {
            "resultcode": "00",
            "message": "success",
            "response": {
                "email": "test@example.com",
                "name": "Test User",
                "id": "Test User",
            },
        }
        mock_get.return_value = mock_get_response

        # Send the request
        response = self.client.post(self.url, {"code": "test_code", "state": "miimgoo"})

        # Check that the user was created and logged in
        user = User.objects.get(email="test@example.com")
        assert user is not None
        assert user.username == "Test User"
        assert user.sns_type == "Naver"
        assert response.status_code == status.HTTP_201_CREATED

        url = reverse("self_user_profile")
        response = self.client.get(url)
        assert response.status_code == 200

    @patch("requests.post")
    @patch("requests.get")
    def test_naver_login_request_existing_user(self, mock_get, mock_post):
        url = reverse("self_user_profile")
        response = self.client.get(url)
        assert response.status_code == 403
        # Create an existing user
        User.objects.create(
            email="test@example.com",
            username="Test User",
            name="Test User",
            sns_type="Naver",
        )

        # Set up mock responses
        mock_post_response = Mock()
        mock_post_response.json.return_value = {"access_token": "test_token"}
        mock_post.return_value = mock_post_response

        mock_get_response = Mock()
        mock_get_response.json.return_value = {
            "resultcode": "00",
            "message": "success",
            "response": {
                "email": "test@example.com",
                "name": "Test User",
                "id": "Test User",
            },
        }
        mock_get.return_value = mock_get_response

        # Send the request
        response = self.client.post(self.url, {"code": "test_code", "state": "miimgoo"})

        # Check that the user was logged in
        assert response.status_code == status.HTTP_200_OK

        url = reverse("self_user_profile")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_naver_login_non_field_code(self):
        response = self.client.post(self.url, {"state": "miimmgoo"})
        assert User.objects.count() == 0
        assert response.status_code == 400

    def test_naver_login_non_field_state(self):
        response = self.client.post(self.url, {"code": "test_code"})
        assert User.objects.count() == 0
        assert response.status_code == 400

    def test_naver_login_mismatch_state(self):
        response = self.client.post(
            self.url, {"code": "test_code", "state": "MISMATCH_STATE"}
        )
        assert User.objects.count() == 0
        assert response.status_code == 400


@pytest.mark.django_db
class TestLogOut:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("logout")
        self.test_user = User.objects.create(username="TestUser")
        self.client.force_login(user=self.test_user)

    def test_logout_authenticated_user(self):
        response = self.client.post(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"LogOut": True}

    def test_logout_unauthenticated_user(self):
        self.client.logout()
        response = self.client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
