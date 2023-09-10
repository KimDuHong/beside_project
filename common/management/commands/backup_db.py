from django.core.management.base import BaseCommand
from memes import s3_connect
from django.core import management
from datetime import datetime


class Command(BaseCommand):
    help = "DB 백업 후 S3 저장"

    def handle(self, *args, **options):
        now = datetime.now().strftime("%Y%m%d")
        backup_file = f"./backup/{now}_db_backup.json"
        management.call_command(
            "dumpdata",
            "--exclude",
            "auth.permission",
            "--exclude",
            "contenttypes",
            "--indent",
            "4",
            output=backup_file,
        )

        s3 = s3_connect.connect_s3()
        s3.upload_file(backup_file, "miimgoo", backup_file)

        self.stdout.write(
            self.style.SUCCESS("Successfully backed up and uploaded database to S3")
        )
