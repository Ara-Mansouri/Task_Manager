import json
import os



TaskFile_json="Task.json"
def Load_Tasks():
    if os.path.exists(TaskFile_json):
        with open (TaskFile_json,"r") as file:
            tasks= json.load(file)
            if "Removed" not in tasks:
             tasks["Removed"] = []
            return tasks 
    return     {"Pending":[],"Completed":[],"Removed":[]}#یک دیکشنری با دو تا کلید که جواب کلید ها لیست است
def Save_Tasks(Tasks):
    with open(TaskFile_json,"w") as file:
        json.dump(Tasks,file,indent=4)#فایل را در قالب جیسون میریزد داخل فایل جیسون و برای فهم بهتر فاصله میندازد
        
def Add_Task(Tasks,Task):
    if Task not in Tasks["Pending"]:
        Tasks["Pending"].append(Task)
        Save_Tasks(Tasks)
        print(f"✅ Task Added Successfully!")
    else:
        print("Task is ALready in the Pending List.\nOperation Failed")
def Remove_Task(Tasks,Task):
    if Task in Tasks["Pending"]:
        Tasks["Pending"].remove(Task)
        Tasks["Removed"].append(Task)
        Save_Tasks(Tasks)
        print(f"❌ Task '{Task}' removed!")
    else:
        print(f"Task {Task} did not Found in the List")

def MarkCompleted(Tasks,Task):
    if Task in Tasks["Pending"]:
        Tasks["Pending"].remove(Task)
        Tasks["Completed"].append(Task)
        print(f"✅ Task {Task} Marked as Completed.")
        Save_Tasks(Tasks)
    else:
         print(f"⚠ Task {Task}  not found.")

def Show_All_Tasks(Tasks):
    print("\n📌 Pending Tasks:")
    if not Tasks["Pending"]:
        print("No Pending Tasks available!")
    else:    
        for Task in Tasks["Pending"]:
            print(f"- {Task}")  
    print(f"\n✔  Completed Tasks:")
    if not Tasks["Completed"]:
        print("No Completed Tasks available!")
    else:    
        for Task in Tasks["Completed"]:
            print(f"- {Task}")
    print("\n❌ Removed Tasks:")
    if not Tasks["Removed"]:
        print("No Removed Tasks available!")
    else:
        for Task in Tasks["Removed"]:
            print(f"- {Task}")   
            
def Undo_RemovedTasks(Tasks):
    if not Tasks["Removed"]:
        print("There is No Removed Tasks To undo")
    else:
        Task=Tasks["Removed"].pop()
        Tasks["Pending"].append(Task)
        print(f"Removed Task {Task} undid Successfully")
        Save_Tasks(Tasks)
        
def Empty_List(Tasks,group):
    if group in Tasks:
        Tasks[group].clear()
        Save_Tasks(Tasks)
        print(f"Group {group} Cleared successfully")
    else:
        print(f"Group {group} Doesnt Exists.")    

def main():
    
    TaskManage=  Load_Tasks()
    while True:
        print("\n📝Daily Task Manager")
        print("1.Add Tasks")
        print("2.Remove Tasks")
        print("3.View Tasks")
        print("4.Mark Tasks As Completed")
        print("5.Undo Last Removed Task")
        print("6.Clear Group")
        print("7.Exit")
    
        choice=input("Enter your choice:")

        if choice =="1":
            Task=input("Enter Your Task:")
            Add_Task(TaskManage,Task)
            TaskManage=  Load_Tasks()
        elif choice=="2":
            Task=input("Enter the Task you Wanna Remove:")
            Remove_Task(TaskManage,Task)
            TaskManage=  Load_Tasks()
        elif choice=="3":
            Show_All_Tasks(TaskManage)
        elif choice=="4":
            Task=input("Enter the Task you Wanna Mark As Completd:")
            MarkCompleted(TaskManage,Task)   
            TaskManage=  Load_Tasks()
        elif choice=="5":
            Undo_RemovedTasks(TaskManage)
            TaskManage=  Load_Tasks()
        elif choice=="6":
            group=input("Enter the Group you Wanna get Cleared (Pending, Completed, Removed):")
            Empty_List(TaskManage,group)
            TaskManage=  Load_Tasks()    
        elif choice=="7":
             print("Exit the Program")
             break    
        else:
            print("⚠Invalid Choice")   

if __name__ == "__main__":
    main()
    