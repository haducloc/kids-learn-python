from datetime import date
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk

# Add project root to the Python path for importing custom modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local imports
import emp_db
import ui_util
import parse_util
import employee_edit_form


# ---------- Search Execution (Threaded) ----------


def search(name_var, dob_var, user_type_var, tree, win, message_text):
    """Trigger a background search and display 'Searching...'"""
    ui_util.set_text_readonly(message_text, "Searching...")

    # Run DB query in a separate thread to avoid freezing the UI
    threading.Thread(
        target=run_query,
        args=(name_var, dob_var, user_type_var, tree, win, message_text),
        daemon=True,
    ).start()


def run_query(name_var, dob_var, user_type_var, tree, win, message_text):
    """Run the actual DB query and update the UI when done."""
    name = parse_util.str_or_none(name_var.get())
    dob = parse_util.date_or_none(dob_var.get())
    user_type = parse_util.int_or_none(user_type_var.get())

    results = emp_db.search_employees(name, dob, user_type)

    # Schedule update of TreeView in main thread
    win.after(0, lambda: update_tree(results, tree, message_text))


def update_tree(rows, tree, message_text):
    """Clear and populate the TreeView with new results."""
    tree.delete(*tree.get_children())
    tree.data_source = rows

    if not rows:
        # Display fallback row when no results
        tree.insert("", "end", values=("No results found", "", "", ""))
        ui_util.set_text_readonly(message_text, "No employees found.")
    else:
        for row in rows:
            emp_id, name, dob, user_type = row
            formatted = (emp_id, name, dob, user_type)
            tree.insert("", "end", values=formatted)

        ui_util.set_text_readonly(message_text, f"{len(rows)} employee(s) found.")


# ---------- Main Search Form UI ----------


def open_search_form(parent):
    """Create and show the search form window."""
    win = tk.Toplevel(parent)
    win.title("Search Employees")

    # Center the window over the parent
    w, h = 960, 480
    x, y = ui_util.compute_win_pos(w, h, parent)
    win.geometry(f"{w}x{h}+{x}+{y}")

    # Grid layout configuration
    win.columnconfigure(0, weight=1, minsize=200)
    win.columnconfigure(1, weight=2, minsize=400)
    win.rowconfigure(5, weight=1)

    # --- Form Variables ---
    name_var = tk.StringVar()
    dob_var = tk.StringVar()
    user_type_var = tk.StringVar()

    # --- Row 0: Message Display Area ---
    message_text = tk.Text(win, height=3, wrap="word", bg="gray", fg="white")
    message_text.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    message_text.configure(state="disabled")

    # --- Row 1: Name Field ---
    tk.Label(win, text="Name").grid(row=1, column=0, sticky="e", padx=10, pady=5)
    name_txt = tk.Entry(win, textvariable=name_var)
    name_txt.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

    # --- Row 2: Date of Birth Field ---
    tk.Label(win, text="Date of Birth (YYYY-MM-DD)").grid(
        row=2, column=0, sticky="e", padx=10, pady=5
    )
    dob_txt = tk.Entry(win, textvariable=dob_var)
    dob_txt.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

    # --- Row 3: User Type Field ---
    tk.Label(win, text="User Type").grid(row=3, column=0, sticky="e", padx=10, pady=5)
    user_type_txt = tk.Entry(win, textvariable=user_type_var)
    user_type_txt.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

    # --- Row 4: Search Button ---
    tk.Button(
        win,
        text="Search",
        command=lambda: search(
            name_var, dob_var, user_type_var, tree, win, message_text
        ),
    ).grid(row=4, column=0, columnspan=2, pady=10)

    # --- Row 5: Results TreeView ---
    frame = ttk.Frame(win)
    frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    columns = ("emp_id", "name", "dob", "user_type")
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w", width=120)

    tree.grid(row=0, column=0, sticky="nsew")

    # --- Vertical Scrollbar ---
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # --- Double-Click on Row to Edit Employee ---
    tree.bind("<Double-1>", lambda e: on_treeview_double_click(e, win))

    # --- Enter Key Triggers Search ---
    for entry in (name_txt, dob_txt, user_type_txt):
        entry.bind(
            "<Return>",
            lambda e: search(name_var, dob_var, user_type_var, tree, win, message_text),
        )

    name_txt.focus_set()
    return win


# ---------- Double-Click Row Handler ----------


def on_treeview_double_click(event, win):
    """Handle double-click on a TreeView row to open the edit form with original data."""
    tree = event.widget
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")

    # Guard: Skip dummy row
    if values[0] == "No results found":
        return

    # Find the index of the selected row
    children = tree.get_children()
    try:
        index = children.index(selected)
        row = tree.data_source[index] if hasattr(tree, "data_source") else values
    except (ValueError, IndexError):
        return  # Selected item not found in data_source

    # Unpack and parse row from data_source
    emp_id, name, dob, user_type = row

    win.destroy()

    # Open the edit form with pre-filled data
    employee_edit_form.open_edit_form(win.master, emp_id, name, dob, user_type)
