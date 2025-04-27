<<<<<<< HEAD
from plyer import notification

def show_alert(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="ScreenAssistant",
        timeout=5
    )




=======

def trigger_tray_popup():
    """Show a popup notification when user gets distracted"""
    def show_popup():
        # Create a hidden root window (required for tkinter)
        root = tk.Tk()
        root.withdraw()
        
        # Show the warning message
        messagebox.showwarning(
            "Focus Alert",
            "You're drifting from your focus! Get back on track."
        )
        
        # Clean up
        root.destroy()
    
    # Run in a separate thread to avoid blocking
    threading.Thread(target=show_popup, daemon=True).start()
>>>>>>> 86744fa57c56d37e6c25bbf0d94906edc8deb6e5
