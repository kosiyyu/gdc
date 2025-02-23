import os
import sys
import time
import psutil
import subprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from env_loader.env_loader import env

SRC_PATH = env["SRC_PATH"]
BINARY_FILENAME = env["BINARY_FILENAME"]

os.chdir(SRC_PATH)

def build_run() -> int:
    process = subprocess.Popen(["java", "-Xmx1024M", "-Xms1024M", "-jar", BINARY_FILENAME, "nogui"], preexec_fn=os.setsid, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL  )
    print(f"Log: Server started with PID: {process.pid}")

    return process.pid

def loop(process_id: int) -> bool:
    while True:
        try:
            proc = psutil.Process(process_id)
            if proc.status() == psutil.STATUS_ZOMBIE:
                print(f"Log: Process {process_id} is a zombie. Exiting loop.")
                return False
            if proc.is_running():
                time.sleep(1)
                continue
            else:
                print(f"Log: Process {process_id} is no longer running.")
                return False
        except psutil.NoSuchProcess:
            print(f"Error: Process {process_id} does not exist.")
            return False

def main():
    proccess_id = build_run()
    is_allive = loop(proccess_id)
    if not is_allive:
        print("Proccess is killed")

if __name__ == "__main__":
    main()