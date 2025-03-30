import sqlite3

DB_NAME = "campus_app.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurant_hours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            restaurant_name TEXT NOT NULL,
            open_time TEXT NOT NULL,
            close_time TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gym_hours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_of_week TEXT NOT NULL,
            open_time TEXT NOT NULL,
            close_time TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def insert_data(table_name, data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    placeholders = ", ".join(["?"] * len(data[0]))
    query = f"INSERT INTO {table_name} VALUES (NULL, {placeholders})"
    cursor.executemany(query, data)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
