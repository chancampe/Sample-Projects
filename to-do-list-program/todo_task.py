##########################################################################
# Chandler Erickson                                                      #
# PCAP Preparation Course                                                #
# 01/01/2023                                                             #
# Mini-Project: To-do List                                               #
# Task Class: Stores task data and can return a neat string of task data #
##########################################################################

# Task Class which assists in managing and printing tasks
# - Object Variables: random 4 character ID (task_id), description (task_name), completion deadline (deadline)
# - Methods: __str__ allows List object's show_tasks method to display each task
class Task:
    def __init__(self, task_id="0000", task_name="default", deadline=""):
        self.task_id = task_id
        self.task_name = task_name
        self.deadline = deadline

    def __str__(self):
        return "{:4s}  |  {:-<41s} {:<40s}".format(self.task_id, self.task_name + ' ', self.deadline)
