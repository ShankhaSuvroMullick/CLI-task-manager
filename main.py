# main.py
import typer
from typing import List, Optional
from task_manager import (
    add_task,
    delete_task,
    complete_task,
    get_all_tasks,
    edit_task,
    undo_last,
)

app = typer.Typer(help="CLI Task Manager")


@app.command()
def add(
    titles: List[str] = typer.Argument(..., help="Titles of tasks to add"),
    due: Optional[str] = typer.Option(None, "--due", help="Due date YYYY-MM-DD"),
    priority: str = typer.Option("medium", "--priority", help="Priority: low, medium, high"),
):
    """Add one or more tasks."""
    try:
        if priority not in ("low", "medium", "high"):
            typer.echo("Error: Priority must be low, medium, or high.")
            raise typer.Exit(code=1)

        if due:
            from datetime import datetime
            try:
                datetime.strptime(due, "%Y-%m-%d")
            except ValueError:
                typer.echo("Error: Date must be in YYYY-MM-DD format. Example: 2024-12-31")
                raise typer.Exit(code=1)

        added = add_task(titles, due_date=due, priority=priority)
        for task in added:
            due_str = f" (due: {task.due})" if task.due else ""
            pri_str = f" [{task.priority.upper()}]"
            typer.echo(f"Added task #{task.id}: {task.title}{pri_str}{due_str}")
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def delete(
    task_ids: List[int] = typer.Argument(..., help="IDs of tasks to delete"),
):
    """Delete one or more tasks by ID."""
    try:
        deleted, not_found = delete_task(task_ids)
        for task_id in deleted:
            typer.echo(f"Deleted task #{task_id}")
        for task_id in not_found:
            typer.echo(f"No task found with ID {task_id}")
        if not_found:
            raise typer.Exit(code=1)
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def complete(
    task_ids: List[int] = typer.Argument(..., help="IDs of tasks to complete"),
):
    """Mark one or more tasks as complete."""
    try:
        completed, not_found = complete_task(task_ids)
        for task_id in completed:
            typer.echo(f"Task #{task_id} marked as complete!")
        for task_id in not_found:
            typer.echo(f"No task found with ID {task_id}")
        if not_found:
            raise typer.Exit(code=1)
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def edit(
    task_id: int = typer.Argument(..., help="ID of task to edit"),
    new_title: str = typer.Argument(..., help="New title for the task"),
):
    """Edit a task title by ID."""
    try:
        task = edit_task(task_id, new_title)
        if task:
            typer.echo(f"Task #{task.id} updated to: {task.title}")
        else:
            typer.echo(f"No task found with ID {task_id}")
            raise typer.Exit(code=1)
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command(name="list")
def list_tasks(
    done: bool = typer.Option(False, "--done", help="Show only completed tasks"),
    pending: bool = typer.Option(False, "--pending", help="Show only pending tasks"),
    overdue: bool = typer.Option(False, "--overdue", help="Show only overdue tasks"),
    priority: Optional[str] = typer.Option(None, "--priority", help="Filter by priority: low, medium, high"),
):
    """List all tasks."""
    try:
        from datetime import datetime
        today = datetime.today().strftime("%Y-%m-%d")

        tasks = get_all_tasks()

        if not tasks:
            typer.echo("No tasks yet. Add one with: python main.py add 'Your task'")
            return

        if done:
            tasks = [t for t in tasks if t.done is True]
        elif pending:
            tasks = [t for t in tasks if t.done is False]
        elif overdue:
            tasks = [t for t in tasks if t.due and t.due < today and not t.done]

        if priority:
            if priority not in ("low", "medium", "high"):
                typer.echo("Error: Priority must be low, medium, or high.")
                raise typer.Exit(code=1)
            tasks = [t for t in tasks if t.priority == priority]

        if not tasks:
            typer.echo("No tasks match that filter.")
            return

        typer.echo("\nYour Tasks:")
        typer.echo("-" * 40)
        for task in tasks:
            status = "DONE" if task.done else "TODO"
            due_str = f" (due: {task.due})" if task.due else ""
            pri = task.priority.upper()
            typer.echo(f"  [{status}] #{task.id} [{pri}] - {task.title}{due_str}")
        typer.echo("")

    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search term to look for in tasks"),
):
    """Search tasks by title."""
    try:
        tasks = get_all_tasks()

        if not tasks:
            typer.echo("No tasks yet.")
            return

        results = [t for t in tasks if query.lower() in t.title.lower()]

        if not results:
            typer.echo(f"No tasks found matching '{query}'")
            return

        typer.echo(f"\nSearch results for '{query}':")
        typer.echo("-" * 40)
        for task in results:
            status = "DONE" if task.done else "TODO"
            due_str = f" (due: {task.due})" if task.due else ""
            pri = task.priority.upper()
            typer.echo(f"  [{status}] #{task.id} [{pri}] - {task.title}{due_str}")
        typer.echo("")

    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def export(
    csv: bool = typer.Option(False, "--csv", help="Export as CSV instead of TXT"),
):
    """Export tasks to a file."""
    try:
        from datetime import datetime
        tasks = get_all_tasks()

        if not tasks:
            typer.echo("No tasks to export.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if csv:
            filename = f"tasks_{timestamp}.csv"
            with open(filename, "w") as f:
                f.write("id,title,done,priority,due\n")
                for task in tasks:
                    f.write(
                        f"{task.id},"
                        f"{task.title},"
                        f"{task.done},"
                        f"{task.priority},"
                        f"{task.due or ''}\n"
                    )
        else:
            filename = f"tasks_{timestamp}.txt"
            with open(filename, "w") as f:
                f.write("MY TASKS\n")
                f.write("=" * 40 + "\n\n")
                for task in tasks:
                    status = "DONE" if task.done else "TODO"
                    due_str = f" (due: {task.due})" if task.due else ""
                    pri = task.priority.upper()
                    f.write(f"[{status}] #{task.id} [{pri}] - {task.title}{due_str}\n")

        typer.echo(f"Tasks exported to {filename}")

    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def stats():
    """Show task statistics."""
    try:
        from datetime import datetime
        today = datetime.today().strftime("%Y-%m-%d")

        tasks = get_all_tasks()

        if not tasks:
            typer.echo("No tasks yet.")
            return

        total     = len(tasks)
        completed = len([t for t in tasks if t.done is True])
        pending   = len([t for t in tasks if t.done is False])
        overdue   = len([t for t in tasks if t.due and t.due < today and not t.done])
        high      = len([t for t in tasks if t.priority == "high"])
        medium    = len([t for t in tasks if t.priority == "medium"])
        low       = len([t for t in tasks if t.priority == "low"])

        typer.echo("\n📊 Task Statistics")
        typer.echo("-" * 40)
        typer.echo(f"  Total tasks:      {total}")
        typer.echo(f"  Completed:        {completed}")
        typer.echo(f"  Pending:          {pending}")
        typer.echo(f"  Overdue:          {overdue}")
        typer.echo("-" * 40)
        typer.echo(f"  High priority:    {high}")
        typer.echo(f"  Medium priority:  {medium}")
        typer.echo(f"  Low priority:     {low}")
        typer.echo("")

    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def undo():
    """Undo the last action."""
    if undo_last():
        typer.echo("Last action undone successfully.")
    else:
        typer.echo("Nothing to undo.")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()