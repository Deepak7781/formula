import sqlite3

conn = sqlite3.connect('formula.db')

cursor = conn.cursor()

cursor.execute("SELECT * FROM thermodynamics;")

rows = cursor.fetchall()

for row in rows:
    print(row)



conn.close()