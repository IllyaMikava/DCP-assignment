import mysql.connector
import pandas as pd

def connect_database():
    """Connect to MySQL database"""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='abc_tunes'
    )
    return conn

def create_table():
    """Create tunes table if it doesn't exist"""
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tunes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            reference VARCHAR(50),
            title VARCHAR(300),
            meter VARCHAR(50),
            length VARCHAR(50),
            key_signature VARCHAR(50),
            rhythm VARCHAR(50),
            composer VARCHAR(300),
            source VARCHAR(300),
            tempo VARCHAR(50),
            z_id VARCHAR(100),
            book_ref VARCHAR(300),
            book_number INT
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

def insert_tune(tune):
    """Insert a single tune into the database"""
    conn = connect_database()
    cursor = conn.cursor()
    
    query = '''
        INSERT INTO tunes (reference, title, meter, length, key_signature, rhythm, 
                          composer, source, tempo, z_id, book_ref, book_number)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    
    values = (
        tune.get('reference', ''),
        tune.get('title', ''),
        tune.get('meter', ''),
        tune.get('length', ''),
        tune.get('key', ''),
        tune.get('rhythm', ''),
        tune.get('composer', ''),
        tune.get('source', ''),
        tune.get('tempo', ''),
        tune.get('z_id', ''),
        tune.get('book_ref', ''),
        tune.get('book_number', 0)
    )
    
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

def insert_all_tunes(tunes):
    """Insert all tunes into database"""
    for tune in tunes:
        insert_tune(tune)

def clear_database():
    """Clear all tunes from database"""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tunes')
    conn.commit()
    cursor.close()
    conn.close()

def load_dataframe():
    """Load all tunes from database into pandas DataFrame"""
    conn = connect_database()
    query = "SELECT * FROM tunes"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_tunes_by_book(df, book_number):
    """Get all tunes from a specific book"""
    return df[df['book_number'] == book_number]

def get_tunes_by_type(df, rhythm):
    """Get all tunes of a specific rhythm/type"""
    return df[df['rhythm'].str.contains(rhythm, case=False, na=False)]

def search_tunes(df, search_term):
    """Search tunes by title"""
    return df[df['title'].str.contains(search_term, case=False, na=False)]

def get_all_books(df):
    """Get list of all book numbers"""
    return sorted(df['book_number'].unique())

def count_tunes_per_book(df):
    """Count tunes in each book"""
    return df.groupby('book_number').size()

def get_all_rhythms(df):
    """Get list of unique rhythms"""
    return df['rhythm'].dropna().unique()