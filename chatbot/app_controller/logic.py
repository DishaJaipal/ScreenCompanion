def launch_app_for_task(task_description):
    """Simple app launcher logic - customize this"""
    task = task_description.lower()
    
    app_mapping = {
        "code": "code",
        "write": "notepad",
        "browse": "chrome",
        "music": "spotify"
    }
    
    for keyword, app in app_mapping.items():
        if keyword in task:
            return f"Launching {app} for: {task_description}"
    
    return f"No app configured for: {task_description}"