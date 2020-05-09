#!/usr/bin/python3
import datetime
import sqlite3
import sys
import pa
import hours

def get_rowid(c,whichTable):
    getstring = "SELECT rid FROM pending WHERE table_name='{}'"
    return (c.execute(getstring.format(whichTable)).fetchall())[0][0]

def get_my_id(c,whichTable, date, hrIn, minIn):
    getstring = "SELECT rowid FROM {0} WHERE date='{1}' and hr_in={2} and min_in={3}"
    return (c.execute(getstring.format(whichTable,date,hrIn,minIn)).fetchall())[0]

def clock_in(conn, whichTable, date, hrIn, minIn):
    insstring = "insert into {0} values ( '{1}',{2},{3},{4},{5},{6} );"
    c = conn.cursor()
    if whichTable == "sleep":
        hrOut = 6
        minOut = 0
        dt = (hrOut-hrIn)%24 + float(minOut-minIn)/60
    elif whichTable == "wake":
        hrOut = 8
        minOut = 30
        dt = (hrOut-hrIn)%24 + float(minOut-minIn)/60
    else:
        hrOut = minOut = dt = -1
    c.execute(insstring.format(whichTable,date,hrIn,minIn,hrOut,minOut,dt))
    if(hours.arePending(conn.cursor(),whichTable)):
        print("You're already clocked in.")
        dt= -2
    else:
        if (whichTable != 'sleep') and (whichTable != 'wake'):
            rowid = get_my_id(c,whichTable,date,hrIn,minIn)
            pend = "insert into pending values ( '{0}',{1} );"
            c.execute(pend.format(whichTable,rowid[0]))
    conn.commit()
    return dt

def clock_out(conn,whichTable,date,hrOut,minOut):
    if hours.arePending(conn.cursor(),whichTable):
        rowid = get_rowid(conn.cursor(),whichTable)
        getTimeStr = "SELECT hr_in, min_in FROM {0} WHERE rowid={1}"
        c = conn.cursor()
        tin = (c.execute(getTimeStr.format(whichTable,rowid))).fetchall()[0]
        dt = (hrOut-tin[0])%24+float(minOut-tin[1])/60
        ckout = "UPDATE {0} SET hr_out = {1}, min_out = {2}, time = {3} WHERE rowid={4}"
        if (whichTable != 'sleep') and (whichTable != 'wake'):
            rem = hours.remaining(conn,whichTable)
        else:
            rem = 24
        dt = min(rem,dt)
        c.execute(ckout.format(whichTable,hrOut,minOut,dt,rowid))
        delstring = "DELETE FROM pending WHERE table_name='{}'"
        c.execute(delstring.format(whichTable))
    else:
        print("Not clocked in yet, sorry.")
        dt = -2
    conn.commit()
    return dt

def chooseFun(operation,whichTable):
    conn = sqlite3.connect(pa.th)
    t = datetime.datetime.now()
    funCall = {
        "in": clock_in,
        "out": clock_out
        }
    mody = "%m/%d/%y"
    date = t.strftime(mody)
    h = t.strftime('%H')
    m = t.strftime("%M")
    f = funCall.get(sys.argv[1])
    if(hours.exists(conn.cursor(),whichTable)):
        dt = f(conn, whichTable, date, int(h), int(m))
    else:
        print ("time card does not exist!")
        dt = -3
    conn.close()
    return dt


if(len(sys.argv) == 3):

    dt = chooseFun(sys.argv[1],sys.argv[2])
    if dt >= 0:
        print("Clocked {} successfully!".format(sys.argv[1]))
        print("Clocked {0} for {1} hrs.".format(sys.argv[1],dt))
else:
    print("Error: Too few arguments")
