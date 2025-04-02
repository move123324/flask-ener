# insert_flights.py
import sqlite3

conn = sqlite3.connect("instance/db.sqlite")

# Insert 50 flights on consecutive days in March 2025
for i in range(50):
    day = 1 + (i % 31)  # day will cycle through 1..31
    date_str = f"2025-03-{day:02d}"
    conn.execute(
        "INSERT INTO flight (iata_departure, iata_aircraft, flight_date) VALUES (?, ?, ?)",
        ("JFK", "A320", date_str)
    )

conn.commit()
conn.close()

print("Inserted 50 flights into 'flight' table.")
