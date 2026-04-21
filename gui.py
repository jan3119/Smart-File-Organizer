import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import main   # your backend file


# ---------------- GUI SETUP ---------------- #

root = tk.Tk()
root.title("Smart File Organizer")
root.geometry("450x300")
root.resizable(False, False)


folder_path = tk.StringVar()


# ---------------- STATUS UPDATE FUNCTION ---------------- #

def update_status(text):
    status_label.config(text=text)
    root.update_idletasks()


# ---------------- SELECT FOLDER ---------------- #

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)
        update_status(f"📂 Selected: {folder}")


# ---------------- START ORGANIZING ---------------- #

def start_organizing():

    folder = folder_path.get()

    if not folder:
        messagebox.showerror("Error", "Please select a folder first!")
        return

    update_status("⏳ Organizing files...")

    # run in background thread (IMPORTANT)
    thread = threading.Thread(
        target=main.organize_file,
        args=(folder, update_status)
    )

    thread.start()


# ---------------- UI DESIGN ---------------- #

title = tk.Label(root, text="Smart File Organizer", font=("Arial", 16, "bold"))
title.pack(pady=10)


entry = tk.Entry(root, textvariable=folder_path, width=50)
entry.pack(pady=5)


btn_select = tk.Button(root, text="Select Folder", command=select_folder)
btn_select.pack(pady=5)


btn_start = tk.Button(root, text="Organize Files", command=start_organizing)
btn_start.pack(pady=10)


status_label = tk.Label(root, text="", fg="blue")
status_label.pack(pady=20)


# ---------------- RUN APP ---------------- #

root.mainloop()