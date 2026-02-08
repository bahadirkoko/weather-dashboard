import sqlite3
from datetime import datetime
import os

# database file location

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'weather.db')


def init_database():
    """
    Docstring for init_database
    Creates the database and table if they do not exists.
    """
    # ensure the data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # connect to database (creates file if does not exists)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # create table with columns for our weather data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            temperature REAL NOT NULL,
            feels_like REAL NOT NULL,
            humidity INTEGER NOT NULL,
            description TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print('Database initialized successfully!')


def save_weather(weather_data):
    ''' Save weather data to the database'''

    if not weather_data:
        print('No data to save')
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO weather_data 
            (city, temperature, feels_like, humidity, description, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            weather_data['city'],
            weather_data['temperature'],
            weather_data['feels_like'],
            weather_data['humidity'],
            weather_data['description'],
            weather_data['timestamp']
        ))

        conn.commit()
        print(f"✓ Saved weather data for {weather_data['city']}")
        return True

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

    finally:
        conn.close()


def get_weather_history(city, limit=10):
    """
    Retrieves weather history for a city.

    Args:
        city: City name to search for
        limit: Maximum number of records to return

    Why: So we can see trends - "How has temperature changed?"
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT city, temperature, feels_like, humidity, description, timestamp
        FROM weather_data
        WHERE city = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (city, limit))

    rows = cursor.fetchall()
    conn.close()

    # Convert rows to list of dictionaries (easier to work with)
    history = []
    for row in rows:
        history.append({
            'city': row[0],
            'temperature': row[1],
            'feels_like': row[2],
            'humidity': row[3],
            'description': row[4],
            'timestamp': row[5]
        })

    return history


def get_all_cities():
    """
    Gets list of all cities we have data for.

    Why: Useful for showing "what cities can I view history for?"
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT DISTINCT city 
        FROM weather_data 
        ORDER BY city
    ''')

    cities = [row[0] for row in cursor.fetchall()]
    conn.close()

    return cities
