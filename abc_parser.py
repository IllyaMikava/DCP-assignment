import os

def parse_abc_file(filepath, book_number):
    """
    Parses a single ABC music notation file and extracts tune metadata.

    It reads the file line by line, looking for standard ABC header fields 
    (like X:, T:, M:, K:, R:, C:, etc.) to populate a list of tune dictionaries.

    Args:
        filepath: The full path to the .abc file to be parsed.
        book_number: The book identifier (integer) to be assigned to all 
                     tunes found in this file.

    Returns:
        A list of dictionaries, where each dictionary represents a single 
        tune and contains its metadata (e.g., 'title', 'key', 'rhythm', 
        'reference', 'book_number').
    """


    tunes = [] # list to store all tunes found in this file
    current_tune = {} # dictionary for the tune being processed
    parsing_started = False 
    
    with open(filepath, 'r', encoding='utf-8') as f: # open the .abc file
        lines = f.readlines() # read all lines and stors it in list of strings
    
    for line in lines: # loop through each line
        line = line.strip() # remove whitespace/newline
        
        if line.startswith('X:'):  # new tune starts
            if current_tune: # if old tune was in process then save it to tunes before starting new one
                current_tune['book_number'] = book_number
                tunes.append(current_tune)
            current_tune = {   # start a new tune dictionary
                'reference': line[2:].strip(),
                'titles': [],
                'composer': '',
                'source': '',
                'notes': ''
            }

        # takes out title name and strips it and if current tune still doesnt have setted title then set it with current title
        elif line.startswith('T:'):
            title = line[2:].strip()
            current_tune['titles'].append(title)
            if 'title' not in current_tune: 
                current_tune['title'] = title
            
        elif line.startswith('M:'):
            current_tune['meter'] = line[2:].strip()
            
        elif line.startswith('L:'):
            current_tune['length'] = line[2:].strip()
            
        elif line.startswith('K:'):
            current_tune['key'] = line[2:].strip()
            
        elif line.startswith('R:'):
            current_tune['rhythm'] = line[2:].strip()
            
        elif line.startswith('C:'):
            current_tune['composer'] = line[2:].strip()
            
        elif line.startswith('S:'):
            current_tune['source'] = line[2:].strip()
            
        elif line.startswith('Z:'):
            current_tune['z_id'] = line[2:].strip()
            
        elif line.startswith('Q:'):
            current_tune['tempo'] = line[2:].strip()
            
        elif line.startswith('B:'):
            current_tune['book_ref'] = line[2:].strip()
    
    # after loop save the last tune was processed
    if current_tune:
        current_tune['book_number'] = book_number
        tunes.append(current_tune)
    
    return tunes 

def load_all_abc_files(base_folder='abc_books'):
    """
    Recursively scans a base directory for ABC files and loads all tunes.

    It assumes a directory structure where subfolders represent book numbers, 
    and .abc files within those subfolders contain the tune data.

    Args:
        base_folder: The root directory to start scanning from. Defaults 
                     to 'abc_books'.

    Returns:
        A list of all tune dictionaries parsed from all .abc files 
        found in the directory structure.
    """
    all_tunes = []  # master list to store all tunes
    
    for book_folder in os.listdir(base_folder):    # loop through folders
        book_path = os.path.join(base_folder, book_folder)  # full path of abc files
        
        if os.path.isdir(book_path):    # ensure it is a folder
            book_number = int(book_folder) # folder name is book number
            
            for filename in os.listdir(book_path):   # loop through files inside
                if filename.endswith('.abc'):       # check if file is .abc
                    filepath = os.path.join(book_path, filename)  # full file pat
                    tunes = parse_abc_file(filepath, book_number) # parse file
                    all_tunes.extend(tunes) # add tunes to master list
    
    return all_tunes # return all tunes from all files