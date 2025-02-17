import os
import sys
import win32com.client
from datetime import datetime

def create_task(script_path, python_path="C:\\Python312\\python.exe", task_name="Model Retraining Task"):
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    rootFolder = scheduler.GetFolder('\\')
    
    taskDef = scheduler.NewTask(0)
    taskDef.RegistrationInfo.Description = "Retrain machine learning model"
    taskDef.RegistrationInfo.Author = "Elwin"
    
    trigger = taskDef.Triggers.Create(1)
    trigger.StartBoundary = "2025-02-16T00:00:00"  # Set the start date and time
    trigger.DaysInterval = 8 
    
    # Create the action to run the script
    execAction = taskDef.Actions.Create(0) 
    execAction.Path = python_path
    execAction.Arguments = script_path
    
    taskDef.Principal.UserId = "SYSTEM"
    taskDef.Principal.LogonType = 3
    
    # Register the task in Task Scheduler
    rootFolder.RegisterTaskDefinition(
        task_name, 
        taskDef, 
        6,
        None,
        None,
        3
    )
    
    print(f"Task '{task_name}' has been created successfully!")

if __name__ == "__main__":
    script_path = "retrain.py"
    # Adjust this to your Python path
    python_path = "C:\\Python312\\python.exe"  
    create_task(script_path, python_path)
