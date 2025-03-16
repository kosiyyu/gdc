from run import main as run
import os
import shutil
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from env_loader.env_loader import env

SRC_PATH = os.getcwd()
BINARY_FILENAME = env["BINARY_FILENAME"]

def copy_flag_to_src():
    flag_path = "/flag"
    
    if not os.path.exists(flag_path):
        print(f"No {flag_path} directory.")
        raise RuntimeError(f"No {flag_path} directory.")
    
    if not os.path.isdir(flag_path):
        print(f"{flag_path} is not a directory.")
        raise RuntimeError(f"{flag_path} is not a directory.")
    
    try:
        flag_files = os.listdir(flag_path)
        print(f"Files in {flag_path}: {flag_files}")

        for file_name in flag_files:
            source_file = os.path.join(flag_path, file_name)
            dest_file = os.path.join(SRC_PATH, file_name)
            
            if os.path.isfile(source_file):
                shutil.copy2(source_file, dest_file)
                print(f"Copied {source_file} to {dest_file}")
            elif os.path.isdir(source_file):
                shutil.copytree(source_file, dest_file)
                print(f"Copied directory {source_file} to {dest_file}")
        
        print(f"All contents copied from {flag_path} to {SRC_PATH}")
        return True
    except Exception as e:
        print(f"Error copying flag contents: {str(e)}")
        return False

binary_path = os.path.join(SRC_PATH, BINARY_FILENAME)
if os.path.exists(SRC_PATH) and os.path.isfile(binary_path):
    pass
else:
    copy_flag_to_src()

run()