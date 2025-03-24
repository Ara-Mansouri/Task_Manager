import json
import os
from datetime import datetime
from datetime import date
from pkgutil import get_data

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

def Get_Valid_priority():
    Valid_priorities=['High','Medium','Low']
    while True:
        priority = input("Enter Priority (High, Medium, Low): ").strip().capitalize()
        if priority in Valid_priorities:
            return priority
        else:
            print("⚠ Invalid priority. Please enter High, Medium, or Low.")

def Get_Valid_deadline():
     deadline = input("Enter deadline (YYYY-MM-DD) or leave blank: ").strip()
     try:
        if deadline:
            datetime.strptime(deadline, "%Y-%m-%d")  # Validate date format
        else:
            deadline = "No deadline"
     except ValueError:
        print("⚠ Invalid date format! Setting deadline to 'No deadline'.")
        deadline = "No deadline" 
     return deadline   

def Add_Task(Tasks):
    Valid_priorities=['High','Medium','Low']
    Task = input("Enter Your Task: ").strip()
    priority = Get_Valid_priority()
    deadline=Get_Valid_deadline()
    
    """Add a task with priority and deadline."""
    if Task not in [t["name"] for t in Tasks["Pending"]]:  # Ensure no duplicate task names
        Task_entry = {
            "name": Task,
            "priority": priority.capitalize(),  # Ensure capitalization (High, Medium, Low)
            "deadline": deadline 
        }
        Tasks["Pending"].append(Task_entry)
        Save_Tasks(Tasks)
        print(f"✅ Task '{Task}' added successfully with priority: {priority} and deadline: {Task_entry['deadline']}")
    else:
        print("⚠ Task is already in the Pending List.\nOperation Failed.")

def Remove_Task(Tasks):
    """Remove a task and move it to Removed list."""
    index=int(input("Enter The Number of the Task you wanna Remove:"))-1
    if 0<=index<len(Tasks["Pending"]):
        RTask=Tasks["Pending"].pop(index)
        Tasks["Removed"].append(RTask)
        Save_Tasks(Tasks)
        print(f"❌ Task '{RTask['name']}' removed!")
    else:
        print(f"⚠ Task number '{index+1}' not found.")

def MarkCompleted(Tasks):
   
    index=int(input("Enter the number of the Task you want To Mark as Completed:"))-1
    if 0<=index<len(Tasks["Pending"]):
        CTask=Tasks["Pending"].pop(index)
        Tasks["Completed"].append(CTask)
        Save_Tasks(Tasks)
        print(f"✅ Task number '{index+1}' marked as Completed.")
    else:
        print(print("⚠ Task number not found."))

def PendingDeadlineHandler(index,task):
    try:
        task_deadline = datetime.strptime(task['deadline'], "%Y-%m-%d").date()
        if task_deadline==date.today():
            print(f"-{index} 🔔 {task['name']} (Priority: {task['priority']}, Deadline: {task['deadline']})")
        else:
            print(f"-{index} {task['name']} (Priority: {task['priority']}, Deadline: {task['deadline']})")
    except ValueError:
        print(f"-{index} {task['name']} (Priority: {task['priority']}, Deadline: {task['deadline']})")

def Show_All_Tasks(Tasks):
    """Display tasks along with their priority and deadline."""
    print(f"\n📌 Pending Tasks Count({len(Tasks['Pending'])}):")
    if not Tasks["Pending"]:
        print("No Pending Tasks available!")
    else:
        for index,task in enumerate(Tasks["Pending"],start=1):
            PendingDeadlineHandler(index,task)
    print(f"\n✔ Completed Tasks Count({len(Tasks['Completed'])}):")
    if not Tasks["Completed"]:
        print("No Completed Tasks available!")
    else:
        for index , t in enumerate(Tasks["Completed"],start=1):
            print(f"- {index} {t['name']} (Priority: {t['priority']}, Deadline: {t['deadline']})")

    print(f"\n❌ Removed Tasks Count({len(Tasks['Removed'])}):")
    if not Tasks["Removed"]:
        print("No Removed Tasks available!")
    else:
        for index,t in enumerate(Tasks["Removed"],start=1):
            print(f"- {index} {t['name']} (Priority: {t['priority']}, Deadline: {t['deadline']})")

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

def Search_Tasks(Tasks):
    keyword=input("Enter task name,deadline or priority:").strip().lower()
    found=False
    print("\nFounded Tasks:")
    Groups=["Pending","Completed","Removed"]
    for group in Groups:
        for Task in Tasks[group]:
            if keyword in Task["name"].lower() or keyword in Task["deadline"].lower() or keyword in Task["priority"].lower():
                print(f"Task {Task['name']} found in the group {group} with deadline {Task['deadline']} and priority {Task['priority']} ")
                found=True
    if not found:
        print("No Matching Tasks were Found")

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
        print("7. Search Tasks")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            Add_Task(TaskManage)
            TaskManage = Load_Tasks()
        elif choice == "2":
            Remove_Task(TaskManage)
            TaskManage = Load_Tasks()
        elif choice == "3":
            Show_All_Tasks(TaskManage)
        elif choice == "4":
            MarkCompleted(TaskManage)
            TaskManage = Load_Tasks()
        elif choice == "5":
            Undo_RemovedTasks(TaskManage)
            TaskManage = Load_Tasks()
        elif choice == "6":
            group = input("Enter the Group to Clear (Pending, Completed, Removed): ").strip()
            Empty_List(TaskManage, group)
            TaskManage = Load_Tasks()
        elif choice == "7":
            Search_Tasks(TaskManage)
        elif choice == "8":
            print("👋 Exiting the Program.")
            break
        else:
            print("⚠ Invalid Choice. Please enter a valid number.")

if __name__ == "__main__":
    main()
