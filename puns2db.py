#!/usr/bin/env python
# https://pad.riseup.net/p/shittyabstergonerdjokes
import sqlite3

connection = sqlite3.connect("database/puns.db")
cursor = connection.cursor()

with open("puns.txt", "r") as puns:
    cont = puns.read()
    cont = cont.split("==========================================")
    
    for line in cont[0].split("\n"):
        if len(line) < 2:
            continue
        cursor.execute("INSERT INTO openers (content) VALUES (?)", (line,))
        connection.commit()
        pass
    
    for line in cont[1].split("\n"):
        if len(line) < 2:
            continue
        cursor.execute("INSERT INTO responses (content) VALUES (?)", (line,))
        connection.commit()
        pass

connection.close()
print "DONE"