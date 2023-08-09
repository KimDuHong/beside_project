from django.db import models
from common.models import CommonModel


class Comment(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="comment",
    )
    meme = models.ForeignKey(
        "memes.Meme",
        on_delete=models.CASCADE,
        related_name="comment",
    )
    description = models.TextField(
        max_length=255,
    )

    def __str__(self) -> str:
        return f"{self.description}"

    class Meta:
        ordering = ["created_at"]
