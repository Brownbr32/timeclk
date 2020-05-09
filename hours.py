import datetime

def remaining(conn, whichTable):
    c = conn.cursor()
    totstr = "select hours from daily_hours where table_name='{0}'"
    remaining = (c.execute(totstr.format(whichTable))).fetchall()[0][0]
    hourstr = "SELECT time FROM {0} where date='{1}'"
    date = datetime.datetime.today().strftime("%m/%d/%y")
    hours = (c.execute(hourstr.format(whichTable,date))).fetchall()
    for t in hours:
        if (t[0] > 0):
            remaining -= t[0]
    return remaining

def arePending(c,whichTable):
    penstr = "select exists(select * from pending where table_name='{0}');"
    return (c.execute(penstr.format(whichTable))).fetchall()[0][0]

def exists(c,whichTable):
    exstr = "select exists(select * from time_table where table_name='{0}')"
    return c.execute(exstr.format(whichTable)).fetchall()[0][0]