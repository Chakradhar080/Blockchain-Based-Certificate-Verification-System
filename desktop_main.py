import ttkbootstrap as tb
from ttkbootstrap.constants import *
import hashlib
import os
import ui_admin
import ui_student

CRED_FILE = 'credentials.txt'

def save_credentials(username, password):
    with open(CRED_FILE, 'a') as f:
        f.write(f"{username},{hashlib.sha256(password.encode()).hexdigest()}\n")

def check_credentials(username, password):
    if not os.path.exists(CRED_FILE):
        return False
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    with open(CRED_FILE, 'r') as f:
        for line in f:
            u, p = line.strip().split(',')
            if u == username and p == hashed_pw:
                return True
    return False

def signup_window():
    signup = tb.Toplevel()
    signup.title("Student Sign-Up")
    signup.geometry("600x450")

    frame = tb.Frame(signup, padding=40)
    frame.pack(expand=True)

    tb.Label(frame, text="Username:", font=("Courier", 18)).grid(row=0, column=0, pady=10, sticky="e")
    entry_user = tb.Entry(frame, width=30, font=("Courier", 16))
    entry_user.grid(row=0, column=1, pady=10)

    tb.Label(frame, text="Password:", font=("Courier", 18)).grid(row=1, column=0, pady=10, sticky="e")
    entry_pass = tb.Entry(frame, show='*', width=30, font=("Courier", 16))
    entry_pass.grid(row=1, column=1, pady=10)

    def register():
        u = entry_user.get()
        p = entry_pass.get()
        if len(u) < 3 or len(p) < 3:
            tb.dialogs.Messagebox.show_error("Minimum 3 characters required.", "Error")
            return
        save_credentials(u, p)
        tb.dialogs.Messagebox.show_info("Sign-Up successful! Now Login.", "Success")
        signup.destroy()

    tb.Button(frame, text="Register", command=register, bootstyle="success", width=24, padding=10).grid(row=2, column=0, columnspan=2, pady=30)

def login_window():
    root = tb.Window(themename="superhero")
    root.title("Login - Certificate System")
    root.state('zoomed')

    main_frame = tb.Frame(root, padding=50)
    main_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Adding header for the blockchain certificate validation
    tb.Label(main_frame, text="BLOCKCHAIN BASED CERTIFICATE VALIDATION", font=("Courier", 36, "bold")).grid(row=0, column=0, columnspan=2, pady=15)
    tb.Label(main_frame, text="Login", font=("Courier", 36, "bold")).grid(row=1, column=0, columnspan=2, pady=10)

    # Username
    tb.Label(main_frame, text="Username:", font=("Courier", 20)).grid(row=2, column=0, pady=5, sticky='e')
    entry_user = tb.Entry(main_frame, font=("Courier", 18), width=30)
    entry_user.grid(row=2, column=1, pady=3)  # Reduced padding between label and textbox

    # Password
    tb.Label(main_frame, text="Password:", font=("Courier", 20)).grid(row=3, column=0, pady=5, sticky='e')
    entry_pass = tb.Entry(main_frame, show="*", font=("Courier", 18), width=30)
    entry_pass.grid(row=3, column=1, pady=3)  # Reduced padding between label and textbox

    # Role
    tb.Label(main_frame, text="Role:", font=("Courier", 20)).grid(row=4, column=0, pady=5, sticky='e')
    role_var = tb.StringVar()
    role_dropdown = tb.Combobox(main_frame, textvariable=role_var, values=["Admin", "Student"], font=("Courier", 18), width=28)
    role_dropdown.grid(row=4, column=1, pady=3)  # Reduced padding between label and selection box
    role_dropdown.current(1)

    # Login function
    def login():
        user = entry_user.get()
        pw = entry_pass.get()
        role = role_var.get()

        if role.lower() == 'admin':
            if user == 'admin' and pw == 'admin123':
                root.withdraw()  # Hide login window instead of destroying it
                ui_admin.launch_admin_ui()  # Launch admin UI
            else:
                tb.dialogs.Messagebox.show_error("Invalid admin credentials", "Login Failed")
        else:
            if check_credentials(user, pw):
                root.withdraw()  # Hide login window instead of destroying it
                ui_student.launch_student_ui(user)  # Launch student UI
            else:
                tb.dialogs.Messagebox.show_error("Invalid student credentials", "Login Failed")

    # Buttons
    btn_frame = tb.Frame(main_frame)
    btn_frame.grid(row=5, column=0, columnspan=2, pady=15)

    tb.Button(btn_frame, text="Login", command=login, bootstyle="primary", width=26, padding=10).grid(row=0, column=0, padx=12)
    tb.Button(btn_frame, text="Sign Up", command=signup_window, bootstyle="info-outline", width=26, padding=10).grid(row=0, column=1, padx=12)

    root.mainloop()

if __name__ == '__main__':
    login_window()
