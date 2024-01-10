##################################################################
# Chandler Erickson                                              #
# PCAP Preparation Course                                        #
# 01/01/2023                                                     #
# Mini-Project: To-do List                                       #
# List Class: create or load list file and manage tasks for list #
##################################################################

from todo_task import Task
import uuid
import sys

# List Class which allows for easy manipulation of lists
# Object Variables: the User's specified list name (list_name), list of object's tasks (tasks)
# Methods: show_tasks, add_task, complete_task
class List:
    def __init__(self, list_name="todo_list.txt"):
        self.list_name = list_name
        self.tasks = []  # Initialized when main_menu.py runs show_tasks()

    # Check for saved data with list_name. If data is found, create task objects for each line (task) in
    # file and add to tasks list. If data is not found, create a new file with list_name.
    def show_tasks(self):
        self.tasks = []
        print("Your tasks:")
        try:  # Try to find previous data under list_name and initialize tasks
            stream = open(self.list_name, 'r')
            line = stream.readline()
            while line != '':
                line = line.rstrip().split('`')
                self.tasks.append(Task(line[0], line[1], line[2]))  # Add a task object for each line to tasks
                line = stream.readline()
            stream.close()
        except FileNotFoundError:
            stream = open(self.list_name, 'w')  # No previous data found under list_name, create new file
            stream.close()
        for task in self.tasks:
            print('-', task)

    # Add a new task to the list
    def add_task(self):
        print("\n[ADD TASK]")

        task_id = str(uuid.uuid4())[0:4]  # Assign new task a random 4 character ID code

        try:
            task_name = input("What's the task (max 40 characters)? ")  # Get task description
            task_name = task_name.lstrip().rstrip()
            task_name = task_name[0:40]

            deadline = input("What's the deadline? ")  # Get task deadline
            deadline = deadline.lstrip().rstrip()
            deadline = deadline[0:40]

            stream = open(self.list_name, 'a')  # Append new task to list
            stream.write(task_id + '`' + task_name + '`' + deadline + '\n')
            stream.close()
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit()
        except Exception as e:
            print(f"Something happened... {e.args[0]}. I was unable to add that task.")

        return 0

    # Complete a task and remove it from the list
    # - Returns completed task name or 0 if task could not be identified with User's ID input
    def complete_task(self):
        print("\n[COMPLETE TASK]")
        try:
            completed_task = input("Enter the ID to complete: ")  # User must enter ID of task to complete
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit()
        for task in self.tasks:
            if completed_task == task.task_id:
                completed_name = task.task_name  # Task is found
                self.tasks.remove(task)          # and removed from list of tasks
                break
        else:
            return 0  # Could not find task

        stream = open(self.list_name, 'w')  # If task is found and removed, tasks must be rewritten to list_name file
        for task in self.tasks:
            stream.write(task.task_id + '`' + task.task_name + '`' + task.deadline + '\n')
        stream.close()

        return completed_name
