#################################################################################
# Chandler Erickson                                                             #
# PCAP Preparation Course                                                       #
# 01/01/2023                                                                    #
# Mini-Project: To-do List                                                      #
# Purpose: Allow user to interact with a virtual to-do list for tracking tasks. #
#          Each task is identifiable by a unique ID and will list the task      #
#          needing completion as well as the deadline completion date.          #
#################################################################################

import glob
import os
import sys
from platform import system
from todo_list import List

# This function is run when program starts, to safely ensure program switches to
# the folder that stores lists, whether the folder is found or not.
def verify_lists_folder():
    try:  # Try to open folder of lists to look for list data.
        os.chdir(r"folder_of_lists")
    except FileNotFoundError:  # Folder does not exist. New folder_of_lists is created and used.
        os.mkdir("folder_of_lists")
        os.chdir(r"folder_of_lists")


# Displays the names of all files found in folder_of_lists and prompts User for the file (list) they would like to open.
# - Parameter (saved_files) is list of file names found in folder_of_lists
# - Input for filename (list_name) or q/Q to quit program
# - Returns list_name
def get_file_name(saved_files):
    print("\nYour lists:")
    for file in saved_files:
        print('-', file[:-4])  # Print saved list names
    try:
        # Get input for list name or q to quit
        user_input = input("\nEnter a list name or 'q' to quit: ")
        if user_input.lower().strip() == 'q':
            print("\nGoodbye!")
            sys.exit()
        else:
            # Convert input to file/list name by removing any non alnum, spaces, underscores, and hyphens.
            list_name = ''.join([char for char in user_input.lstrip().rstrip()
                                 if char.isalnum() or char in ' -_']) + ".txt"
            return list_name
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit()


# Clear screen in between menu options
def clear_screen():
    os_type = system()
    if "Windows" in os_type:
        os.system("cls")
    else:
        os.system("clear")


# Shows current tasks and prompt User to add task, complete task, delete list, or exit
# - Parameter (todo_list) is list object created from User inputted list_name
# - Input for User's choice (choice) from listed options
# - Returns choice
def list_menu(todo_list):
    bad_entry_count = 0  # If User enters 5 invalid inputs, program ends.
    choice = 0  # Must be 1, 2, 3, or 4 to select a list option

    while bad_entry_count < 5:
        print("\n==", todo_list.list_name[:-4], "==\n")

        todo_list.show_tasks()  # list object method (show_tasks) displays all current tasks for the list object

        print("\n[1] add task\n" +
              "[2] complete task\n" +
              "[3] delete list\n" +
              "[4] exit list")
        try:
            choice = int(input("Your choice: "))
            if choice not in [1, 2, 3, 4]:
                raise ValueError
            else:
                break
        except ValueError:  # If input is not 1, 2, 3, or 4; print message and try again
            bad_entry_count += 1
            clear_screen()
            print("\nInvalid input... enter a number 1–4")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit()

    if bad_entry_count == 5:  # Too many invalid inputs, end program
        print("\nThat's a lot of invalid inputs. I'm ending the program.")
        sys.exit()
    else:
        return choice


# Display a completion message when User completes a task or error message for unrecognized task ID input.
# - Parameter (task_name) is name of task being completed
def completed_task_message(task_name):
    if task_name == 0:
        clear_screen()
        print("\nI couldn't find a task with that ID")
    else:  # If a task was found with ID input and was successfully removed, print message
        message = "**************************** " + task_name + " COMPLETE! *************"
        for i in range(0, len(message)):
            print('\n' + message[i:i+20])
            clear_screen()


# Ask User to confirm their choice of deleting the current list
# - Parameter: todo_list object
# - Return choice
def delete_list(todo_list):
    clear_screen()
    print("\nPermanently delete " + todo_list.list_name[:-4] + '?')
    print("[1] yes\n" +
          "[2] no")
    try:
        choice = input("Your choice: ")
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit()
    clear_screen()
    return choice


# Main controls program flow. Program will loop until User enter q/Q from get_file_name() menu.
# - Objects and Methods: todo_list, add_task(), complete_task()
# - Function calls: verify_lists_folder(), get_file_name(saved_files), list_menu(todo_list), clear_screen()
def main():
    clear_screen()
    print("\n== TO-DO LIST PROGRAM ==")
    verify_lists_folder()  # Verify folder_of_lists

    while True:
        saved_files = glob.glob("*.txt")  # Get all file/list names from folder_of_lists
        file_name = get_file_name(saved_files)  # Get User's list name to use
        clear_screen()

        while True:
            todo_list = List(file_name)  # Create list object for User's entered list name

            list_action = list_menu(todo_list)  # Get User's choice of list action
            match list_action:
                case 1:  # Add task
                    todo_list.add_task()
                    clear_screen()
                case 2:  # Complete task
                    completed_task = todo_list.complete_task()
                    completed_task_message(completed_task)
                case 3:  # Delete list
                    confirm_delete = delete_list(todo_list)
                    if confirm_delete.strip() == '1':
                        os.remove(todo_list.list_name)
                        break
                    else:
                        continue
                case 4:  # Exit current list (go back to filename menu)
                    clear_screen()
                    break


if __name__ == '__main__':
    main()
