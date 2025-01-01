import os
import shutil as sh
import datetime as dt

SRC_PATH = "../server-j21.0.5/src/"

os.chdir(SRC_PATH)

LOG_NAME = "world_backup.log"
PRE_ARCHIVE_NAME = "world_backup"

WORLD_FOLDER_FILENAME = "world"
SERVER_PROPERTIES_FILENAME = "server.properties"
USERCACHE_FILENAME = "usercache.json"

BANNED_PLAYERS_FILENAME = "banned-players.json"
BANNED_IPS_FILENAME = "banned-ips.json"
WHITELIST_FILENAME = "whitelist.json"
OPS_FILENAME = "ops.json"

CRITICAL_FILES = [SERVER_PROPERTIES_FILENAME, USERCACHE_FILENAME, LOG_NAME]

OPTIONAL_FILES = [
    BANNED_PLAYERS_FILENAME,
    BANNED_IPS_FILENAME,
    WHITELIST_FILENAME,
    OPS_FILENAME,
]

def create_log():
    date_string = str(dt.datetime.now().timestamp()).replace(".", "")
    with open(LOG_NAME, "w") as file:
        file.write(date_string)

def create_targz():
    if not os.path.exists(WORLD_FOLDER_FILENAME):
        raise FileNotFoundError(f"ERROR: World folder '{WORLD_FOLDER_FILENAME}' does not exist.")
    
    if os.path.exists(PRE_ARCHIVE_NAME):
        raise RuntimeError(f"ERROR: Pre-archive folder '{PRE_ARCHIVE_NAME}' already exists.")
    os.mkdir(PRE_ARCHIVE_NAME)

    sh.copytree(WORLD_FOLDER_FILENAME, os.path.join(PRE_ARCHIVE_NAME, WORLD_FOLDER_FILENAME))

    for filename in CRITICAL_FILES:
        if os.path.exists(filename):
            sh.copy2(filename, PRE_ARCHIVE_NAME)
        else:
            raise FileNotFoundError(f"ERROR: Critical file '{filename}' is missing.")

    for filename in OPTIONAL_FILES:
        if os.path.exists(filename):
            sh.copy2(filename, PRE_ARCHIVE_NAME)
        else:
            print(f"WARNING: Optional file '{filename}' is missing, skipping.")

    # root_dir refers to base directory of output file, or working directory for your working script.
    # base_dir refers to content you want pack.
    sh.make_archive(base_name=PRE_ARCHIVE_NAME, format="gztar", root_dir=".", base_dir=PRE_ARCHIVE_NAME)

def cleanup():
    os.remove(LOG_NAME)
    sh.rmtree(PRE_ARCHIVE_NAME)

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
