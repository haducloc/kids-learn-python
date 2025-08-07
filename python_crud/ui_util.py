import tkinter as tk

def compute_win_pos(w, h, root):
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x, y = (screen_w - w) // 2, (screen_h - h) // 2
    return x, y

def set_text_readonly(text_widget, text):
    text_widget.configure(state="normal")
    text_widget.delete("1.0", tk.END)
    text_widget.insert("1.0", text)
    text_widget.configure(state="disabled")
