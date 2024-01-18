import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk  # Import the ttk module for themed widgets



class RegistrationWindow:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window
        self.root.title("Register")

        self.new_username_var = tk.StringVar()
        self.new_password_var = tk.StringVar()

        tk.Label(root, text="New Username:").pack(pady=5)
        tk.Entry(root, textvariable=self.new_username_var).pack(pady=5)
        tk.Label(root, text="New Password:").pack(pady=5)
        tk.Entry(root, textvariable=self.new_password_var, show="*").pack(pady=5)
        tk.Button(root, text="Register", command=self.register, bg="#8F8").pack(pady=10)

    def register(self):
        new_username = self.new_username_var.get()
        new_password = self.new_password_var.get()

        # Check if username already exists
        if new_username in self.login_window.users:
            self.show_error("Username already exists! Please choose a different username.")
        else:
            # Add new user to the user system
            self.login_window.users[new_username] = new_password
            self.show_info("Registration successful! You can now log in.")
            self.root.destroy()  # Close the registration window


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(root, text="Username:").pack(pady=5)
        tk.Entry(root, textvariable=self.username_var).pack(pady=5)
        tk.Label(root, text="Password:").pack(pady=5)
        tk.Entry(root, textvariable=self.password_var, show="*").pack(pady=5)
        tk.Button(root, text="Login", command=self.login, bg="#8F8").pack(pady=10)

        # Button to open the registration window
        tk.Button(root, text="Register", command=self.open_registration, bg="#88F").pack(pady=5)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        users = {'user1': 'password1', 'user2': 'password2'}  # Simple user system for demo

        if username in users and users[username] == password:
            self.root.destroy()
            app = TodoApp(username)
            app.run()
        else:
            self.show_error("Invalid credentials! Please try again.")

    def open_registration(self):
        registration_root = tk.Tk()
        registration_window = RegistrationWindow(registration_root, self)
        registration_root.mainloop()

    def show_error(self, message):
        style = ttk.Style()
        style.configure("TButton", foreground="red", background="#F88")
        messagebox.showerror("Error", message)





class TodoApp:
    def __init__(self, username):
        self.root = tk.Tk()
        self.root.title("To-Do List App")

        self.logged_in_user = username
        self.users = {'user1': 'password1', 'user2': 'password2'}  # Simple user system for demo
        self.tasks = []

        self.task_var = tk.StringVar()
        self.serial_var = tk.IntVar()
        self.serial_var.set(1)

        # Entry for adding tasks
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Add Task:").pack(side=tk.LEFT)
        entry_task = tk.Entry(entry_frame, textvariable=self.task_var, width=30)
        entry_task.pack(side=tk.LEFT)
        tk.Button(entry_frame, text="Add", command=self.add_task).pack(side=tk.LEFT)

        # Listbox to display tasks
        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=40, height=10)
        self.listbox.pack(pady=10)

        # Buttons for editing, deleting, and clearing tasks
        tk.Button(self.root, text="Edit", command=self.edit_task, bg="#88F").pack(side=tk.LEFT, padx=5)  # Set button color
        tk.Button(self.root, text="Delete", command=self.delete_task, bg="#88F").pack(side=tk.LEFT, padx=5)  # Set button color
        tk.Button(self.root, text="Clear All", command=self.clear_all_tasks, bg="#88F").pack(side=tk.LEFT, padx=5)  # Set button color

        # Serial number Label
        tk.Label(self.root, text="Serial No.:").pack(side=tk.LEFT)
        tk.Entry(self.root, textvariable=self.serial_var, state="readonly", width=3).pack(side=tk.LEFT)

        # Done Checkbox
        self.done_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Done", variable=self.done_var).pack(side=tk.LEFT)

        # Complete Task Button
        tk.Button(self.root, text="Complete Task", command=self.complete_task, bg="#88F").pack(side=tk.LEFT)  # Set button color

        # Logout Button
        tk.Button(self.root, text="Logout", command=self.logout, bg="#F88").pack(side=tk.RIGHT, padx=10)  # Set button background color


    def add_task(self):
        task = self.task_var.get()
        if task:
            self.tasks.append({'task': task, 'done': False})
            self.update_task_list()
            #'[p0

    def delete_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            del self.tasks[task_index]
            self.update_task_list()
        else:
            self.show_warning("Please select a task to delete!")

    def clear_all_tasks(self):
        self.tasks = []
        self.update_task_list()

    def edit_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            old_task = self.tasks[task_index]['task']
            new_task = simpledialog.askstring("Edit Task", "Edit Task:", initialvalue=old_task)
            if new_task is not None:
                self.tasks[task_index]['task'] = new_task
                self.update_task_list()
        else:
            self.show_warning("Please select a task to edit!")

    def complete_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            self.tasks[task_index]['done'] = True
            self.update_task_list()
        else:
            self.show_warning("Please select a task to mark as completed!")

    def update_task_list(self):
        self.listbox.delete(0, tk.END)
        for index, task in enumerate(self.tasks, start=1):
            done_status = "[Done]" if task['done'] else ""
            self.listbox.insert(tk.END, f"{index}. {task['task']} {done_status}")

    def show_warning(self, message):
        style = ttk.Style()
        style.configure("TButton", foreground="orange", background="#FF8")  # Set button color
        messagebox.showwarning("Warning", message)

    def logout(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()
