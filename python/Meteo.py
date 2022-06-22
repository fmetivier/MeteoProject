import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from sqlalchemy import create_engine


def temp_record(station_code=1):
    """
    temperature record of the station
    the record is stored in a mysql database
    """
    f = open("mylogin.txt", "r")
    mylogin = f.readline().strip("\n")
    mypass = f.readline().strip("\n")
    f.close()
    print(mylogin, mypass)
    engine = create_engine("mysql://%s:%s@localhost/weatherDB" % (mylogin, mypass))
    conn = engine.connect()

    sql = "select str_to_date(concat(md,' ',mt),'%Y-%m-%d %T') as dt, avg(T) as Tm from data  "
    sql += "where stcode = %s group by md, hour(mt)" % (station_code)
    df = pd.read_sql(sql, conn)

    fig, ax = plt.subplots(1)
    ax.plot(df["dt"], df["Tm"].tolist(), "-", color="C1")
    myFmt = md.DateFormatter("%d:%h")
    ax.xaxis.set_major_formatter(myFmt)
    ax.set_ylabel("Temperature ($^o$C)")
    ax.set_xlabel("Date")


def temperature_hour_avg(station_code=1):
    """
    hourly temperature plot from the database record
    """
    f = open("mylogin.txt", "r")
    mylogin = f.readline().strip("\n")
    mypass = f.readline().strip("\n")
    f.close()
    print(mylogin, mypass)
    engine = create_engine("mysql://%s:%s@localhost/weatherDB" % (mylogin, mypass))
    conn = engine.connect()

    sql = (
        "select hour(mt) as hour, avg(T) as Tm from data  where stcode = %s group by hour(mt)"
        % (station_code)
    )

    df = pd.read_sql(sql, conn)

    plt.figure()

    plt.plot(df["hour"], df["Tm"].tolist(), color="C1")


def precip_1(station_code=1):
    """
    Calculation fo the rainfall intensity
    """
    f = open("mylogin.txt", "r")
    mylogin = f.readline().strip("\n")
    mypass = f.readline().strip("\n")
    f.close()
    engine = create_engine("mysql://%s:%s@localhost/weatherDB" % (mylogin, mypass))
    conn = engine.connect()

    sql = "select str_to_date(concat(md,' ',mt),'%Y-%m-%d %T') as t,P  from data "
    sql += "where stcode = %s" % (station_code)

    df = pd.read_sql(sql, conn)
    temps = df["t"].tolist()
    precip = df["P"].tolist()

    starttime = []
    raintime = []
    rain = []
    start = True

    for i in np.arange(1, len(precip) - 2):
        if precip[i - 1] == 1 or start == True:
            starttime.append(temps[i])

        if precip[i] == 0:
            start = False
        else:
            raintime.append(temps[i + 1])
            rain.append(precip[i])
            start = True

    if len(starttime) > len(raintime):
        starttime.pop()
    print(len(rain), len(raintime), len(starttime))
    # get I
    I = []
    pI = []
    pT = []

    for i in range(len(rain)):

        dt = raintime[i].timestamp() - starttime[i].timestamp()
        I.append(rain[i] / dt)

    for i in np.arange(1, len(rain) - 1):
        pT.append(starttime[i])
        pT.append(starttime[i])
        pT.append(raintime[i])
        pI.append(I[i - 1])
        pI.append(I[i])
        pI.append(I[i])

    fig, ax = plt.subplots(1)
    ax.plot(pT, pI)
    myFmt = md.DateFormatter("%d:%h")
    ax.xaxis.set_major_formatter(myFmt)
    ax.set_ylabel("Rainfall rate (mm/s)")
    ax.set_xlabel("Date")


if __name__ == "__main__":
    temp_record()
    temperature_hour_avg()
    precip_1()

    plt.show()
