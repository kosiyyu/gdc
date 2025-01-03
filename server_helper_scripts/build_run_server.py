import os
import subprocess

java_version = "21.0.5"
server_jar_path = "../server-j21.0.5/src/"
binary_filename = "server.jar"

os.chdir(server_jar_path)

def validate_java_version():
    result = subprocess.run(["java", "-version"], capture_output=True, text=True)
    
    if java_version in result.stderr:
        print("Java version is valid")
    else:
        print(f"Java version is invalid, please install Java {java_version} that is available for this server build")
        exit(1)

def build_run():

    process = subprocess.Popen(["java", "-Xmx1024M", "-Xms1024M", "-jar", binary_filename, "nogui"], text=True)

    print(f"Server started with PID: {process.pid}")


validate_java_version()
build_run()

exit(0)