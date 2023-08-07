from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class SNS_choices(models.TextChoices):
        Kakao = "Kakao"
        Naver = "Naver"

    name = models.CharField(
        max_length=10,
    )
    first_name = models.CharField(
        max_length=100,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
    )
    sns_type = models.CharField(
        max_length=100,
        choices=SNS_choices.choices,
    )

    def __str__(self) -> str:
        return f"{self.username}"
