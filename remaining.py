#!/usr/bin/python3
import datetime
import sys
import sqlite3
import pa
import hours


allTables = ['personal','hw', 'exercise', 'house']
conn = sqlite3.connect(pa.th)
for whichTable in allTables:
    print("Hours remaining in {0}:  \t{1}".format(whichTable,round(hours.remaining(conn,whichTable),3)))

