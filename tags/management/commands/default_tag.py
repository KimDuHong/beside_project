from django.core.management.base import BaseCommand
import json
from tags.models import Tag


class Command(BaseCommand):
    help = "이 커맨드를 통해 default tag 를 설정합니다."

    def handle(self, *args, **options):
        with open("./tags/default.json") as tag_data:
            tags = json.load(tag_data)
            # 'tag' 테이블이 비어있는 경우, 주어진 데이터를 삽입
        created_count = 0
        for type, names in tags.items():
            for name in names:
                _, created = Tag.objects.get_or_create(name=name, type=type)
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"{type} / {name} 태그가 생성되었습니다.")
                    )
                    created += 1
        self.stdout.write(self.style.SUCCESS(f"{created_count}개의 새로운 태그가 생성되었습니다."))
