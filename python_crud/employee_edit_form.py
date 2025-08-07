import os
import sys
from datetime import date
import tkinter as tk
from tkinter import ttk

# Add project root to the Python path for importing custom modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local imports
import emp_db
import user_type_db
import ui_util
import parse_util

# ---------- Save Handler (Insert or Update) ----------


def save_employee(emp_id, name_var, dob_var, user_type_var, win, message_text):
    """Handles saving or updating the employee form."""

    # Clear previous status or error messages
    ui_util.set_text_readonly(message_text, "")

    # --- Get and clean input values ---
    name = parse_util.str_or_none(name_var.get())
    dob, dob_parsed = parse_util.try_parse_date(dob_var.get())
    user_type, type_parsed = parse_util.try_parse_int(user_type_var.get())

    # --- Validate fields ---
    errors = []

    if not name:
        errors.append("Name is required.")

    if not type_parsed:
        errors.append("User Type is invalid.")
    elif user_type is None:
        errors.append("User Type is required.")

    if dob is not None and not dob_parsed:
        errors.append("Date of Birth is invalid.")

    if errors:
        # Show validation errors in message text area
        ui_util.set_text_readonly(message_text, "\n".join(errors))
        return

    # --- Save or update logic ---
    if emp_id is None:
        # Insert new employee
        err = emp_db.insert_employee(name, dob, user_type)
        success_msg = "Employee added successfully!"
    else:
        # Update existing employee
        err = emp_db.update_employee(emp_id, name, dob, user_type)
        success_msg = "Employee updated successfully!"

    # --- Handle DB operation result ---
    if err:
        ui_util.set_text_readonly(message_text, err)
    else:
        ui_util.set_text_readonly(message_text, success_msg)
        # Close the form window after short delay
        win.after(1000, win.destroy)


# ---------- Shared Add/Edit Form UI ----------


def open_edit_form(
    parent,
    emp_id: int | None = None,
    name: str | None = None,
    dob: date | None = None,
    user_type: int | None = None,
):
    """Creates the Add/Edit Employee popup form."""

    is_edit = emp_id is not None
    win = tk.Toplevel(parent)
    win.title("Edit Employee" if is_edit else "Add New Employee")

    # --- Position the window centered over parent ---
    w, h = 960, 480
    x, y = ui_util.compute_win_pos(w, h, parent)
    win.geometry(f"{w}x{h}+{x}+{y}")

    # --- Configure layout grid ---
    win.columnconfigure(0, weight=1, minsize=200)
    win.columnconfigure(1, weight=2, minsize=400)

    # --- Form input variables ---
    name_var = tk.StringVar(value=name)
    dob_var = tk.StringVar(value=str(dob) if dob else "")
    user_type_var = tk.StringVar(value=str(user_type) if user_type is not None else "")

    # --- Row 0: Message text area (readonly) ---
    message_text = tk.Text(win, height=3, wrap="word", bg="gray", fg="white")
    message_text.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    message_text.configure(state="disabled")

    # --- Row 1: Name input ---
    tk.Label(win, text="Name").grid(row=1, column=0, sticky="e", padx=10, pady=10)
    name_entry = tk.Entry(win, textvariable=name_var)
    name_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

    # --- Row 2: Date of Birth input (optional) ---
    tk.Label(win, text="Date of Birth (YYYY-MM-DD)").grid(
        row=2, column=0, sticky="e", padx=10, pady=10
    )
    dob_entry = tk.Entry(win, textvariable=dob_var)
    dob_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

    # --- Row 3: User Type input (required) ---
    tk.Label(win, text="User Type (int)").grid(
        row=3, column=0, sticky="e", padx=10, pady=10
    )
    user_type_entry = tk.Entry(win, textvariable=user_type_var)
    user_type_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=10)

    # --- Row 4: Save or Update button ---
    action_label = "Update" if is_edit else "Save"
    save_btn = ttk.Button(
        win,
        text=action_label,
        command=lambda: save_employee(
            emp_id, name_var, dob_var, user_type_var, win, message_text
        ),
    )
    save_btn.grid(row=4, column=0, columnspan=2, pady=20)

    # --- Auto-focus on the name field for user convenience ---
    name_entry.focus_set()

    return win
