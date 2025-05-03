import os
import subprocess
import platform

def get_app_for_task(task):
    """
    Maps a user-defined task to a system application name.
    Modify based on your OS.
    """
    task_app_map = {
        "write_note": "notepad" if platform.system() == "Windows" else "gedit",
        "calculate": "calc" if platform.system() == "Windows" else "gnome-calculator",
        "browse": "chrome" if platform.system() == "Windows" else "google-chrome",
        "write_doc": "write" if platform.system() == "Windows" else "libreoffice"
    }
    return task_app_map.get(task, None)

def launch_app_for_task(task):
    """
    Launches the corresponding application for a given task.
    """
    app = get_app_for_task(task)
    if app:
        try:
            subprocess.Popen(app, shell=True)
            return f"Launched {app} for task: {task}"
        except Exception as e:
            return f"Failed to launch {app}: {e}"
    else:
        return f"No application mapped for task: {task}"
