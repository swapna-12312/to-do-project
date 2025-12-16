import sqlite3

conn = sqlite3.connect('todo.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0
)
''')
conn.commit()
conn.close()

print("Database initialized!")
