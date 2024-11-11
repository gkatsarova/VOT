from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['POST'])
def add_movie():
    title = request.form['title']
    genre = request.form['genre']
    year = request.form['year']
    director = request.form['director']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO movies (title, genre, year, director, watched) VALUES (?, ?, ?, ?, ?)',
                 (title, genre, year, director, False))
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/toggle_watched/<int:movie_id>', methods=['POST'])
def toggle_watched(movie_id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    
    if movie:
        new_status = not movie['watched']
        conn.execute('UPDATE movies SET watched = ? WHERE id = ?', (new_status, movie_id))
        conn.commit()
    
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 