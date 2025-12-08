def display_dataframe(df):
    """Display dataframe in a readable format"""
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