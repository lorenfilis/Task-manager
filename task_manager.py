# **** Task Manager ****
# A program that allows you to add, view and edit tasks.
# Assign tasks to different users and generate reports statistics.

# Completed using course materials and mentor calls.

# Notes:
# Use the following username and password to access the admin rights
# username: admin
# password: password


# =====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


# Adds a new user to the user.txt file
def reg_user():
    while True:
        new_username = input("New Username: ")
        if new_username in username_password.keys():  # checks the username has not been taken
            print("Username already exists, please try a different username.")
        else:
            break
    # Requests password, confirms it and checks that they are the same
    while True:
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")
        if new_password == confirm_password:
            print("New user added")
            username_password[new_username] = new_password
            # adds password to user.txt
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
                break
        else:
            print("Passwords do no match, please re-enter a password")
            continue


# Allows a user to add a new task to task.txt file
def add_task():
    # Prompt for username of the person whom the task is assigned to,
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        else:
            break
    # Enter the task details
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''

    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    # Writes the new task to the task file.
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


# Reads the tasks from task.txt file and prints them all to the console
def view_all():
    for t in task_list:
        disp_str = f"--------------------------------------------------\n"
        disp_str += f"Task: \t\t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


# Reads the task from task.txt file and prints the current users tasks to the console
# Then allows for some editing of the task
def view_mine():
    print("My Tasks:")
    current_user_tasks = [task for task in task_list if task['username'] == curr_user]

    for index, task in enumerate(current_user_tasks, start=1):
            disp_str = f"--------------------------------------------------\n"
            disp_str += f"Task Number: \t {index}\n"
            disp_str += f"Task: \t\t\t {task['title']}\n"
            disp_str += f"Assigned to: \t {task['username']}\n"
            disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {task['description']}\n"
            print(disp_str)

    while True:
        print("Select a task number to perform or enter -1 to return to the main menu: ")
        try:
            task_num = int(input())
            if task_num == -1:
                break
            elif task_num > 0 and task_num <= len(current_user_tasks):
                selected_task = current_user_tasks[task_num - 1]

            print("Selected Task:")
            disp_str = f"-------------------------------------------------------\n"
            disp_str += f"Task Number: \t {task_num}\n"
            disp_str += f"Task: \t\t\t {selected_task['title']}\n"
            disp_str += f"Assigned to: \t {selected_task['username']}\n"
            disp_str += f"Date Assigned: \t {selected_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {selected_task['description']}\n"
            disp_str += f"Completed: \t\t {'Yes' if selected_task['completed'] else 'No'}\n"
            print(disp_str)

        except Exception:
            print("Invalid input.")
            continue

        print("Task menu:")
        print("1. Mark as completed")
        print("2. Edit task")
        task_menu = input("Please enter 1 or 2: ")

        if task_menu == '1':
            if selected_task['completed']:
                print("Task is already complete.")
            else:
                selected_task['completed'] = True
                print("Task marked as completed. Well done!")
        elif task_menu == '2':
            if selected_task['completed']:
                print("Sorry, cannot edit once task is already completed.")
            else:
                print("Edit menu:")
                print("1. Edit username")
                print("2. Edit due date")
                edit_menu = input("Please enter 1 or 2: ")

                if edit_menu == '1':
                    while True:
                        new_username = input("Enter a new username: ")
                        if new_username in username_password.keys():
                            selected_task['username'] = new_username
                            print("Username updated.")
                            break
                        else:
                            print('Username does not exists')
                elif edit_menu == '2':
                    new_due_date = input("Enter a new due date (YYYY-MM-DD): ")
                    try:
                        due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT).date()
                        selected_task['due_date'] = due_date
                        print("Due date updated.")
                    except ValueError:
                        print("Invalid date format. Please try again.")
                else:
                    print("Invalid option. Please try again.")
        else:
            print("Invalid action. Please try again.")

        # Overwrites task file with updated tasks
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))


# Creating two reports with the task statistics
def reports():
    # Generate task Overview Report
    total_tasks = len(task_list)
    completed_tasks = sum(t['completed'] for t in task_list)
    uncompleted_tasks = total_tasks - completed_tasks

    overdue_tasks = sum(t['completed'] is False and t['due_date'] < datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) for t in task_list)
    incomplete_percentage = percentage(uncompleted_tasks, total_tasks)
    overdue_percentage = percentage(overdue_tasks, total_tasks)

    task_overview = f"Task Overview\n" \
                    f"----------------\n" \
                    f"Total tasks: {total_tasks}\n" \
                    f"Completed tasks: {completed_tasks}\n" \
                    f"Uncompleted tasks: {uncompleted_tasks}\n" \
                    f"Overdue tasks: {overdue_tasks}\n" \
                    f"Incomplete percentage: {incomplete_percentage}%\n" \
                    f"Overdue percentage: {overdue_percentage}%"

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(task_overview)

    # Generate User Overview Report
    total_users = len(username_password.keys())
    user_overview = f"User Overview\n" \
                    f"----------------\n" \
                    f"Total users: {total_users}\n"

    for username in username_password.keys():
        user_tasks = [t for t in task_list if t['username'] == username]
        total_user_tasks = len(user_tasks)
        completed_user_tasks = sum(t['completed'] for t in user_tasks)
        uncompleted_user_tasks = total_user_tasks - completed_user_tasks
        overdue_user_tasks = sum(t['completed'] is False and t['due_date'] < datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) for t in user_tasks)

        percentage_total_user_tasks = percentage(total_user_tasks, total_tasks)
        percentage_completed_user_tasks = percentage(completed_user_tasks, total_user_tasks)
        percentage_uncompleted_user_tasks = percentage(uncompleted_user_tasks, total_user_tasks)
        percentage_overdue_user_tasks = percentage(overdue_user_tasks, total_user_tasks)

        user_overview += f"\nUsername: {username}\n" \
                         f"Total tasks assigned: {total_user_tasks}\n" \
                         f"Percentage of total tasks: {percentage_total_user_tasks:.2f}%\n" \
                         f"Percentage of tasks completed: {percentage_completed_user_tasks:.2f}%\n" \
                         f"Percentage of tasks uncompleted: {percentage_uncompleted_user_tasks:.2f}%\n" \
                         f"Percentage of tasks uncompleted and overdue: {percentage_overdue_user_tasks:.2f}%\n"

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(user_overview)


    print("Reports generated successfully.")


# A function for working out percentages and handling errors
def percentage(x, y):
    try:
        answer = (x / y) * 100
        return round(answer)
    except ZeroDivisionError:
        return 0

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)



# ====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    if curr_user == "admin":
        print()
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()
    else:
        print()
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        reports()
    elif menu == 'ds' and curr_user == 'admin':
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        # The reports are generated if they don't already exist.
        if not os.path.exists("task_overview.txt" or "user_overview.txt"):
            reports()

        # Info is read from the report files and printed for user
        with open("user_overview.txt", 'r') as user_overview_file:
            user_lines = user_overview_file.read()
            print(user_lines)
        with open("task_overview.txt", 'r') as task_overview_file:
            task_lines = task_overview_file.read()
            print(task_lines)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")