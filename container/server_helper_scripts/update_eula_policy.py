import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from env_loader.env_loader import env

os.chdir(env["SRC_PATH"])

EULA_FILENAME = env["EULA_FILENAME"]

def update_eula_policy():
    file = open(EULA_FILENAME, "r+")
    lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("#"):
            continue
        if line.startswith("eula=false"):
            lines[i] = "eula=true\n"

            file.seek(0)
            file.truncate()
            file.seek(0)
            file.writelines(lines)
            
            print("Log: Eula property changed to true.")
            break
        elif line.startswith("eula=true"):
            print("Log: Eula property is already set to true")
            break
        else:
            print("Log: Eula property is invalid")
            break

def main():
    try:
        update_eula_policy()
        print(f"Update process completed successfully.")
    except RuntimeError as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    main()
