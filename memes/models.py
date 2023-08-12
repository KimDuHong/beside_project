from django.db import models
from common.models import CommonModel
from tags.models import Tag
from PIL import Image
import imageio
import requests
from io import BytesIO
from .s3_connect import connect_s3, presigned_s3_view
from uuid import uuid4
from favorites.models import Favoirte_meme


class Meme(CommonModel):
    title = models.CharField(max_length=100)
    thumbnail = models.URLField(editable=False)
    meme_url = models.URLField()
    tags = models.ManyToManyField(Tag, related_name="tags")
    visited = models.PositiveIntegerField(
        editable=False,
        default=0,
    )

    @property
    def favorites(self):
        return self.favoirte_meme.count()

    @property
    def all_tags(self):
        return self.tags.all()

    @property
    def favorite_count(self):
        return Favoirte_meme.objects.filter(meme=self).count()

    def save(self, *args, **kwargs):
        s3 = connect_s3()
        filename = self.meme_url.split("https://kr.object.ncloudstorage.com/miimgoo/")[
            -1
        ]
        if filename[-4:] == ".gif":
            signed_url = presigned_s3_view(filename)
            response = requests.get(signed_url)
            gif = imageio.mimread(BytesIO(response.content))
            first_frame = Image.fromarray(gif[0])

            # 첫 번째 프레임을 임시 파일에 저장
            temp_file = BytesIO()
            first_frame.save(temp_file, format="JPEG")
            # 임시 파일을 NCP Object Storage에 업로드
            temp_file.seek(0)
            filename = filename.split("/data/")[-1][:-4]
            file_name = f"memes/thumbnails/{uuid4()}.jpg"

            s3.upload_fileobj(temp_file, "miimgoo", file_name)

            # thumbnail 필드에 NCP Object Storage URL 저장
            self.thumbnail = f"https://kr.object.ncloudstorage.com/miimgoo/{file_name}"
        else:
            self.thumbnail = self.meme_url

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title}"
