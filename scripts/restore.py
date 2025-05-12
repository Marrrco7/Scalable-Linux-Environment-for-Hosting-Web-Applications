#!/usr/bin/env python3
import os
import subprocess
import glob
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

project_root = Path(__file__).resolve().parent.parent
env_path = project_root / "backup.env"
if not env_path.is_file():
    raise FileNotFoundError(f"Could not find {env_path}")
load_dotenv(dotenv_path=env_path)

db_name   = os.getenv("DB_NAME")
db_user   = os.getenv("DB_USER")
db_pass   = os.getenv("DB_PASSWORD")
db_host   = os.getenv("DB_HOST", "localhost")
db_port   = os.getenv("DB_PORT", "")

missing = [k for k,v in (("DB_NAME",db_name),("DB_USER",db_user),("DB_PASSWORD",db_pass)) if not v]
if missing:
    raise EnvironmentError(f"Missing {', '.join(missing)} in backup.env")

backups_dir = project_root / "backups"
sql_files = sorted(backups_dir.glob("videogames_backup_*.sql"))
if not sql_files:
    raise FileNotFoundError("No backups found in backups/")

latest = sql_files[-1]
test_db = f"{db_name}_restore_test"

env = os.environ.copy()
env["PGPASSWORD"] = db_pass


cmd = ["createdb", "-U", db_user, "-h", db_host]
if db_port:
    cmd += ["-p", db_port]
cmd.append(test_db)
subprocess.run(cmd, env=env, check=True)


cmd = ["psql", "-U", db_user, "-h", db_host, "-d", test_db, "-f", str(latest)]
if db_port:
    cmd += ["-p", db_port]
subprocess.run(cmd, env=env, check=True)


canary = [
    "psql", "-U", db_user, "-h", db_host, "-d", test_db,
    "-t", "-c",
    "SELECT COUNT(*) FROM public.videogames_register_videogame;"
]
if db_port:
    canary += ["-p", db_port]
result = subprocess.run(canary, env=env, check=True, stdout=subprocess.PIPE, text=True)
count = result.stdout.strip()
print(f" check: {count} rows in videogames_register_videogame")


# cmd = ["dropdb", "-U", db_user, "-h", db_host]
# if db_port:
#     cmd += ["-p", db_port]
# cmd.append(test_db)
# subprocess.run(cmd, env=env, check=True)
# print("Restore test succeeded and test database dropped.")
