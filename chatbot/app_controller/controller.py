from terminator import App
from app_controller.app_controller import APPS
from logic import get_app_for_task
import time

running_apps = {}

def launch_app(app_name):
    if app_name in APPS:
        path = APPS[app_name]
        app = App(path)
        app.launch()
        running_apps[app_name] = app
        print(f"Launched {app_name}")
    else:
        print(f"App '{app_name}' not found in config.")

def close_app(app_name):
    if app_name in running_apps:
        app = running_apps[app_name]
        app.close()  # You can also use app.kill()
        print(f"Closed {app_name}")
        del running_apps[app_name]
    else:
        print(f"App '{app_name}' not currently running.")

def main():
    while True:
        task = input("\nEnter task (write_note/calculate/browse/write_doc/exit): ")

        if task == "exit":
            print("Exiting and closing all apps...")
            for app in list(running_apps):
                close_app(app)
            break

        app_to_open = get_app_for_task(task)

        if app_to_open:
            # Close all others before launching the new one
            for app in list(running_apps):
                close_app(app)
            launch_app(app_to_open)
        else:
            print("Unknown task!")

if __name__ == "__main__":
    main()