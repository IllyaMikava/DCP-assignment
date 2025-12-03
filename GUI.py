"""
GUI VERSION - ABC Tune Database Interface
This module provides a graphical user interface for managing and querying ABC tune files.
"""

import tkinter as tk
from tkinter import messagebox
from abc_parser import load_all_abc_files
from database import *

# Create main window
window = tk.Tk()
window.title("ABC Tune Database")
window.geometry("800x600")

# Results display
results_text = tk.Text(window, width=70, height=25)
results_text.pack(pady=10)

# Load Files button
def load_files_click():
    """
    Load all ABC files from folders into the database.
    Clears existing database and loads fresh data.
    Shows a message box with the number of tunes loaded.
    """
    tunes = load_all_abc_files()
    clear_database()
    insert_all_tunes(tunes)
    messagebox.showinfo("Done", f"Loaded {len(tunes)} tunes!")

btn_load = tk.Button(window, text="Load ABC Files", command=load_files_click, width=20)
btn_load.pack(pady=5)

# View All button
def view_all_click():
    """
    Display all tunes from the database in the results text area.
    Shows title, key signature, meter, rhythm, and book number for each tune.
    """
    results_text.delete(1.0, tk.END)
    df = load_dataframe()
    
    for idx, row in df.iterrows():
        results_text.insert(tk.END, f"Title: {row['title']}\n")
        results_text.insert(tk.END, f"Key: {row['key_signature']} | Meter: {row['meter']}\n")
        results_text.insert(tk.END, f"Rhythm: {row['rhythm']} | Book: {row['book_number']}\n")
        results_text.insert(tk.END, "-" * 50 + "\n")

btn_view_all = tk.Button(window, text="View All Tunes", command=view_all_click, width=20)
btn_view_all.pack(pady=5)

# Search section
search_frame = tk.Frame(window)
search_frame.pack(pady=5)

tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)

def search_click():
    """
    Search for tunes by title using the search term entered by the user.
    Displays matching tunes or a 'No tunes found' message.
    Search is case-insensitive.
    """
    results_text.delete(1.0, tk.END)
    search_term = search_entry.get()
    df = load_dataframe()
    results = search_tunes(df, search_term)
    
    if results.empty:
        results_text.insert(tk.END, "No tunes found!")
    else:
        for idx, row in results.iterrows():
            results_text.insert(tk.END, f"Title: {row['title']}\n")
            results_text.insert(tk.END, f"Key: {row['key_signature']} | Meter: {row['meter']}\n")
            results_text.insert(tk.END, f"Rhythm: {row['rhythm']} | Book: {row['book_number']}\n")
            results_text.insert(tk.END, "-" * 50 + "\n")

btn_search = tk.Button(search_frame, text="Search", command=search_click, width=10)
btn_search.pack(side=tk.LEFT)

# Book filter section
book_frame = tk.Frame(window)
book_frame.pack(pady=5)

tk.Label(book_frame, text="Book Number:").pack(side=tk.LEFT)
book_entry = tk.Entry(book_frame, width=10)
book_entry.pack(side=tk.LEFT, padx=5)

def filter_book_click():
    """
    Filter and display tunes from a specific book number.
    User must enter a valid book number in the entry field.
    """
    results_text.delete(1.0, tk.END)
    book_num = int(book_entry.get())
    df = load_dataframe()
    results = get_tunes_by_book(df, book_num)
    
    for idx, row in results.iterrows():
        results_text.insert(tk.END, f"Title: {row['title']}\n")
        results_text.insert(tk.END, f"Key: {row['key_signature']} | Meter: {row['meter']}\n")
        results_text.insert(tk.END, f"Rhythm: {row['rhythm']}\n")
        results_text.insert(tk.END, "-" * 50 + "\n")

btn_filter_book = tk.Button(book_frame, text="Filter", command=filter_book_click, width=10)
btn_filter_book.pack(side=tk.LEFT)

# Statistics button (basic stats)
# def stats_click():
#     """
#     Display database statistics including total number of tunes
#     and the count of tunes per book.
#     """
#     results_text.delete(1.0, tk.END)
#     df = load_dataframe()
    
#     results_text.insert(tk.END, f"Total tunes: {len(df)}\n\n")
    
#     counts = count_tunes_per_book(df)
#     results_text.insert(tk.END, "Tunes per book:\n")
#     for book, count in counts.items():
#         results_text.insert(tk.END, f"  Book {book}: {count} tunes\n")

# btn_stats = tk.Button(window, text="Show Statistics", command=stats_click, width=20)
# btn_stats.pack(pady=5)

def stats_click():
    """Display comprehensive database statistics"""
    results_text.delete(1.0, tk.END)
    df = load_dataframe()
    
    # Header
    results_text.insert(tk.END, "=" * 60 + "\n")
    results_text.insert(tk.END, "DATABASE STATISTICS\n")
    results_text.insert(tk.END, "=" * 60 + "\n\n")
    
    # Overall Statistics
    results_text.insert(tk.END, "OVERALL STATISTICS:\n")
    results_text.insert(tk.END, "-" * 60 + "\n")
    results_text.insert(tk.END, f"Total tunes in database: {len(df)}\n")
    results_text.insert(tk.END, f"Total books: {len(df['book_number'].unique())}\n")
    results_text.insert(tk.END, f"Total unique composers: {df['composer'].fillna('Unknown').nunique()}\n")
    results_text.insert(tk.END, f"Total unique rhythms: {df['rhythm'].fillna('Unknown').nunique()}\n\n")
    

# Clear database button
def clear_click():
    """
    Clear all tunes from the database.
    Shows a confirmation message when complete.
    """
    clear_database()
    results_text.delete(1.0, tk.END)
    messagebox.showinfo("Done", "Database cleared!")

btn_clear = tk.Button(window, text="Clear Database", command=clear_click, width=20)
btn_clear.pack(pady=5)

# Create table when starting
create_table()

# Run the window
window.mainloop()