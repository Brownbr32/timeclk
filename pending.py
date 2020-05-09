#!/usr/bin/python3 -B
import sqlite3
import pa

def pending(conn):
    c = conn.cursor()
    table = c.execute("select * from pending;")
    for row in table:
        print(row[0])

pending(sqlite3.connect(pa.th))
