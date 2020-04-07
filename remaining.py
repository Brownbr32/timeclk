#!/usr/bin/python3
import datetime
import sys
import sqlite3
import pa

t = datetime.datetime.today().strftime("%m/%d/%y")
print(t)

def printRemaining(conn, whichTable):
    c = conn.cursor()
    totstr = "select hours from daily_hours where table_name='{0}'"
    remaining = (c.execute(totstr.format(whichTable))).fetchall()[0][0]
    hourstr = "SELECT time FROM {0} where date='{1}'"
    date = datetime.datetime.today().strftime("%m/%d/%y")
    hours = (c.execute(hourstr.format(whichTable,date))).fetchall()
    for t in hours:
        if (t[0] > 0):
            remaining -= t[0]
    print("Hours remaining in {0}:\t{1}".format(whichTable,remaining))



allTables = ['personal','hw', 'exercise', 'house']
conn = sqlite3.connect(pa.th)
for whichTable in allTables:
    printRemaining(conn,whichTable)

