#!/usr/bin/env python
# https://pad.riseup.net/p/shittyabstergonerdjokes
import sqlite3

connection = sqlite3.connect("database/puns.db")
cursor = connection.cursor()

with open("puns.txt", "r") as puns:
    for punline in puns:
        splitp = punline.find("[")
        cursor.execute("INSERT INTO puns (content, category) VALUES (?,?)", (punline[:splitp], punline[splitp+1:-2]))
        connection.commit()

connection.close()
print "DONE"