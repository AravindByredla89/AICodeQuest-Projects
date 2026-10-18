
import json
import os
from datetime import datetime, date

FILE_NAME = "tasks.json"
DATE_FORMAT = "%Y-%m-%d"

PRIORITIES = {
    "1": "High",
    "2": "Medium",
    "3": "Low"
}

PRIORITY_ORDER = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}


def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            tasks = json.load(file)

        if not isinstance(tasks, list):
            print("Warning: Invalid task file format.")
            return []

        valid_tasks = []

        for task in tasks:
            if not isinstance(task, dict):
                continue

            if not all(key in task for key in
                       ("id", "title", "priority", "completed")):
                continue

            task.setdefault("description", "")
            task.setdefault("due_date", "")
            task.setdefault("created_at", "")
            task.setdefault("updated_at", "")

            valid_tasks.append(task)

        return valid_tasks

    except (json.JSONDecodeError, OSError):
        print("Warning: Could not load tasks. Starting with an empty list.")
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
    except OSError as error:
        print(f"Error: Could not save tasks: {error}")


def current_timestamp():
    """Return the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_next_id(tasks):
    """Generate a unique ID greater than all existing IDs."""
    return max(
        (task["id"] for task in tasks if isinstance(task["id"], int)),
        default=0
    ) + 1


def get_priority():
    """Ask for a valid priority."""
    print("Priority: 1. High  2. Medium  3. Low")

    while True:
        choice = input("Choose priority [default: 2]: ").strip()

        if not choice:
            return "Medium"

        if choice in PRIORITIES:
            return PRIORITIES[choice]

        print("Invalid choice. Enter 1, 2, or 3.")


def get_due_date(existing_date=""):
    """Read an optional due date in YYYY-MM-DD format."""
    while True:
        prompt = f"Due date YYYY-MM-DD [{existing_date}]: "
        value = input(prompt).strip()

        if not value:
            return existing_date

        if value.lower() == "none":
            return ""

        try:
            datetime.strptime(value, DATE_FORMAT)
            return value
        except ValueError:
            print("Invalid date. Example: 2026-12-31")


def is_overdue(task):
    """Check whether a pending task is past its due date."""
    if task["completed"] or not task.get("due_date"):
        return False

    try:
        due = datetime.strptime(
            task["due_date"], DATE_FORMAT
        ).date()

        return due < date.today()

    except ValueError:
        return False


def add_task(tasks):
    """Add a new task with description and due date."""
    title = input("Enter task title: ").strip()

    if not title:
        print("Task title cannot be empty.")
        return

    description = input("Enter task description (optional): ").strip()
    priority = get_priority()
    due_date = get_due_date()

    timestamp = current_timestamp()

    task = {
        "id": get_next_id(tasks),
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "completed": False,
        "created_at": timestamp,
        "updated_at": timestamp
    }

    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully!")


def view_tasks(tasks, status="all"):
    """Display tasks filtered by status."""
    filtered_tasks = []

    for task in tasks:
        if status == "all":
            filtered_tasks.append(task)
        elif status == "pending" and not task["completed"]:
            filtered_tasks.append(task)
        elif status == "completed" and task["completed"]:
            filtered_tasks.append(task)
        elif status == "overdue" and is_overdue(task):
            filtered_tasks.append(task)

    if not filtered_tasks:
        print("No tasks found.")
        return

    print("\n" + "-" * 100)
    print(
        f"{'ID':<5} {'Status':<12} {'Priority':<10} "
        f"{'Due Date':<12} Title"
    )
    print("-" * 100)

    for task in filtered_tasks:
        if task["completed"]:
            task_status = "Completed"
        elif is_overdue(task):
            task_status = "Overdue"
        else:
            task_status = "Pending"

        due_date = task.get("due_date") or "Not set"

        print(
            f"{task['id']:<5} {task_status:<12} "
            f"{task['priority']:<10} {due_date:<12} "
            f"{task['title']}"
        )

        if task.get("description"):
            print(f"      Description: {task['description']}")

    print("-" * 100)


def find_task(tasks, task_id):
    """Find a task by its ID."""
    return next(
        (task for task in tasks if task["id"] == task_id),
        None
    )


def get_task_id():
    """Read and validate a task ID."""
    try:
        task_id = int(input("Enter task ID: "))

        if task_id <= 0:
            print("Task ID must be a positive number.")
            return None

        return task_id

    except ValueError:
        print("Please enter a valid numeric ID.")
        return None


def complete_task(tasks):
    """Mark a task as completed."""
    task_id = get_task_id()

    if task_id is None:
        return

    task = find_task(tasks, task_id)

    if task is None:
        print("Task not found.")
        return

    if task["completed"]:
        print("Task is already completed.")
        return

    task["completed"] = True
    task["updated_at"] = current_timestamp()

    save_tasks(tasks)
    print("Task marked as completed!")


def reopen_task(tasks):
    """Mark a completed task as pending again."""
    task_id = get_task_id()

    if task_id is None:
        return

    task = find_task(tasks, task_id)

    if task is None:
        print("Task not found.")
        return

    if not task["completed"]:
        print("This task is already pending.")
        return

    task["completed"] = False
    task["updated_at"] = current_timestamp()

    save_tasks(tasks)
    print("Task reopened successfully!")


def edit_task(tasks):
    """Edit a task's title, description, priority, and due date."""
    task_id = get_task_id()

    if task_id is None:
        return

    task = find_task(tasks, task_id)

    if task is None:
        print("Task not found.")
        return

    new_title = input(
        f"New title [{task['title']}]: "
    ).strip()

    if new_title:
        task["title"] = new_title

    new_description = input(
        f"New description [{task.get('description', '')}]: "
    ).strip()

    if new_description:
        task["description"] = new_description
    elif input("Clear description? (y/n): ").strip().lower() == "y":
        task["description"] = ""

    print("Priority: 1. High  2. Medium  3. Low")
    choice = input(
        f"New priority [{task['priority']}], Enter to skip: "
    ).strip()

    if choice in PRIORITIES:
        task["priority"] = PRIORITIES[choice]
    elif choice:
        print("Invalid priority. Keeping existing priority.")

    task["due_date"] = get_due_date(task.get("due_date", ""))
    task["updated_at"] = current_timestamp()

    save_tasks(tasks)
    print("Task updated successfully!")


def delete_task(tasks):
    """Delete a task after confirmation."""
    task_id = get_task_id()

    if task_id is None:
        return

    task = find_task(tasks, task_id)

    if task is None:
        print("Task not found.")
        return

    confirmation = input(
        f"Delete '{task['title']}'? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        tasks.remove(task)
        save_tasks(tasks)
        print("Task deleted successfully!")
    else:
        print("Deletion cancelled.")


def search_tasks(tasks):
    """Search tasks by title or description."""
    keyword = input("Enter search keyword: ").strip().lower()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    results = [
        task for task in tasks
        if keyword in task["title"].lower()
        or keyword in task.get("description", "").lower()
    ]

    if results:
        print(f"\nFound {len(results)} matching task(s):")
        view_tasks(results)
    else:
        print("No matching tasks found.")


def sort_tasks(tasks):
    """Display tasks sorted by a selected field."""
    if not tasks:
        print("No tasks available to sort.")
        return

    print("\nSort tasks by:")
    print("1. Priority")
    print("2. Due date")
    print("3. Title")
    print("4. Creation date")

    choice = input("Choose sorting option: ").strip()

    if choice == "1":
        sorted_tasks = sorted(
            tasks,
            key=lambda task: PRIORITY_ORDER.get(
                task["priority"], 4
            )
        )
    elif choice == "2":
        sorted_tasks = sorted(
            tasks,
            key=lambda task: (
                not bool(task.get("due_date")),
                task.get("due_date", "")
            )
        )
    elif choice == "3":
        sorted_tasks = sorted(
            tasks,
            key=lambda task: task["title"].lower()
        )
    elif choice == "4":
        sorted_tasks = sorted(
            tasks,
            key=lambda task: task.get("created_at", "")
        )
    else:
        print("Invalid sorting option.")
        return

    view_tasks(sorted_tasks)


def show_statistics(tasks):
    """Display a summary of task progress."""
    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    pending = total - completed
    overdue = sum(1 for task in tasks if is_overdue(task))

    high = sum(
        1 for task in tasks
        if task["priority"] == "High" and not task["completed"]
    )

    medium = sum(
        1 for task in tasks
        if task["priority"] == "Medium" and not task["completed"]
    )

    low = sum(
        1 for task in tasks
        if task["priority"] == "Low" and not task["completed"]
    )

    print("\n========== TASK STATISTICS ==========")
    print(f"Total tasks:       {total}")
    print(f"Completed tasks:   {completed}")
    print(f"Pending tasks:     {pending}")
    print(f"Overdue tasks:     {overdue}")
    print(f"High priority:     {high}")
    print(f"Medium priority:   {medium}")
    print(f"Low priority:      {low}")

    if total > 0:
        percentage = (completed / total) * 100
        print(f"Completion rate:   {percentage:.2f}%")

    print("=====================================")


def show_menu():
    """Display the main menu."""
    print("\n========== TODO MANAGER ==========")
    print("1. Add task")
    print("2. View all tasks")
    print("3. View pending tasks")
    print("4. View completed tasks")
    print("5. Complete task")
    print("6. Edit task")
    print("7. Delete task")
    print("8. Search tasks")
    print("9. Sort tasks")
    print("10. Show statistics")
    print("11. View overdue tasks")
    print("12. Reopen completed task")
    print("13. Exit")
    print("==================================")


def main():
    """Run the application."""
    tasks = load_tasks()

    print("Welcome to the Terminal To-Do Manager!")

    while True:
        show_menu()
        choice = input("Enter your choice (1-13): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            view_tasks(tasks, "pending")
        elif choice == "4":
            view_tasks(tasks, "completed")
        elif choice == "5":
            complete_task(tasks)
        elif choice == "6":
            edit_task(tasks)
        elif choice == "7":
            delete_task(tasks)
        elif choice == "8":
            search_tasks(tasks)
        elif choice == "9":
            sort_tasks(tasks)
        elif choice == "10":
            show_statistics(tasks)
        elif choice == "11":
            view_tasks(tasks, "overdue")
        elif choice == "12":
            reopen_task(tasks)
        elif choice == "13":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-13.")


if __name__ == "__main__":
    main()
