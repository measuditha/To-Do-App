import tkinter as tk
import csv
from tkinter import messagebox
from todo_window import open_todo_window

signup_window = None

# Function to save user details to a CSV file
def save_to_csv(email, username, password):
    with open('users.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, username, password])

# Function to clear all entry fields in a form
def clear_signup_fields(entries):
    for entry in entries:
        entry.delete(0, tk.END)

# Function to show a confirmation popup after successful signup
def show_confirmation_popup(signup_window, entries, root):
    def on_ok_click():
        popup.destroy()
        clear_signup_fields(entries)
        signup_window.destroy()
        root.deiconify()

    popup = tk.Toplevel()
    popup.title("Confirmation")
    popup.geometry("200x100")
    tk.Label(popup, text="Signup completed").pack(side="top", fill="x", pady=10)
    ok_button = tk.Button(popup, text="OK", command=on_ok_click)
    ok_button.pack()

# Function handling the signup process
def signup(email, username, password, signup_window, entries, root):
    save_to_csv(email, username, password)
    show_confirmation_popup(signup_window, entries, root)

# Function to open the signup window
def open_signup_window(root):
    global signup_window
    root.withdraw()

    def on_signup_click():
        user_email = email_entry.get()
        user_username = username_entry.get()
        user_password = password_entry.get()
        signup(user_email, user_username, user_password, signup_window, [email_entry, username_entry, password_entry], root)

    signup_window = tk.Toplevel()
    signup_window.title("Signup Page")
    signup_window.geometry("300x200")

    form_frame = tk.Frame(signup_window)
    form_frame.pack(padx=10, pady=10)

    # Creating form fields for signup
    email_label = tk.Label(form_frame, text="Email")
    email_label.grid(row=0, column=0, pady=5)
    email_entry = tk.Entry(form_frame)
    email_entry.grid(row=0, column=1, pady=5)

    username_label = tk.Label(form_frame, text="Username")
    username_label.grid(row=1, column=0, pady=5)
    username_entry = tk.Entry(form_frame)
    username_entry.grid(row=1, column=1, pady=5)

    password_label = tk.Label(form_frame, text="Password")
    password_label.grid(row=2, column=0, pady=5)
    password_entry = tk.Entry(form_frame, show="*")
    password_entry.grid(row=2, column=1, pady=5)

    signup_button = tk.Button(form_frame, text="Sign Up", command=on_signup_click)
    signup_button.grid(row=3, column=1, pady=10)

# Function to reopen the login window
def open_login_window(root):
    try:
        signup_window.destroy()
    except tk.TclError:
        pass
    root.deiconify()

# Function to check user credentials
def check_credentials(username, password):
    with open('users.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if username == row[1] and password == row[2]:
                return True
        return False

# Function to handle the login process
def login(username, password, root):
    if check_credentials(username, password):
        messagebox.showinfo("Success", "User login successful", parent=root)
        root.withdraw()
        open_todo_window()
    else:
        messagebox.showerror("Failure", "Login unsuccessful. Please check username and password", parent=root)

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login Page")
    root.geometry("300x200")

    form_frame = tk.Frame(root)
    form_frame.pack(padx=10, pady=10)

    # Creating form fields for login
    username_label = tk.Label(form_frame, text="Username")
    username_label.grid(row=0, column=0, pady=5)
    username_entry = tk.Entry(form_frame)
    username_entry.grid(row=0, column=1, pady=5)

    password_label = tk.Label(form_frame, text="Password")
    password_label.grid(row=1, column=0, pady=5)
    password_entry = tk.Entry(form_frame, show="*")
    password_entry.grid(row=1, column=1, pady=5)

    login_button = tk.Button(form_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), root))
    login_button.grid(row=2, column=1, pady=10)

    create_account_link = tk.Button(form_frame, text="Create an Account", relief="flat", command=lambda: open_signup_window(root))
    create_account_link.grid(row=3, column=1, pady=10)

    root.mainloop()
