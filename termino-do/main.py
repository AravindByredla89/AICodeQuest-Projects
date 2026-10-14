
import json
import os

FILE_NAME = "tasks.json"


def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not load tasks. Starting with an empty list.")
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except OSError:
        print("Error: Could not save tasks.")


def add_task(tasks):
    """Add a new task."""
    title = input("Enter task title: ").strip()

    if not title:
        print("Task title cannot be empty.")
        return

    print("Priority: 1. High  2. Medium  3. Low")
    priority_choice = input("Choose priority [default: 2]: ").strip()

    priorities = {"1": "High", "2": "Medium", "3": "Low"}
    priority = priorities.get(priority_choice, "Medium")

    task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        "title": title,
        "priority": priority,
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully!")


def view_tasks(tasks, status="all"):
    """Display tasks, optionally filtered by status."""
    filtered_tasks = [
        task for task in tasks
        if status == "all"
        or (status == "pending" and not task["completed"])
        or (status == "completed" and task["completed"])
    ]

    if not filtered_tasks:
        print("No tasks found.")
        return

    print("\n" + "-" * 60)
    print(f"{'ID':<5} {'Status':<12} {'Priority':<10} Title")
    print("-" * 60)

    for task in filtered_tasks:
        task_status = "Completed" if task["completed"] else "Pending"
        print(
            f"{task['id']:<5} {task_status:<12} "
            f"{task['priority']:<10} {task['title']}"
        )

    print("-" * 60)


def find_task(tasks, task_id):
    """Find a task by its ID."""
    return next(
        (task for task in tasks if task["id"] == task_id),
        None
    )


def get_task_id():
    """Read and validate a task ID."""
    try:
        return int(input("Enter task ID: "))
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
    save_tasks(tasks)
    print("Task marked as completed!")


def edit_task(tasks):
    """Edit a task's title and priority."""
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

    print("Priority: 1. High  2. Medium  3. Low")
    choice = input(
        f"New priority [{task['priority']}], Enter to skip: "
    ).strip()

    priorities = {"1": "High", "2": "Medium", "3": "Low"}

    if choice in priorities:
        task["priority"] = priorities[choice]
    elif choice:
        print("Invalid priority. Keeping the existing priority.")

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
    print("8. Exit")
    print("==================================")


def main():
    """Run the application."""
    tasks = load_tasks()
    print("Welcome to the Terminal To-Do Manager!")

    while True:
        show_menu()
        choice = input("Enter your choice (1-8): ").strip()

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
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    main()
