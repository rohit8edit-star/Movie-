import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="bot.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                join_date TIMESTAMP
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                year INTEGER,
                language TEXT,
                quality TEXT,
                file_id TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                movie_name TEXT,
                request_date TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_user(self, user_id):
        try:
            self.cursor.execute('INSERT INTO users (user_id, join_date) VALUES (?, ?)', (user_id, datetime.now()))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_total_users(self):
        self.cursor.execute('SELECT COUNT(*) FROM users')
        return self.cursor.fetchone()[0]

    def get_all_users(self):
        self.cursor.execute('SELECT user_id FROM users')
        return [row[0] for row in self.cursor.fetchall()]

    def add_movie(self, name, year, language, quality, file_id):
        self.cursor.execute('''
            INSERT INTO movies (name, year, language, quality, file_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name.lower(), year, language, quality, file_id))
        self.conn.commit()

    def delete_movie(self, movie_id):
        self.cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
        self.conn.commit()

    def search_movie(self, query):
        self.cursor.execute('''
            SELECT id, name, year, language, quality, file_id 
            FROM movies 
            WHERE name LIKE ?
            LIMIT 50
        ''', (f'%{query.lower()}%',))
        return self.cursor.fetchall()

    def get_movie_by_id(self, movie_id):
        self.cursor.execute('''
            SELECT id, name, year, language, quality, file_id 
            FROM movies 
            WHERE id = ?
        ''', (movie_id,))
        return self.cursor.fetchone()

    def add_request(self, user_id, movie_name):
        self.cursor.execute('''
            INSERT INTO requests (user_id, movie_name, request_date)
            VALUES (?, ?, ?)
        ''', (user_id, movie_name, datetime.now()))
        self.conn.commit()

db = Database()
