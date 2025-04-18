import threading
import tkinter as tk

def trigger_tray_popup():
    def show_popup():
        window = tk.Tk()
        window.title("Stay Focused!")
        window.geometry("300x150")
        tk.Label(window, text="You're drifting from today's focus. Refocus?").pack(pady=10)
        tk.Button(window, text="Back to focus!", command=window.destroy).pack(pady=5)
        tk.Button(window, text="Ignore", command=window.destroy).pack(pady=5)
        window.mainloop()

    threading.Thread(target=show_popup).start()
