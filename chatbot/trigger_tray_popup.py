import threading
import tkinter as tk
from tkinter import messagebox

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