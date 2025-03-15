import json
import os



TaskFile_json="Task.json"
def Load_Tasks():
    if os.path.exists(TaskFile_json):
        with open (TaskFile_json,"r") as file:
            return json.load(file)
    return     {"pending":[],"Completed":[]}#یک دیکشنری با دو تا کلید که جواب کلید ها لیست است
def Save_Tasks(Tasks):
    with open(TaskFile_json,"w") as file:
        json.dump(Tasks,file,indent=4)#فایل را در قالب جیسون میریزد داخل فایل جیسون و برای فهم بهتر فاصله میندازد
        
def Add_Task(Tasks,Task):
    Tasks["pending"].append(Task)
    Save_Tasks(Tasks)
    print(f"Task {Task} Saved in  the System")
def Remove_Task(Tasks,Task):
    if Task in Tasks["pending"]:
        Tasks["pending"].remove(Task)
        Save_Tasks(Tasks)
        print(f"Task {Task} Removed from the List ")
    else:
        print(f"Task {Task} did not Found in the List")

def MarkCompleted(Tasks,Task):
    if Task in Tasks["pending"]:
        Tasks["pending"].remove(Task)
        Tasks["Completed"].append(Task)
        print(f"Task {Task} Marked as Completed.")
        Save_Tasks(Tasks)
    else:
        print(f"Task {Task} did not found")

def Show_All_Tasks(Tasks):
    print("pending Tasks:")
    for Task in Tasks["pending"]:
        print(f"- {Task}")
    print("Completed Tasks:")
    for Task in Tasks["Completed"]:
        print(f"- {Task}")

def main():
    while True:
        TaskManage=  Load_Tasks()
        print("\nDaily Task Manager")
        print("1.Add Tasks")
        print("2.Remove Tasks")
        print("3.View Tasks")
        print("4.Mark Tasks As Completed")
        print("5.Exit")
    
        choice=input("Enter your choice:")

        if choice =="1":
            Task=input("Enter Your Task")
            Add_Task(TaskManage,Task)
        elif choice=="2":
            Task=input("Enter the Task you Wanna Remove")
            Remove_Task(TaskManage,Task)
        elif choice=="3":
            Show_All_Tasks(TaskManage)
        elif choice=="4":
            Task=input("Enter the Task you Wanna Mark As Completd")
            MarkCompleted(TaskManage,Task)        
        elif choice=="5":
             print("Exit the Program")
             break    
        else:
            print("Invalid Choice")   

if __name__ == "__main__":
    main()
    


#     import json
# import os

# # File to store tasks
# TASKS_FILE = "tasks.json"

# # Load tasks from file (if exists)
# def load_tasks():
#     if os.path.exists(TASKS_FILE):
#         with open(TASKS_FILE, "r") as file:
#             return json.load(file)
#     return {"pending": [], "completed": []}

# # Save tasks to file
# def save_tasks(tasks):
#     with open(TASKS_FILE, "w") as file:
#         json.dump(tasks, file, indent=4)

# # Add a new task
# def add_task(tasks, task):
#     tasks["pending"].append(task)
#     save_tasks(tasks)
#     print(f"✅ Task '{task}' added successfully!")

# # Remove a task
# def remove_task(tasks, task):
#     if task in tasks["pending"]:
#         tasks["pending"].remove(task)
#         save_tasks(tasks)
#         print(f"❌ Task '{task}' removed!")
#     else:
#         print("⚠ Task not found.")

# # Mark task as completed
# def complete_task(tasks, task):
#     if task in tasks["pending"]:
#         tasks["pending"].remove(task)
#         tasks["completed"].append(task)
#         save_tasks(tasks)
#         print(f"✅ Task '{task}' marked as completed!")
#     else:
#         print("⚠ Task not found.")

# # Show all tasks
# def list_tasks(tasks):
#     print("\n📌 Pending Tasks:")
#     for task in tasks["pending"]:
#         print(f"  - {task}")

#     print("\n✅ Completed Tasks:")
#     for task in tasks["completed"]:
#         print(f"  ✔ {task}")

# # Main menu
# def main():
#     tasks = load_tasks()

#     while True:
#         print("\n📝 Daily Task Manager")
#         print("1. Add Task")
#         print("2. Remove Task")
#         print("3. Mark Task as Completed")
#         print("4. View Tasks")
#         print("5. Exit")

#         choice = input("Enter your choice (1-5): ")

#         if choice == "1":
#             task = input("Enter task: ")
#             add_task(tasks, task)
#         elif choice == "2":
#             task = input("Enter task to remove: ")
#             remove_task(tasks, task)
#         elif choice == "3":
#             task = input("Enter task to mark as completed: ")
#             complete_task(tasks, task)
#         elif choice == "4":
#             list_tasks(tasks)
#         elif choice == "5":
#             print("👋 Exiting Task Manager. See you later!")
#             break
#         else:
#             print("⚠ Invalid choice. Please enter a number between 1-5.")

# if __name__ == "__main__":
#     main()
