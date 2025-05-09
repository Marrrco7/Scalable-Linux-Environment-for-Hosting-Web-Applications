import os
import subprocess
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Backup the PostgreSQL database using pg_dump"

    def handle(self, *args, **kwargs):
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_host = db_settings.get('HOST', 'localhost')
        db_password = db_settings['PASSWORD']

        os.makedirs("backups", exist_ok=True)
        filename = f"backups/videogames_backup_{datetime.now():%Y%m%d_%H%M%S}.sql"

        command = [
            "pg_dump",
            "-U", db_user,
            "-h", db_host,
            "-d", db_name,
            "-f", filename
        ]

        env = os.environ.copy()
        env["PGPASSWORD"] = db_password

        self.stdout.write(f"Backing up to {filename}...")
        subprocess.run(command, env=env, check=True)
        self.stdout.write(self.style.SUCCESS(" Backup completed successfully!"))
