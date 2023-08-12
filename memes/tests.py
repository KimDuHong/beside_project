import pytest
from rest_framework.test import APIClient
from .models import Meme, Tag
from .serializers import MemeSerializer
import json
from django.urls import reverse


@pytest.fixture
def test_meme_data_jpg():
    return {
        "title": "Test Meme",
        "meme_url": "https://example.com/test.jpg",
        "tags": {"circum": ["위로"]},
    }


@pytest.fixture
def test_meme_data_gif():
    return {
        "title": "Test Meme",
        "meme_url": "https://kr.object.ncloudstorage.com/miimgoo/memes/data/test.gif",
        "tags": {"circum": ["위로"]},
    }


@pytest.fixture
def test_meme_data_non_title():
    return {
        "meme_url": "https://kr.object.ncloudstorage.com/miimgoo/memes/gif/test.gif",
        "tags": {"circum": ["위로"]},
    }


@pytest.fixture
def test_meme_data_non_url():
    return {
        "title": "Test Meme",
        "tags": {"circum": ["위로"]},
    }


@pytest.fixture
def test_meme_data_non_tags():
    return {
        "title": "Test Meme",
        "meme_url": "https://kr.object.ncloudstorage.com/miimgoo/memes/gif/test.gif",
    }


@pytest.fixture
def create_test_tags():
    with open("./tags/default.json") as f:
        data = json.load(f)
    for tag_type, tag_names in data.items():
        for name in tag_names:
            Tag.objects.create(name=name, type=tag_type)


@pytest.mark.django_db
class TestMemeAPI:
    def setup_method(cls):
        cls.client = APIClient()
        cls.url = reverse("meme-list")

    def test_create_meme_jpg(
        self,
        test_meme_data_jpg,
        create_test_tags,
    ):
        response = self.client.post(self.url, test_meme_data_jpg, format="json")
        assert response.status_code == 201
        assert Meme.objects.count() == 1
        assert Meme.objects.get().title == test_meme_data_jpg["title"]
        assert Meme.objects.get().meme_url == Meme.objects.get().thumbnail

    def test_create_meme_gif(
        self,
        test_meme_data_gif,
        create_test_tags,
    ):
        response = self.client.post(self.url, test_meme_data_gif, format="json")
        assert response.status_code == 201
        assert Meme.objects.count() == 1
        assert Meme.objects.get().title == test_meme_data_gif["title"]
        assert Meme.objects.get().meme_url != Meme.objects.get().thumbnail

    def test_create_non_field_title(
        self,
        test_meme_data_non_title,
        create_test_tags,
    ):
        response = self.client.post(self.url, test_meme_data_non_title, format="json")
        assert response.status_code == 400
        assert Meme.objects.count() == 0

    def test_create_non_field_url(
        self,
        test_meme_data_non_url,
        create_test_tags,
    ):
        response = self.client.post(self.url, test_meme_data_non_url, format="json")
        assert response.status_code == 400
        assert Meme.objects.count() == 0

    def test_create_non_field_tags(
        self,
        test_meme_data_non_tags,
        create_test_tags,
    ):
        response = self.client.post(self.url, test_meme_data_non_tags, format="json")
        assert response.status_code == 400
        assert Meme.objects.count() == 0
