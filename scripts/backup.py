#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent
env_path = project_root / "backup.env"
if not env_path.is_file():
    raise FileNotFoundError(f"Could not find {env_path}")
load_dotenv(dotenv_path=env_path)

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "")

missing = [k for k,v in (("DB_NAME", db_name), ("DB_USER", db_user), ("DB_PASSWORD", db_password)) if not v]
if missing:
    raise EnvironmentError(f"Missing environment variables in backup.env: {', '.join(missing)}")

backup_dir = project_root / "backups"
backup_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = backup_dir / f"videogames_backup_{timestamp}.sql"

command = [
    "pg_dump",
    "-U", db_user,
    "-h", db_host,
    "-d", db_name,
    "-f", str(filename),
    "--no-owner",
    "--verbose"
]
if db_port:
    command.extend(["-p", db_port])

env = os.environ.copy()
env["PGPASSWORD"] = db_password

result = subprocess.run(command, env=env)
if result.returncode != 0:
    exit(result.returncode)
