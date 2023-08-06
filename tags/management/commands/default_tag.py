from django.core.management.base import BaseCommand
import json
from tags.models import Tag


class Command(BaseCommand):
    help = "이 커맨드를 통해 default tag 를 설정합니다."

    def handle(self, *args, **options):
        if not Tag.objects.exists():
            with open("./tags/default.json") as tag_data:
                tags = json.load(tag_data)
                # 'tag' 테이블이 비어있는 경우, 주어진 데이터를 삽입
            for type, names in tags.items():
                for name in names:
                    Tag.objects.create(name=name, type=type)
        else:
            self.stdout.write(self.style.SUCCESS("태그가 이미 존재합니다."))
