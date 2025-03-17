import json
import os
from datetime import datetime

TaskFile_json = "Task.json"

def Load_Tasks():
    """Load tasks from the JSON file or create a new one if it doesn't exist."""
    if os.path.exists(TaskFile_json):
        with open(TaskFile_json, "r") as file:
            try:
                tasks = json.load(file)
                tasks.setdefault("Pending", [])
                tasks.setdefault("Completed", [])
                tasks.setdefault("Removed", [])
                return tasks
            except json.JSONDecodeError: 
                print("⚠ Error: Task file is corrupted. Resetting it.")

                # If file doesn't exist or was corrupted, create an empty structure
                tasks = {"Pending": [], "Completed": [], "Removed": []}
                Save_Tasks(tasks)  # Save the new empty structure
    return tasks
def Save_Tasks(Tasks):
    """Save tasks to the JSON file."""
    with open(TaskFile_json, "w") as file:
        json.dump(Tasks, file, indent=4)

def Add_Task(Tasks, Task, deadline=None, priority="Medium"):
    """Add a task with priority and deadline."""
    if Task not in [t["name"] for t in Tasks["Pending"]]:  # Ensure no duplicate task names
        Task_entry = {
            "name": Task,
            "priority": priority.capitalize(),  # Ensure capitalization (High, Medium, Low)
            "deadline": deadline if deadline else "No deadline"
        }
        Tasks["Pending"].append(Task_entry)
        Save_Tasks(Tasks)
        print(f"✅ Task '{Task}' added successfully with priority: {priority} and deadline: {Task_entry['deadline']}")
    else:
        print("⚠ Task is already in the Pending List.\nOperation Failed.")

def Remove_Task(Tasks, Task):
    """Remove a task and move it to Removed list."""
    for t in Tasks["Pending"]:
        if t["name"] == Task:
            Tasks["Pending"].remove(t)
            Tasks["Removed"].append(t)
            Save_Tasks(Tasks)
            print(f"❌ Task '{Task}' removed!")
            return
    print(f"⚠ Task '{Task}' not found.")

def MarkCompleted(Tasks, Task):
    """Mark a task as completed and move it to Completed list."""
    for t in Tasks["Pending"]:
        if t["name"] == Task:
            Tasks["Pending"].remove(t)
            Tasks["Completed"].append(t)
            Save_Tasks(Tasks)
            print(f"✅ Task '{Task}' marked as Completed.")
            return
    print(f"⚠ Task '{Task}' not found.")

def Show_All_Tasks(Tasks):
    """Display tasks along with their priority and deadline."""
    print("\n📌 Pending Tasks:")
    if not Tasks["Pending"]:
        print("No Pending Tasks available!")
    else:
        for t in Tasks["Pending"]:
            print(f"- {t['name']} (Priority: {t['priority']}, Deadline: {t['deadline']})")

    print("\n✔ Completed Tasks:")
    if not Tasks["Completed"]:
        print("No Completed Tasks available!")
    else:
        for t in Tasks["Completed"]:
            print(f"- {t['name']} (Priority: {t['priority']}, Deadline: {t['deadline']})")

    print("\n❌ Removed Tasks:")
    if not Tasks["Removed"]:
        print("No Removed Tasks available!")
    else:
        for t in Tasks["Removed"]:
            print(f"- {t['name']} (Priority: {t['priority']}, Deadline: {t['deadline']})")

def Undo_RemovedTasks(Tasks):
    """Restore the last removed task."""
    if not Tasks["Removed"]:
        print("⚠ There are no removed tasks to undo.")
    else:
        Task = Tasks["Removed"].pop()
        Tasks["Pending"].append(Task)
        print(f"✅ Removed Task '{Task['name']}' restored successfully.")
        Save_Tasks(Tasks)

def Empty_List(Tasks, group):
    """Clear all tasks from a specific group."""
    if group in Tasks:
        Tasks[group].clear()
        Save_Tasks(Tasks)
        print(f"✅ Group '{group}' cleared successfully.")
    else:
        print(f"⚠ Group '{group}' does not exist.")

def main():
    TaskManage = Load_Tasks()
    while True:
        print("\n📝 Daily Task Manager")
        print("1. Add Tasks")
        print("2. Remove Tasks")
        print("3. View Tasks")
        print("4. Mark Tasks As Completed")
        print("5. Undo Last Removed Task")
        print("6. Clear Group")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            Task = input("Enter Your Task: ").strip()
            priority = input("Enter Priority (High, Medium, Low): ").strip().capitalize()
            deadline = input("Enter deadline (YYYY-MM-DD) or leave blank: ").strip()
            try:
                if deadline:
                    datetime.strptime(deadline, "%Y-%m-%d")  # Validate date format
                else:
                    deadline = None
            except ValueError:
                print("⚠ Invalid date format! Setting deadline to 'No deadline'.")
                deadline = None  
            Add_Task(TaskManage, Task, deadline, priority)
            TaskManage = Load_Tasks()
        elif choice == "2":
            Task = input("Enter the Task you want to Remove: ").strip()
            Remove_Task(TaskManage, Task)
            TaskManage = Load_Tasks()
        elif choice == "3":
            Show_All_Tasks(TaskManage)
        elif choice == "4":
            Task = input("Enter the Task you want to Mark As Completed: ").strip()
            MarkCompleted(TaskManage, Task)
            TaskManage = Load_Tasks()
        elif choice == "5":
            Undo_RemovedTasks(TaskManage)
            TaskManage = Load_Tasks()
        elif choice == "6":
            group = input("Enter the Group to Clear (Pending, Completed, Removed): ").strip()
            Empty_List(TaskManage, group)
            TaskManage = Load_Tasks()
        elif choice == "7":
            print("👋 Exiting the Program.")
            break
        else:
            print("⚠ Invalid Choice. Please enter a valid number.")

if __name__ == "__main__":
    main()
