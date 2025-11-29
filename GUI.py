"""GUI VERSION"""

import tkinter as tk
from tkinter import messagebox
from abc_parser import load_all_abc_files
from database import *

#  Create main window
window = tk.Tk()
window.title("ABC Tune Database")
window.geometry("800x600")

# Results display
results_text = tk.Text(window, width=70, height=25)
results_text.pack(pady=10)

# Load Files button
def load_files_click():
    tunes = load_all_abc_files()
    clear_database()
    insert_all_tunes(tunes)
    messagebox.showinfo("Done", f"Loaded {len(tunes)} tunes!")

btn_load = tk.Button(window, text="Load ABC Files", command=load_files_click, width=20)
btn_load.pack(pady=5)
