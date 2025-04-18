def get_app_for_task(task):
    if task == "write_note":
        return "notepad"
    elif task == "calculate":
        return "calculator"
    elif task == "browse":
        return "chrome"
    elif task == "write_doc":
        return "wordpad"
    else:
        return None
