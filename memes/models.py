from django.db import models
from common.models import CommonModel
from django.db.models import Count
from django.core.exceptions import ValidationError


class Feed(CommonModel):
    thumbnail = models.URLField()
    meme_gif = models.URLField()

    @property
    def thumbnail(self):
        image = self.images.first()
        if image:
            return image.url
        else:
            return None

    def clean(self):
        super().clean()
        if self.category.group != self.group:
            raise ValidationError("그룹의 카테고리 내에서 선택해주세요.")
