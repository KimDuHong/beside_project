from django.db import models
from common.models import CommonModel
from django.core.exceptions import ValidationError


class Favoirte_meme(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    meme = models.ForeignKey(
        "memes.Meme",
        on_delete=models.CASCADE,
        related_name="favoirte_meme",
    )

    class Meta:
        unique_together = ("user", "meme")

    def __str__(self) -> str:
        return f"{self.user} / {self.meme}"
