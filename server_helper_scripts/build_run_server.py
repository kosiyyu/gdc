import os
import subprocess
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from env_loader.env_loader import env

JAVA_VERSION = env["JAVA_VERSION"]
SRC_PATH = env["SRC_PATH"]
BINARY_FILENAME = env["BINARY_FILENAME"]

os.chdir(SRC_PATH)

def validate_java_version():
    result = subprocess.run(["java", "-version"], capture_output=True, text=True)
    
    if JAVA_VERSION in result.stderr:
        print("Java version is valid")
    else:
        print(f"Java version is invalid, please install Java {JAVA_VERSION} that is available for this server build")
        exit(1)

def build_run():

    process = subprocess.Popen(["java", "-Xmx1024M", "-Xms1024M", "-jar", BINARY_FILENAME, "nogui"], text=True)

    print(f"Server started with PID: {process.pid}")


validate_java_version()
build_run()

exit(0)