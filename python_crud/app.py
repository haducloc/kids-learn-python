# main.py

import tkinter as tk
from tkinter import ttk, messagebox
import ui_util
import employee_search_form
import employee_edit_form

# ---------- Top-Level Form Handlers ----------

def open_search():
    employee_search_form.open_search_form(root)  # Launch search window

def open_add():
    employee_edit_form.open_edit_form(root)  # Launch add employee form

def open_reports():
    messagebox.showinfo("Reports", "This will open the Reports screen.")  # Placeholder

def create_nav_button(parent, text, command):
    return ttk.Button(parent, text=text, command=command, width=30)

# ---------- Main Application Entry ----------

def main():
    global root
    root = tk.Tk()
    root.title("Employee Management System")

    # Center the window on screen
    w, h = 640, 480
    x, y = ui_util.compute_win_pos(w, h, root)
    root.geometry(f"{w}x{h}+{x}+{y}")

    # --- Header ---
    ttk.Label(root, text="Employee Management System", font=("Arial", 20)).pack(pady=30)

    # --- Navigation Buttons ---
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=20)

    create_nav_button(btn_frame, "🔍 Search Employees", open_search).pack(pady=10)
    create_nav_button(btn_frame, "➕ Add Employee", open_add).pack(pady=10)
    create_nav_button(btn_frame, "📊 Reports", open_reports).pack(pady=10)
    create_nav_button(btn_frame, "❌ Exit", root.quit).pack(pady=10)

    # --- Start the GUI event loop ---
    root.mainloop()

# ---------- Run App ----------
if __name__ == "__main__":
    main()
