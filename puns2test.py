#!/usr/bin/env python
import sqlite3

connection = sqlite3.connect("database/puns.db")
cursor = connection.cursor()
for i in range(100):
    placeholder = "Placeholder #%s" % (str(i))
    cursor.execute("INSERT INTO openers (content) VALUES (?)", (placeholder,))
    connection.commit()
    cursor.execute("INSERT INTO responses (content) VALUES (?)", (placeholder,))
    connection.commit()

connection.close()
print("DONE")
