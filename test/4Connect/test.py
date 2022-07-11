import sqlite3, os

conn = sqlite3.connect('myDatabase')
for line in conn.iterdump():
    print(line)

