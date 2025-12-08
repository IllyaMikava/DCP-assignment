"""CLI VERSION
A command-line interface for managing and searching an ABC tune database.

This script provides functions to load ABC music files, insert tune data into 
a SQLite database, and perform various search and viewing operations on the 
stored tunes.
"""

from abc_parser import load_all_abc_files
from database import *
import pandas as pd 

def display_menu():
    """
    Display the main menu options for the ABC Tune Database application.
    """
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

def display_dataframe(df: pd.DataFrame):
    """
    Display the contents of a pandas DataFrame containing tune data.

    If the DataFrame is empty, a 'No tunes found!' message is printed. 
    Otherwise, it iterates through the rows and prints detailed information 
    for each tune.

    Args:
        df: A pandas DataFrame where each row represents a tune.
    """
    if df.empty:
        print("\nNo tunes found!")
        return
    
    print(f"\nFound {len(df)} tune(s):\n")
    for idx, row in df.iterrows():          # Loop through each row in the DataFrame
                                            # idx is the index (row number), row is the actual data
                                            # iterrows() returns each row as a Series object
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
    """
    Load all ABC files from the filesystem, clear the existing database, 
    and insert the parsed tune data into the database.
    """
    print("\nLoading ABC files...")
    tunes = load_all_abc_files()
    print(f"Found {len(tunes)} tunes")
    
    print("Clearing database...")
    clear_database() # calls in clear database function which is in database.py file
    
    print("Inserting tunes into database...")
    insert_all_tunes(tunes) #calling in incert all tunes function and passing tunes as a parameters
    print("Done!")

def view_all_tunes():
    """
    Load all tunes from the database and display them using display_dataframe.
    """
    # Call the database function that loads all tunes into a pandas DataFrame
    # Assigns the result to variable df (short for dataframe)
    df = load_dataframe()
    
    display_dataframe(df) # calling in function for printing whole datafarme in structured way

def search_by_title():
    """
    Prompt the user for a search term and display tunes whose titles 
    match the term (case-insensitive substring search).
    """
    search_term = input("\nEnter search term: ")
    df = load_dataframe()

    # Call the database function that filters the DataFrame
    # Returns only tunes whose titles contain the search term
    # Assigns the filtered DataFrame to results
    results = search_tunes(df, search_term)
    #prints out reuslt values in structured way
    display_dataframe(results)

def view_by_book():
    """
    Display a list of available book numbers, prompt the user to select one, 
    and display all tunes belonging to that book number.
    """
    df = load_dataframe()
    books = get_all_books(df)
    
    print(f"\nAvailable books: {list(books)}")
    # Note: Added int() for conversion, assuming input will be a valid book number
    try:
        book_num = int(input("Enter book number: "))
    except ValueError:
        print("\nInvalid input. Book number must be an integer.")
        return
    
    results = get_tunes_by_book(df, book_num)
    display_dataframe(results)

def view_by_rhythm():
    """
    Display a list of available rhythms (tune types), prompt the user to 
    select one, and display all tunes matching that rhythm.
    """
    df = load_dataframe()
    rhythms = get_all_rhythms(df)
    
    print("\nAvailable rhythms:")
    for r in rhythms:
        print(f"  - {r}")
    
    rhythm = input("\nEnter rhythm: ")
    results = get_tunes_by_type(df, rhythm)
    display_dataframe(results)

def show_statistics():
    """
    Calculate and display various statistics about the tunes in the database, 
    including total counts and distribution by book and rhythm.
    """
    df = load_dataframe()
    
    print("\n" + "="*50)
    print("DATABASE STATISTICS")
    print("="*50)
    print(f"Total tunes: {len(df)}")
    print(f"Total books: {len(get_all_books(df))}")
    
    print("\nTunes per book:")
    counts = count_tunes_per_book(df) #function from database.py which groups by tunes and counts them up and gives us dict like (1,5), (2,7)
    for book, count in counts.items(): #book goes over book1 items and book2 items count is a value 
        print(f"  Book {book}: {count} tunes")
    
    print("\nRhythm distribution:")
    # Using df['rhythm'].value_counts() for a clean count of each rhythm
    rhythm_counts = df['rhythm'].value_counts() # Access the 'rhythm' column of the DataFrame and counts it 
    for rhythm, count in rhythm_counts.items():
        print(f"  {rhythm}: {count} tunes")

def main():
    """
    The main function that runs the CLI program. 
    It creates the database table if it doesn't exist and enters the main menu loop.
    """
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