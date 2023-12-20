import csv
import tkinter as tk
from tkinter import messagebox

# Function to open the main task manager window
def open_todo_window():
    root = tk.Tk()
    root.title("Task Manager")
    root.geometry("752x506")

    # Header frame containing navigation buttons
    header_frame = tk.Frame(root, bg='black', height=30)
    header_frame.pack(side='top', fill='x')

    # Navigation buttons
    nav_buttons = ['Home', 'Tasks', 'About Us']
    for button in nav_buttons:
        tk.Button(header_frame, text=button, relief='flat', bg='black', fg='white').pack(side='left', padx=5)

    # Search and profile icons
    search_icon = tk.Label(header_frame, text='🔍', bg='black', fg='white')
    search_icon.pack(side='right', padx=(0, 5))
    profile_icon = tk.Label(header_frame, text='👤', bg='black', fg='white')
    profile_icon.pack(side='right')

    # Function to open the add task window
    def on_add_clicked():
        root.destroy()
        open_add_todo_window(on_close=open_todo_window)

    # Function to open the update task window
    def on_update_clicked(task_data, row):
        root.destroy()
        open_update_todo_window(task_data, row, on_close=open_todo_window)

    # Function to refresh the task list displayed in the main window
    def refresh_task_list():
        for widget in tasks_frame.winfo_children():
            widget.destroy()
        try:
            with open('todo.csv', newline='') as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    add_task_to_frame(row, i)
        except FileNotFoundError:
            messagebox.showerror("Error", "todo.csv not found. Please make sure the file exists.")

    # Function to add a task to the main window
    def add_task_to_frame(task_data, row_index):
        task_frame = tk.Frame(tasks_frame, bg='white', borderwidth=1, relief='groove')
        task_frame.pack(fill='x', padx=5, pady=5)
        for j, text in enumerate(task_data):
            tk.Label(task_frame, text=text, bg='white').grid(row=0, column=j, sticky='w', padx=5)
        tk.Button(task_frame, text='Update', bg='blue',
                  command=lambda r=task_data, i=row_index: on_update_clicked(r, i)).grid(row=0,
                                                                                     column=len(task_data) + 1,
                                                                                     padx=5)
        tk.Button(task_frame, text='Delete', bg='red', command=lambda i=row_index: on_delete_clicked(i)).grid(row=0,
                                                                                                              column=len(
                                                                                                                  task_data) + 2,
                                                                                                              padx=5)

    # Function to handle task deletion
    def on_delete_clicked(row_index):
        try:
            with open('todo.csv', 'r') as file:
                tasks = list(csv.reader(file))
            del tasks[row_index]
            with open('todo.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(tasks)
            refresh_task_list()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Main content frame
    content_frame = tk.Frame(root, bg='white')
    content_frame.pack(expand=True, fill='both', padx=20, pady=(5, 20))

    # Filter frame containing filter options
    filter_frame = tk.Frame(content_frame, bg='white')
    filter_frame.pack(fill='x', pady=(0, 10))

    # Add task button
    add_button = tk.Button(filter_frame, text='Add', bg='green', fg='white', command=on_add_clicked)
    add_button.pack(side='left', padx=(0, 10))

    # Function to filter tasks based on user input
    def filter_tasks():
        filter_date = date_entry.get()
        filter_type = type_entry.get()
        try:
            with open('todo.csv', newline='') as file:
                reader = csv.reader(file)
                for widget in tasks_frame.winfo_children():
                    widget.destroy()
                for i, row in enumerate(reader):
                    if filter_date in row[0] and filter_type in row[3]:
                        add_task_to_frame(row, i)
        except FileNotFoundError:
            messagebox.showerror("Error", "todo.csv not found. Please make sure the file exists.")

    # Apply filter button
    filter_button = tk.Button(filter_frame, text='Apply Filter', command=filter_tasks)
    filter_button.pack(side='right', padx=5)

    # Filter label and input fields
    filter_label = tk.Label(filter_frame, text='Filter', bg='white')
    filter_label.pack(side='left', padx=(0, 10))
    date_entry = tk.Entry(filter_frame, bg='white', width=20)
    date_entry.pack(side='left', padx=(0, 10))
    type_entry = tk.Entry(filter_frame, bg='white', width=20)
    type_entry.pack(side='left')

    # Canvas and scrollbar for displaying tasks
    tasks_canvas = tk.Canvas(content_frame, bg='white')
    tasks_scrollbar = tk.Scrollbar(content_frame, orient='vertical', command=tasks_canvas.yview)
    tasks_scrollbar.pack(side='right', fill='y')
    tasks_canvas.pack(side='left', fill='both', expand=True)
    tasks_canvas.configure(yscrollcommand=tasks_scrollbar.set)

    # Frame to hold tasks
    tasks_frame = tk.Frame(tasks_canvas, bg='white')
    tasks_canvas.create_window((0, 0), window=tasks_frame, anchor='nw')

    # Load tasks from 'todo.csv' and display them
    try:
        with open('todo.csv', newline='') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                task_frame = tk.Frame(tasks_frame, bg='white', borderwidth=1, relief='groove')
                task_frame.pack(fill='x', padx=5, pady=5)

                for j, text in enumerate(row):
                    tk.Label(task_frame, text=text, bg='white').grid(row=0, column=j, sticky='w', padx=5)

                tk.Button(task_frame, text='Update', bg='blue',
                          command=lambda r=row, i=i: on_update_clicked(r, i)).grid(row=0, column=len(row) + 1, padx=5)
                tk.Button(task_frame, text='Delete', bg='red').grid(row=0, column=len(row) + 2, padx=5)
    except FileNotFoundError:
        messagebox.showerror("Error", "todo.csv not found. Please make sure the file exists.")

    # Update canvas and scroll region
    tasks_frame.update_idletasks()
    tasks_canvas.config(scrollregion=tasks_canvas.bbox('all'))

    # Refresh the task list in the main window
    refresh_task_list()

    root.mainloop()

# Function to open the add task window
def open_add_todo_window(on_close=None):
    def save_data():
        name = name_entry.get()
        priority = priority_entry.get()
        topic = topic_entry.get()
        type_ = type_entry.get()

        # Check if all fields are filled
        if not (name and priority and topic and type_):
            messagebox.showwarning("Warning", "Please fill all the fields.")
            return

        data = [name, priority, topic, type_]
        try:
            # Append the task data to 'todo.csv' file
            with open('todo.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)
            messagebox.showinfo("Success", "Data added successfully!")

            # Clear the input fields
            name_entry.delete(0, tk.END)
            priority_entry.delete(0, tk.END)
            topic_entry.delete(0, tk.END)
            type_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def on_cancel():
        root.destroy()
        if on_close:
            on_close()

    root = tk.Tk()
    root.title("To-Do App")

    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    # Input fields for task details
    name_label = tk.Label(main_frame, text="Name")
    name_entry = tk.Entry(main_frame, width=50)
    priority_label = tk.Label(main_frame, text="Priority")
    priority_entry = tk.Entry(main_frame, width=50)
    topic_label = tk.Label(main_frame, text="Topic")
    topic_entry = tk.Entry(main_frame, width=50)
    type_label = tk.Label(main_frame, text="Type")
    type_entry = tk.Entry(main_frame, width=50)

    # Grid layout for input fields and labels
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    priority_label.grid(row=1, column=0, padx=5, pady=5)
    priority_entry.grid(row=1, column=1, padx=5, pady=5)
    topic_label.grid(row=2, column=0, padx=5, pady=5)
    topic_entry.grid(row=2, column=1, padx=5, pady=5)
    type_label.grid(row=3, column=0, padx=5, pady=5)
    type_entry.grid(row=3, column=1, padx=5, pady=5)

    # Add and cancel buttons
    add_button = tk.Button(main_frame, text="Add", bg="green", command=save_data)
    cancel_button = tk.Button(main_frame, text="Cancel", bg="red", command=on_cancel)

    add_button.grid(row=4, column=0, padx=5, pady=5)
    cancel_button.grid(row=4, column=2, padx=5, pady=5)

    root.mainloop()

# Function to open the update task window
def open_update_todo_window(task_data, row_index, on_close=None):
    def save_updated_data():
        updated_data = [name_entry.get(), priority_entry.get(), topic_entry.get(), type_entry.get()]
        with open('todo.csv', 'r') as file:
            tasks = list(csv.reader(file))
        tasks[row_index] = updated_data
        with open('todo.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(tasks)
        messagebox.showinfo("Success", "Task updated successfully!")
        root.destroy()
        if on_close:
            on_close()

    root = tk.Tk()
    root.title("Update Task")

    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    # Input fields for updated task details
    name_label = tk.Label(main_frame, text="Name")
    name_entry = tk.Entry(main_frame, width=50)
    priority_label = tk.Label(main_frame, text="Priority")
    priority_entry = tk.Entry(main_frame, width=50)
    topic_label = tk.Label(main_frame, text="Topic")
    topic_entry = tk.Entry(main_frame, width=50)
    type_label = tk.Label(main_frame, text="Type")
    type_entry = tk.Entry(main_frame, width=50)

    # Set initial values in input fields
    name_entry.insert(0, task_data[0])
    priority_entry.insert(0, task_data[1])
    topic_entry.insert(0, task_data[2])
    type_entry.insert(0, task_data[3])

    # Grid layout for input fields and labels
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    priority_label.grid(row=1, column=0, padx=5, pady=5)
    priority_entry.grid(row=1, column=1, padx=5, pady=5)
    topic_label.grid(row=2, column=0, padx=5, pady=5)
    topic_entry.grid(row=2, column=1, padx=5, pady=5)
    type_label.grid(row=3, column=0, padx=5, pady=5)
    type_entry.grid(row=3, column=1, padx=5, pady=5)

    # Update and cancel buttons
    update_button = tk.Button(main_frame, text="Update", bg="blue", command=save_updated_data)
    update_button.grid(row=4, column=0, padx=5, pady=5)

    cancel_button = tk.Button(main_frame, text="Cancel", bg="red", command=root.destroy)
    cancel_button.grid(row=4, column=2, padx=5, pady=5)

    root.mainloop()
