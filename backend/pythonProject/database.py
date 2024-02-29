import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        fname TEXT NOT NULL,
        lname TEXT NOT NULL,
        salt TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        card1 INTEGER NOT NULL,
        card2 INTEGER NOT NULL,
        card3 INTEGER NOT NULL,
        card4 INTEGER NOT NULL,
        card5 INTEGER NOT NULL,
        card6 INTEGER NOT NULL,
        card7 INTEGER NOT NULL
    ) 
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cardReadings (
        id INTEGER PRIMARY KEY,
        image TEXT NOT NULL,
        text1 TEXT NOT NULL,
        text2 TEXT NOT NULL,
        text3 TEXT NOT NULL,
        text4 TEXT NOT NULL,
        text5 TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
