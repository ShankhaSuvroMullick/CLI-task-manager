# storage.py
import json
import os
from models import Task

TASKS_FILE = "tasks.json"
BACKUP_FILE = "tasks_backup.json"

def load_tasks() -> list[Task]:
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as file:
            data = json.load(file)
            return [Task.from_dict(t) for t in data]
    except json.JSONDecodeError:
        raise ValueError(
            "tasks.json is corrupted. Please fix or delete the file."
        )

def save_tasks(tasks: list[Task]) -> None:
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            backup_data = f.read()
        with open(BACKUP_FILE, "w") as f:
            f.write(backup_data)
    with open(TASKS_FILE, "w") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2)

def restore_backup() -> bool:
    if not os.path.exists(BACKUP_FILE):
        return False
    with open(BACKUP_FILE, "r") as f:
        backup_data = f.read()
    with open(TASKS_FILE, "w") as f:
        f.write(backup_data)
    os.remove(BACKUP_FILE)
    return True