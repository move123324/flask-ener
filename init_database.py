import sqlite3
import os

os.makedirs('instance', exist_ok=True)

db_path = 'instance/db.sqlite'
conn = sqlite3.connect(db_path)

conn.executescript('''
CREATE TABLE IF NOT EXISTS airport (
    iata_code TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS aircraft (
    iata_aircraft TEXT PRIMARY KEY,
    aircraft_type TEXT
);

CREATE TABLE IF NOT EXISTS flight (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    iata_departure TEXT NOT NULL,
    iata_aircraft TEXT NOT NULL,
    flight_date TEXT NOT NULL
);
''')

conn.execute("INSERT OR IGNORE INTO airport (iata_code, name) VALUES ('JFK', 'John F Kennedy International Airport')")
conn.execute("INSERT OR IGNORE INTO aircraft (iata_aircraft, aircraft_type) VALUES ('A320', 'Airbus A320')")
conn.execute("INSERT OR IGNORE INTO flight (iata_departure, iata_aircraft, flight_date) VALUES ('JFK', 'A320', '2025-03-23')")

conn.commit()
conn.close()

print(f"Database initialized at {db_path}")
