import os
import subprocess
from datetime import datetime


from dotenv import load_dotenv
load_dotenv("../credentials.env")

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_host = os.getenv("DB_HOST", "localhost")
backup_dir = "../backups"
os.makedirs(backup_dir, exist_ok=True)

filename = f"{backup_dir}/videogames_backup_{datetime.now():%Y%m%d_%H%M%S}.sql"

command = [
    "pg_dump",
    "-U", db_user,
    "-h", db_host,
    "-d", db_name,
    "-f", filename
]


env = os.environ.copy()
env["PGPASSWORD"] = os.getenv("DB_PASSWORD")

print(f"🔁 Running backup to: {filename}")
subprocess.run(command, env=env, check=True)
print("✅ Backup complete!")
