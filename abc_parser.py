import os

def parse_abc_file(filepath, book_number):
    """Parse an ABC file and return list of tune dictionaries"""
    tunes = []
    current_tune = {}
    parsing_started = False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('X:'):
            if current_tune:
                current_tune['book_number'] = book_number
                tunes.append(current_tune)
            current_tune = {
                'reference': line[2:].strip(),
                'titles': [],
                'composer': '',
                'source': '',
                'notes': ''
            }
            
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
    
    if current_tune:
        current_tune['book_number'] = book_number
        tunes.append(current_tune)
    
    return tunes

def load_all_abc_files(base_folder='abc_books'):
    """Load all ABC files from all book folders"""
    all_tunes = []
    
    for book_folder in os.listdir(base_folder):
        book_path = os.path.join(base_folder, book_folder)
        
        if os.path.isdir(book_path):
            book_number = int(book_folder)
            
            for filename in os.listdir(book_path):
                if filename.endswith('.abc'):
                    filepath = os.path.join(book_path, filename)
                    tunes = parse_abc_file(filepath, book_number)
                    all_tunes.extend(tunes)
    
    return all_tunes