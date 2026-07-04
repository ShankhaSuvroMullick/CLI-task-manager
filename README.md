# CLI Task Manager

A command-line task manager built with Python and Typer.

## Features
- Add, delete, complete tasks
- Multiple IDs at once
- Filter by done, pending, overdue
- Edit tasks
- Due dates
- Priority levels (low, medium, high)
- Search tasks
- Export to TXT and CSV
- Undo last action
- Statistics

## Setup

```bash
git clone https://github.com/YOURUSERNAME/cli-task-manager.git
cd cli-task-manager
python -m venv venv
venv\Scripts\activate
pip install typer
```

## Usage

```bash
python main.py add "Buy groceries"
python main.py add "Task" --priority high --due 2024-12-31
python main.py list
python main.py list --done
python main.py list --priority high
python main.py complete 1 2
python main.py delete 3
python main.py edit 1 "New title"
python main.py search "buy"
python main.py export
python main.py export --csv
python main.py stats
python main.py undo
```

## Stack
- Python
- Typer