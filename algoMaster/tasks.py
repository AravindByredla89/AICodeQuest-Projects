
def add_task(tasks, task):
    tasks.append(task)
    print(f"Task added: {task}")


def show_tasks(tasks):
    if not tasks:
        print("No tasks available.")
        return

    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task}")


def remove_task(tasks, task_number):
    if 1 <= task_number <= len(tasks):
        removed = tasks.pop(task_number - 1)
        print(f"Task removed: {removed}")
    else:
        print("Invalid task number.")


def main():
    tasks = []

    while True:
        print("\n1. Add task")
        print("2. Show tasks")
        print("3. Remove task")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            task = input("Enter task: ")
            add_task(tasks, task)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            show_tasks(tasks)
            try:
                number = int(input("Enter task number to remove: "))
                remove_task(tasks, number)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
