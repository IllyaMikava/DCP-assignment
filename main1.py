from abc_parser import load_all_abc_files
from database import *

def display_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("ABC TUNE DATABASE - MAIN MENU")
    print("="*50)
    print("1. Load ABC files into database")
    print("2. View all tunes")
    print("3. Search tunes by title")
    print("4. View tunes by book number")
    print("5. View tunes by rhythm/type")
    print("6. Show statistics")
    print("7. Clear database")
    print("0. Exit")
    print("="*50)