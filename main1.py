"""CLI VERSION"""

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

def display_dataframe(df):
    """Display dataframe"""
    if df.empty:
        print("\nNo tunes found!")
        return
    
    print(f"\nFound {len(df)} tune(s):\n")
    for idx, row in df.iterrows():
        print(f"ID: {row['id']}")
        print(f"  Title: {row['title']}")
        print(f"  Reference: {row['reference']}")
        print(f"  Key: {row['key_signature']}")
        print(f"  Meter: {row['meter']}")
        print(f"  Rhythm: {row['rhythm']}")
        if row['composer']:
            print(f"  Composer: {row['composer']}")
        if row['source']:
            print(f"  Source: {row['source']}")
        print(f"  Book: {row['book_number']}")
        print("-" * 40)

def load_files():
    """Load all ABC files and insert into database"""
    print("\nLoading ABC files...")
    tunes = load_all_abc_files()
    print(f"Found {len(tunes)} tunes")
    
    print("Clearing database...")
    clear_database()
    
    print("Inserting tunes into database...")
    insert_all_tunes(tunes)
    print("Done!")

def view_all_tunes():
    """View all tunes in database"""
    df = load_dataframe()
    display_dataframe(df)

def search_by_title():
    """Search tunes by title"""
    search_term = input("\nEnter search term: ")
    df = load_dataframe()
    results = search_tunes(df, search_term)
    display_dataframe(results)
