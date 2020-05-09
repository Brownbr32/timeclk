#!/usr/bin/python3
import sys
import sqlite3

allNames = [
            'hw',
            'personal',
            'sleep',
            'wake',
            'exercise',
            'house'
           ]
allNames = [
            'test',
            'test1',
           ]

conn = sqlite3.connect("clk.db")
c = conn.cursor()
addCol = "ALTER TABLE {0} ADD {1} {2}"

for whichTable in allNames:
    print("executing:")
    print(addCol.format(whichTable,sys.argv[1],sys.argv[2]))
    print(" ")
    c.execute(addCol.format(whichTable,sys.argv[1],sys.argv[2]))
c.commit()

