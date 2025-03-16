import os
import sys
import shutil as sh
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from env_loader.env_loader import env

BACKUP_FILENAME = env["BACKUP_FILENAME"]
LOG_PATH = os.path.join(env["BACKUP_FILENAME"], env["LOG_FILENAME"])
BACKUP_DIR = env["BACKUP_DIR"]

os.chdir(env["SRC_PATH"])

def extract():
    if not os.path.exists(BACKUP_FILENAME):
        raise RuntimeError(f"Error: Backup file: {BACKUP_FILENAME} could not been found.")

    sh.unpack_archive(filename=BACKUP_FILENAME, format="gztar", extract_dir=".")

    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    for item in os.listdir(BACKUP_DIR):
        src_path = os.path.join(BACKUP_DIR, item)
        dest_path = os.path.join(".", item)

        if os.path.exists(dest_path):
            if os.path.isfile(dest_path):
                print("FILE", dest_path, src_path)
                os.remove(dest_path)
            elif os.path.isdir(dest_path):
                print("DIR", dest_path, src_path)
                sh.rmtree(dest_path)
            else:
                raise RuntimeError(f"Error: Unknown file type on path {dest_path}")
        
        sh.move(src_path, dest_path)

def cleanup():
    if not os.path.exists(BACKUP_DIR) or not os.path.exists(BACKUP_FILENAME):
        raise RuntimeError(f"Error: Cleanup failed.")

    # This directory should be empty
    os.rmdir(BACKUP_DIR)
    os.remove(BACKUP_FILENAME)
    


def main():
    try:
        extract()
        cleanup()
        print(f"Extraction process completed successfully.")
    except Exception as e:
        print(f"Extraction failed: {e}")

if __name__ == "__main__":
    main()
