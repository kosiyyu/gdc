import os
import sys
import time
import psutil
from psutil import Process, Popen
import subprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from env_loader.env_loader import env

SRC_PATH = env["SRC_PATH"]
BINARY_FILENAME = env["BINARY_FILENAME"]
MAX_RUNTIME = 7200 # in seconds
# MAX_RUNTIME = 3600 # in seconds

os.chdir(SRC_PATH)

def build_run() -> Popen:
    process = subprocess.Popen(
        ["java", "-Xmx1024M", "-Xms1024M", "-jar", BINARY_FILENAME, "nogui"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        text=True,
        bufsize=1
    )
    print(f"Log: Server started with PID: {process.pid}")
    return process

def kill_process(proc: Process):
    try:
        parent = psutil.Process(proc.pid)
        children = parent.children(recursive=True)
        
        for child in children:
            child.terminate()
        
        proc.terminate()
        
        _, alive = psutil.wait_procs(children + [parent], timeout=3)
        
        for p in alive:
            p.kill()
            
    except psutil.NoSuchProcess:
        print(f"Log: Process {proc.pid} already terminated")
    except Exception as e:
        print(f"Error killing process: {e}")

def stop_server(proc: Popen):
    try:
        if proc and proc.poll() is None:
            print("Log: Sending stop command to server")
            proc.stdin.write("stop\n")
            proc.stdin.flush()
            
            for _ in range(10):
                if proc.poll() is not None:
                    print("Log: Server stopped gracefully")
                    return True
                time.sleep(1)
            
            print("Log: Server didn't stop gracefully")
            return False
    except Exception as e:
        print(f"Error stopping server: {e}")
        return False

def save_state(proc: Popen):
    try:
        if proc and proc.poll() is None:
            print("Log: Saving world state")
            proc.stdin.write("save-all\n")
            proc.stdin.flush()
            
            time.sleep(3)
            return True
    except Exception as e:
        print(f"Error saving state: {e}")
        return False

def loop(popen: Popen) -> bool:
    process_id = popen.pid
    start_time = time.time()

    while True:
        try:
            proc = psutil.Process(process_id)
            current_time = time.time()

            if current_time - start_time >= MAX_RUNTIME:
                print(f"Log: Time limit reached ({MAX_RUNTIME}s), initiating shutdown sequence")
                save_state(popen)
                stop_server(popen)

                if proc.is_running():
                    kill_process(proc)
                return False

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
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            return False

def main():
    try:
        proc = build_run()
        is_alive = loop(proc)
        if not is_alive:
            print("Process is terminated")
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        try:
            if proc.poll() is None:
                kill_process(psutil.Process(proc.pid))
        except:
            pass

if __name__ == "__main__":
    main()