# main.py
import typer
from task_manager import add_task, delete_task, complete_task, get_all_tasks

app = typer.Typer(help="CLI Task Manager")

@app.command()
def add(title: str = typer.Argument(..., help="Title of the new task")):
    """Add a new task."""
    task = add_task(title)
    typer.echo(f"Added task #{task['id']}: {task['title']}")

@app.command()
def delete(task_id: int = typer.Argument( help="ID of task to delete")):
    """Delete a task by ID."""
    if delete_task(task_id):
        typer.echo(f"Deleted task #{task_id}")
    else:
        typer.echo(f"No task found with ID {task_id}")
        raise typer.Exit(code=1)

@app.command()
def complete(task_id: int = typer.Argument(..., help="ID of task to complete")):
    """Mark a task as complete."""
    if complete_task(task_id):
        typer.echo(f"Task #{task_id} marked as complete!")
    else:
        typer.echo(f"No task found with ID {task_id}")
        raise typer.Exit(code=1)

@app.command()
def list_tasks():
    """List all tasks."""
    tasks = get_all_tasks()
    if not tasks:
        typer.echo("No tasks yet. Add one with: python main.py add 'Your task'")
        return
    typer.echo("\nYour Tasks:")
    typer.echo("-" * 30)
    for task in tasks:
        status = "DONE" if task["done"] else "TODO"
        typer.echo(f"  [{status}] #{task['id']} - {task['title']}")
    typer.echo("")

if __name__ == "__main__":
    app()