import os
import sys
import subprocess
import datetime
import threading
import termios
import tty

print("=== Simple Network Logger ===")

print("Available interfaces:\n")
subprocess.run(["sudo", "tshark", "-D"])

iface = input("\nSelect interface number: ")

print("\nPress ENTER anytime to stop the capture manually.\n")

output_file = "capture_log.txt"
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

command = [
    "sudo",
    "tshark",
    "-i", iface,
    "-T", "fields",
    "-e", "frame.number",
    "-e", "ip.src",
    "-e", "ip.dst",
    "-e", "frame.len"
]

stop_capture = False

def wait_for_enter():
    global stop_capture
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch == "\r" or ch == "\n":
                stop_capture = True
                break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

threading.Thread(target=wait_for_enter, daemon=True).start()

print("Running tshark... (press ENTER to stop)\n")

try:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    captured_lines = []

    for line in process.stdout:
        if stop_capture:
            process.terminate()
            break
        print(line.strip())
        captured_lines.append(line)

    with open(output_file, "w") as f:
        f.write("Network Capture Log\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("-------------------------------------\n")
        f.writelines(captured_lines)

    print("\nCapture stopped!")
    print(f"{len(captured_lines)} packets recorded.")
    print(f"Saved to: {os.path.abspath(output_file)}")

except FileNotFoundError:
    print("ERROR: tshark is not installed or not in PATH.")
    sys.exit(1)
