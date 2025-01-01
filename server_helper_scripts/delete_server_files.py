import os
import shutil as sh

SRC_PATH = "../server-j21.0.5/src/"

os.chdir(SRC_PATH)

def delete_server_files():
    file_list = os.listdir()

    for item in file_list:
        if item.endswith(".jar") or item == "eula.txt":
            print(f"Log: Skipping file {item}.")
            continue
        
        if os.path.isdir(item):
            sh.rmtree(item)
            print(f"Log: Directory {item} deleted.")
        elif os.path.islink(item):
            os.remove(item)
            print(f"Log: Symbolic link {item} deleted.")
        elif os.path.isfile(item):
            os.remove(item)
            print(f"Log: File {item} deleted.")
        else:
            raise RuntimeError(f"Error: Unknown file type on path {item}")
            
def main():
    try:
        delete_server_files()
        print(f"File deletion process completed successfully.")
    except Exception as e:
        print(f"File deletion failed: {e}")

if __name__ == "__main__":
    main()


