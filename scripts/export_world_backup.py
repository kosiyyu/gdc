import os
import sys
import httpx
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from env_loader.env_loader import env

os.chdir(env["SRC_PATH"])

def transfer_world():
  url = os.getenv("PUSH_BACKUP_URL")

  with open("world.tar.gz", "rb") as file:
    response = httpx.put(url, data=file)
    print(response)

def main():
  try:
    transfer_world()
    print(f"Export process completed successfully.")
  except Exception as e:
    print(f"Export failed: {e}")