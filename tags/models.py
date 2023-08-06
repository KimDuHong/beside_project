from django.db import models
from common.models import CommonModel
from django.core.exceptions import ValidationError


class Tag(CommonModel):
    class TypeChoices(models.TextChoices):
        SITUATION = "상황", "상황"
        EMOTION = "감정", "감정"
        CHARACTER = "인물", "인물"
        OTHER = "기타", "기타"

    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=100,
        choices=TypeChoices.choices,
    )

    class Meta:
        unique_together = (
            "name",
            "type",
        )

    def __str__(self) -> str:
        return f"{self.type} : {self.name}"
