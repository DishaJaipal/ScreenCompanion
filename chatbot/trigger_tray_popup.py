from plyer import notification

def show_alert(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="ScreenAssistant",
        timeout=5
    )
