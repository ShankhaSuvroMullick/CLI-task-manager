# task_manager.py
from storage import load_tasks, save_tasks, restore_backup
from models import Task

def add_task(titles: list[str], due_date: str = None, priority: str = "medium") -> list[Task]:
    tasks = load_tasks()
    added = []
    for title in titles:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        new_id = max((t.id for t in tasks), default=0) + 1
        task = Task(
            id=new_id,
            title=title,
            due=due_date,
            priority=priority
        )
        tasks.append(task)
        added.append(task)
    save_tasks(tasks)
    return added

def delete_task(task_ids: list[int]):
    tasks = load_tasks()
    deleted = []
    not_found = []
    for task_id in task_ids:
        filtered = [t for t in tasks if t.id != task_id]
        if len(filtered) == len(tasks):
            not_found.append(task_id)
        else:
            deleted.append(task_id)
            tasks = filtered
    save_tasks(tasks)
    return deleted, not_found

def complete_task(task_ids: list[int]):
    tasks = load_tasks()
    completed = []
    not_found = []
    for task_id in task_ids:
        found = False
        for task in tasks:
            if task.id == task_id:
                task.done = True
                completed.append(task_id)
                found = True
                break
        if not found:
            not_found.append(task_id)
    save_tasks(tasks)
    return completed, not_found

def edit_task(task_id: int, new_title: str):
    new_title = new_title.strip()
    if not new_title:
        raise ValueError("Task title cannot be empty.")
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.title = new_title
            save_tasks(tasks)
            return task
    return None

def get_all_tasks() -> list[Task]:
    return load_tasks()

def undo_last() -> bool:
    return restore_backup()