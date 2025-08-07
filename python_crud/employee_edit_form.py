# employee_edit_form.py

import tkinter as tk
from tkinter import ttk
import emp_db
import ui_util


# ---------- Save Handler (Insert or Update) ----------

def save_employee(emp_id, name_var, dob_var, user_type_var, win, message_text):
    # Clear previous messages
    ui_util.set_text_readonly(message_text, "")

    # Get trimmed input values
    name = name_var.get().strip()
    dob = dob_var.get().strip()
    user_type_str = user_type_var.get().strip()

    # Validate fields
    errors = []
    if not name:
        errors.append("Name is required.")
    if not user_type_str:
        errors.append("User Type is required.")
    elif not user_type_str.isdigit():
        errors.append("User Type must be an integer.")

    if errors:
        ui_util.set_text_readonly(message_text, "\n".join(errors))
        return

    user_type = int(user_type_str)

    # Insert or Update employee record
    if emp_id is None:
        err = emp_db.insert_employee(name, dob or None, user_type)
        success_msg = "Employee added successfully!"
    else:
        err = emp_db.update_employee(emp_id, name, dob or None, user_type)
        success_msg = "Employee updated successfully!"

    if err:
        ui_util.set_text_readonly(message_text, err)
    else:
        ui_util.set_text_readonly(message_text, success_msg)
        win.after(1000, win.destroy)


# ---------- Shared Add/Edit Form ----------

def open_edit_form(parent, emp_id=None, name="", dob="", user_type=None):
    is_edit = emp_id is not None
    win = tk.Toplevel(parent)
    win.title("Edit Employee" if is_edit else "Add New Employee")

    # Center and size the window
    w, h = 960, 480
    x, y = ui_util.compute_win_pos(w, h, parent)
    win.geometry(f"{w}x{h}+{x}+{y}")

    # ---------- Grid Setup ----------
    win.columnconfigure(0, weight=1, minsize=200)
    win.columnconfigure(1, weight=2, minsize=400)

    # ---------- Form Variables ----------
    name_var = tk.StringVar(value=name)
    dob_var = tk.StringVar(value=dob)
    user_type_var = tk.StringVar(value=str(user_type) if user_type is not None else "")

    # ---------- Row 0: Message Text ----------
    message_text = tk.Text(win, height=3, wrap="word", bg="gray", fg="white")
    message_text.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    message_text.configure(state="disabled")

    # ---------- Row 1: Name ----------
    tk.Label(win, text="Name").grid(row=1, column=0, sticky="e", padx=10, pady=10)
    name_entry = tk.Entry(win, textvariable=name_var)
    name_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

    # ---------- Row 2: Date of Birth (Nullable) ----------
    tk.Label(win, text="Date of Birth (YYYY-MM-DD)").grid(
        row=2, column=0, sticky="e", padx=10, pady=10
    )
    dob_entry = tk.Entry(win, textvariable=dob_var)
    dob_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

    # ---------- Row 3: User Type ----------
    tk.Label(win, text="User Type (int)").grid(row=3, column=0, sticky="e", padx=10, pady=10)
    user_type_entry = tk.Entry(win, textvariable=user_type_var)
    user_type_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=10)

    # ---------- Row 4: Save/Update Button ----------
    action_label = "Update" if is_edit else "Save"
    save_btn = ttk.Button(
        win,
        text=action_label,
        command=lambda: save_employee(
            emp_id, name_var, dob_var, user_type_var, win, message_text
        ),
    )
    save_btn.grid(row=4, column=0, columnspan=2, pady=20)

    # Auto-focus first field
    name_entry.focus_set()

    return win
