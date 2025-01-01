import os
import shutil as sh

BACKUP_FILENAME = "world_backup.tar.gz"
OUT_DIR = "world_backup"
LOG_FILENAME = "world_backup/world_backup.log"
SRC_PATH = "../server-j21.0.5/src/"

os.chdir(SRC_PATH)

def extract():
    if not os.path.exists(BACKUP_FILENAME):
        raise RuntimeError(f"Error: Backup file: {BACKUP_FILENAME} could not been found.")

    sh.unpack_archive(filename=BACKUP_FILENAME, format="gztar", extract_dir=".")

    if os.path.exists(LOG_FILENAME):
        os.remove(LOG_FILENAME)

    for item in os.listdir(OUT_DIR):
        src_path = os.path.join(OUT_DIR, item)
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
    if not os.path.exists(OUT_DIR) or not os.path.exists(BACKUP_FILENAME):
        raise RuntimeError(f"Error: Cleanup failed.")

    # This directory should be empty
    os.rmdir(OUT_DIR)
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
