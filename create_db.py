import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
c.execute('CREATE TABLE trains (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, source TEXT, destination TEXT)')
c.execute('CREATE TABLE bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, train_id INTEGER)')

conn.commit()
conn.close()
print("Database and tables created.")
