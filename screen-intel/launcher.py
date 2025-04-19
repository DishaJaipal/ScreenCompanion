import threading
import subprocess
import os

# Get full absolute path
base_path = os.path.dirname(os.path.abspath(__file__))

def run_gui():
    subprocess.run(["python", os.path.join(base_path, "gui.py")])

def run_capture():
    subprocess.run(["python", os.path.join(base_path, "capture.py")])

# Launch both
threading.Thread(target=run_gui).start()
threading.Thread(target=run_capture).start()
