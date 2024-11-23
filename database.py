import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import sqlite3

conn = sqlite3.connect('formula.db')

cursor = conn.cursor()

cursor.execute("SELECT * FROM classicalPhysics;")

rows = cursor.fetchall()

for row in rows:
    for term in row:
        print(term)



conn.close()