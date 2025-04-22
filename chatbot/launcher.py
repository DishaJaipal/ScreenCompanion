import threading
from tray_app import run_tray

if __name__ == "__main__":
    tray_thread = threading.Thread(target=run_tray)
    tray_thread.start()
