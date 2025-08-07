import tkinter as tk
from tkinter import ttk
import threading
import emp_db
import ui_util
import employee_edit_form

# ---------- Search Execution ----------

def search(name_var, dob_var, user_type_var, tree, win, message_text):
    ui_util.set_text_readonly(message_text, "Searching...")

    # Run DB query in background
    threading.Thread(
        target=run_query,
        args=(name_var, dob_var, user_type_var, tree, win, message_text),
        daemon=True,
    ).start()

def run_query(name_var, dob_var, user_type_var, tree, win, message_text):
    name = name_var.get().strip()
    dob = dob_var.get().strip()
    user_type = user_type_var.get().strip()
    results = emp_db.search_employees(name, dob, user_type)
    win.after(0, lambda: update_tree(results, tree, message_text))

def update_tree(rows, tree, message_text):
    tree.delete(*tree.get_children())
    if not rows:
        tree.insert("", "end", values=("No results found", "", "", ""))
        ui_util.set_text_readonly(message_text, "No employees found.")
    else:
        for row in rows:
            tree.insert("", "end", values=row)
        ui_util.set_text_readonly(message_text, f"{len(rows)} employee(s) found.")

# ---------- Main Search Window ----------

def open_search_form(parent):
    win = tk.Toplevel(parent)
    win.title("Search Employees")

    # Center and size the window
    w, h = 960, 480
    x, y = ui_util.compute_win_pos(w, h, parent)
    win.geometry(f"{w}x{h}+{x}+{y}")

    # Grid layout setup
    win.columnconfigure(0, weight=1, minsize=200)
    win.columnconfigure(1, weight=2, minsize=400)
    win.rowconfigure(5, weight=1)

    # ---------- Form Variables ----------
    name_var = tk.StringVar()
    dob_var = tk.StringVar()
    user_type_var = tk.StringVar()

    # ---------- Row 0: Top Message ----------
    message_text = tk.Text(win, height=3, wrap="word", bg="gray", fg="white")
    message_text.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    message_text.configure(state="disabled")

    # ---------- Row 1-3: Input Fields ----------
    tk.Label(win, text="Name").grid(row=1, column=0, sticky="e", padx=10, pady=5)
    name_txt = tk.Entry(win, textvariable=name_var)
    name_txt.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

    tk.Label(win, text="Date of Birth (YYYY-MM-DD)").grid(
        row=2, column=0, sticky="e", padx=10, pady=5
    )
    dob_txt = tk.Entry(win, textvariable=dob_var)
    dob_txt.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

    tk.Label(win, text="User Type").grid(row=3, column=0, sticky="e", padx=10, pady=5)
    user_type_txt = tk.Entry(win, textvariable=user_type_var)
    user_type_txt.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

    # ---------- Row 4: Search Button ----------
    tk.Button(
        win,
        text="Search",
        command=lambda: search(
            name_var, dob_var, user_type_var, tree, win, message_text
        ),
    ).grid(row=4, column=0, columnspan=2, pady=10)

    # ---------- Row 5: Search Results ----------
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

    # Double-click to open edit form
    tree.bind("<Double-1>", lambda e: on_treeview_double_click(e, win))

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Bind Enter key to trigger search
    for entry in (name_txt, dob_txt, user_type_txt):
        entry.bind(
            "<Return>",
            lambda e: search(
                name_var, dob_var, user_type_var, tree, win, message_text
            ),
        )

    name_txt.focus_set()
    return win

# ---------- TreeView Row Double-Click ----------

def on_treeview_double_click(event, win):
    tree = event.widget
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    if values[0] == "No results found":
        return

    emp_id, name, dob, user_type = values

    # Close search window before showing edit form
    win.destroy()
    employee_edit_form.open_edit_form(win.master, emp_id, name, dob, user_type)
