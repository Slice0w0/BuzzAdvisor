import sqlite3
import json
import os

# Define the path to the JSON file
json_file_path = os.path.join('data', 'oms-central', 'oms-central-processed.json')

# Define the path to the SQLite database
db_path = os.path.join('data', 'gatech_courses.db')

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the 'courses' table if it doesn't exist, with 'codes' as the primary key
cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        codes TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        syllabus_url TEXT,
        is_foundational BOOLEAN,
        slug TEXT,
        review_count INTEGER,
        rating REAL,
        difficulty REAL,
        workload REAL
    )
''')

# Load JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Insert JSON data into the 'courses' table
for course in data:
    # Join multiple codes with a dash to form a single primary key
    codes_str = '-'.join(course.get('codes', []))
    syllabus_url = course.get('syllabus', {}).get('url', None)
    
    cursor.execute('''
        INSERT OR IGNORE INTO courses (codes, name, description, syllabus_url, is_foundational, slug, review_count, rating, difficulty, workload)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        codes_str,
        course.get('name'),
        course.get('description'),
        syllabus_url,
        course.get('isFoundational'),
        course.get('slug'),
        course.get('reviewCount', 0),
        course.get('rating', 0.0),
        course.get('difficulty', 0.0),
        course.get('workload', 0.0)
    ))

# Commit the changes and close the connection
conn.commit()
conn.close()
