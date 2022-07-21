# MeteoLog: an Autonomous NON connected Meteorologic Station using Arduino

* [Introduction](##introduction)
* [Station](##station)
* [Arduino scripts](##arduino-scripts)
* [Python and SQL](##python-and-sql)




## Introduction

The project aims at developping a lowcost meteorologic station with the following properties
* The station's main purpose is to measure rainfall but temperature and humidity are also included,
* it has to be solar powered,
* it has to store the data on an SD card

Included are the references needed to build the station, the electronic and the codes needed to have it run.


## The station

![](./data/IMG_1832.jpg)

### Structure & parts

* Watchdog auger pluviometer that sends a small voltage when the auger tilts. The one I bought is uselessly expensive (400€) because  it includes an electronic logger that I do not wish to use here because (1) its time resolution is too limited, (2) it is not solar powered, (3) it has to be used with some silly expensive (100€) windows program to retrieve the data.
You can get the equivalent without the logger for ~ 100€ (sic, look at Rainwise for exemple)
* Temperature and humidity sensor DHT11 (3.5€). A DHT22 (10.2€) would be better as it is more precise (0.5° and 2% compared to 2° and 5% for the DHT11).
* 3W Solar panel (19€)
* 3.7V, 800mA LiPo battery (7.1€)
* DFRobot Sunflower 5 to handle the solar panel and the battery(8.65€),
* Housing for DHT11 by TFA Dostman (18€)
* Box for the electronic
* Rod and Norcan to hold everything

### Electronic

![](./data/IMG_1826.jpg)


* Arduino Nano
* RTC module to keep track of time
* The auger pluviometer is connected to the digital port 2 that enables interruptions to be raised.
* SDcard module to store the data
* Solar charger connected to LiPo battery and to the Nano.

![](./sketch/MeteoLog_bb.jpg)
Note that the breadboard view  does not include USB connection to the sunflower solar module.



## Arduino scripts

### NanoWeatherLoggerSleepOne

This scripts puts the arduino in deepsleep for a minute. During the sleep period if the auger tilts an interrupt is launched and a rainfall counter increments. At the end of th period the DHT11 measures temperature and humidity and the Arduino stores Temperature, humidity and amount of rain fallen during the last minute.

A sample of a METEOLOG.TXT data file stored on the SD card is given in data.

## Python and SQL

I use a Mariadb database to store the data once retrieved from the SDcard. I call the base weatherDB.


The format of the data table corresponding to the NanoWeatherLoggerSleepOne script is given below.

* md, date, date of measurement
* mt, time, time of measurement
* T, float, temperature
* H, float, Humidity
* P, float, precipitation
* stcode, int, station code

The stations table records the Station informations so it becomes possible to store the data from as many stations as we wish (once they're built !)

Its structure is the following

* stcode, int, station code
* name, varchar(255), station name,
* longitude, float
* latitude, float
* elevation, float
* comment, text, any useful information.

A sample of the database is given in data. To install the database you need to have a running version of MariaDB or Mysql server.

One way recreate the database is to open a terminal in the data folder and enter the following command
```mysql
mysql -u<your login> -p<your pass> < weatherDB.sql
```

 Once installed
enter your  your SQL identifiers  in the mylogin.txt file.
You can then run the demo scripts from Meteo.py
