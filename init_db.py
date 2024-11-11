import sqlite3

conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE movies_new (
        id INTEGER PRIMARY KEY,
        title TEXT,
        year INTEGER,
        director TEXT,
        genre TEXT,
        watched BOOLEAN DEFAULT 0
    )
""")

cursor.execute("""
    INSERT INTO movies_new (id, title, year, director, genre, watched)
    SELECT id, title, year, director, genre, watched FROM movies
""")

cursor.execute("DROP TABLE movies")

cursor.execute("ALTER TABLE movies_new RENAME TO movies")

conn.commit()
conn.close()

print("Table is updated")
