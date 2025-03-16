import os
import sys
import shutil as sh
import datetime as dt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from env_loader.env_loader import env

os.chdir(env["SRC_PATH"])

LOG_FILENAME = env["LOG_FILENAME"]
BACKUP_DIR = env["BACKUP_DIR"]
WORLD_DIR = env["WORLD_DIR"]
SERVER_PROPERTIES_FILENAME = env["SERVER_PROPERTIES_FILENAME"]
USERCACHE_FILENAME = env["USERCACHE_FILENAME"]
BANNED_PLAYERS_FILENAME = env["BANNED_PLAYERS_FILENAME"]
BANNED_IPS_FILENAME = env["BANNED_IPS_FILENAME"]
WHITELIST_FILENAME = env["WHITELIST_FILENAME"]
OPS_FILENAME = env["OPS_FILENAME"]

CRITICAL_FILES = [SERVER_PROPERTIES_FILENAME, USERCACHE_FILENAME, LOG_FILENAME]

OPTIONAL_FILES = [
    BANNED_PLAYERS_FILENAME,
    BANNED_IPS_FILENAME,
    WHITELIST_FILENAME,
    OPS_FILENAME,
]

print(BACKUP_DIR, WORLD_DIR)

def create_log():
    date_string = str(dt.datetime.now().timestamp()).replace(".", "")
    with open(LOG_FILENAME, "w") as file:
        file.write(date_string)

def create_targz():
    if not os.path.exists(WORLD_DIR):
        raise FileNotFoundError(f"ERROR: World folder '{WORLD_DIR}' does not exist.")
    
    if os.path.exists(BACKUP_DIR):
        raise RuntimeError(f"ERROR: Pre-archive folder '{BACKUP_DIR}' already exists.")
    
    os.mkdir(BACKUP_DIR)
    sh.copytree(WORLD_DIR, os.path.join(BACKUP_DIR, WORLD_DIR))

    for filename in CRITICAL_FILES:
        if os.path.exists(filename):
            sh.copy2(filename, BACKUP_DIR)
        else:
            raise FileNotFoundError(f"ERROR: Critical file '{filename}' is missing.")

    for filename in OPTIONAL_FILES:
        if os.path.exists(filename):
            sh.copy2(filename, BACKUP_DIR)
        else:
            print(f"WARNING: Optional file '{filename}' is missing, skipping.")

    # root_dir refers to base directory of output file, or working directory for your working script.
    # base_dir refers to content you want pack.
    sh.make_archive(base_name=BACKUP_DIR, format="gztar", root_dir=".", base_dir=BACKUP_DIR)

def cleanup():
    os.remove(LOG_FILENAME)
    sh.rmtree(BACKUP_DIR)

def main():
    try:
        create_log()
        create_targz()
        cleanup()
        print("Backup process completed successfully.")
    except Exception as e:
        print(f"Backup failed: {e}")

if __name__ == "__main__":
    main()
