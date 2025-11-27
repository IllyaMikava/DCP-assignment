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

def view_by_rhythm():
    """View tunes by rhythm"""
    df = load_dataframe()
    rhythms = get_all_rhythms(df)
    
    print("\nAvailable rhythms:")
    for r in rhythms:
        print(f"  - {r}")
    
    rhythm = input("\nEnter rhythm: ")
    results = get_tunes_by_type(df, rhythm)
    display_dataframe(results)

def show_statistics():
    """Show database statistics"""
    df = load_dataframe()
    
    print("\n" + "="*50)
    print("DATABASE STATISTICS")
    print("="*50)
    print(f"Total tunes: {len(df)}")
    print(f"Total books: {len(get_all_books(df))}")
    
    print("\nTunes per book:")
    counts = count_tunes_per_book(df)
    for book, count in counts.items():
        print(f"  Book {book}: {count} tunes")
    
    print("\nRhythm distribution:")
    rhythm_counts = df['rhythm'].value_counts()
    for rhythm, count in rhythm_counts.items():
        print(f"  {rhythm}: {count} tunes")

def main():
    """Main program loop"""
    create_table()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            load_files()
        elif choice == '2':
            view_all_tunes()
        elif choice == '3':
            search_by_title()
        elif choice == '4':
            view_by_book()
        elif choice == '5':
            view_by_rhythm()
        elif choice == '6':
            show_statistics()
        elif choice == '7':
            clear_database()
            print("Database cleared!")
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice!")
        
        input("\nPress Enter to continue...")

if __name__ == '__main__':
    main()