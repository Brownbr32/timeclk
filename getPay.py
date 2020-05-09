#!/usr/bin/python3 -B
import sys
import sqlite3
import pa



def getWage(conn,whichTable):
    c = conn.cursor()
    wagestr = "select wage from hourly where table_name='{0}'"
    hrly = (c.execute(wagestr.format(whichTable))).fetchall()[0][0]
    hourstr = "SELECT time FROM {0}"
    hours = (c.execute(hourstr.format(whichTable))).fetchall()
    wage = 0
    #print(whichTable)
    #print(hrly)
    #print(hours)
    for t in hours:
        if (t[0] > 0):
            wage += t[0] * hrly
    #print(wage)
    return wage



allTables = ['personal','hw', 'sleep', 'wake', 'exercise', 'house']
wage = 0
for whichTable in allTables:
    conn = sqlite3.connect(pa.th)
    wage += getWage(conn,whichTable)
print("For your good behavior, you get a bonus of: \n${0:3.2f}".format(wage))
print("That gives you a spending allowance of: \n${0:3.2f}".format(wage/4))
