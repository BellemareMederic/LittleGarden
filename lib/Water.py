from threading import Thread
import time
import config
from lib.DBConnection import *
import json
from datetime import datetime
import lib.Util as Util

# Humidity sensor
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1115 as ADS
import board
import busio


class Water(Thread):
    def __init__(self, globalConf):
        Thread.__init__(self)
        self.parameter = globalConf
        self.dbCreate()
        self.status = {
            "isForceWatering": False,
            "isWatering": False,
        }
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(i2c)

    def run(self):
        """
        Execution du thread
        """

        start = datetime.time(datetime.strptime(
            self.parameter["shutup"]["start"], "%H:%M:%S"))
        end = datetime.time(datetime.strptime(
            self.parameter["shutup"]["end"], "%H:%M:%S"))
        while True:
            currentTime = datetime.time(datetime.now())
            self.checkHumidity()
            if(not Util.timeBetweem(start, end, currentTime)):
                if(self.status["currentHumidity"] < self.parameter["water"]["targeted_moister"] or self.status["isForceWatering"]):
                    while (self.status["currentHumidity"] < self.parameter["water"]["targeted_moister"] or self.status["isForceWatering"]):
                        self.doWatering()
                        self.status["isForceWatering"] = False
                        time.sleep(self.parameter["water"]["after"])
                        self.checkHumidity()
                else:
                    self.dbInsert()
            time.sleep(self.parameter["water"]["loop_delay"])

    def checkHumidity(self):
        """
        Lire les données d'un ou plusieur capteur humidité
        """
        channel = AnalogIn(ads, ADS.P0)
        print(channel.value, channel.voltage)

    def doWatering(self):
        """
        Active la pompe pour X nombre de seconds
        """

        # open water pompe
        self.status["isWatering"] = True
        self.dbInsert()
        time.sleep(self.parameter["water"]["open"])
        self.status["isWatering"] = False
        # close water pompe

    def dbCreate(self):
        """
        crée la table dans la database si elle n'existe pas.
        """

        connection = createDBConnection()
        cursor = connection.cursor()
        try:
            cursor.execute(f"""CREATE TABLE water(
                timestamp TEXT DEFAULT (datetime('now','localtime')),
                humidity FLOAT,
                water FLOAT,
                watering INT,
                forceWatering INT)""")
        except sqlite3.Error as e:
            print(e)

        connection.commit()
        connection.close()

    def dbInsert(self):
        """
        On insert l'objet status dans la base de donnée
        """

        connection = createDBConnection()
        cursor = connection.cursor()
        data = self.status
        try:
            cursor.execute(f"INSERT INTO water (humidity, water, watering, forceWatering) VALUES (?,?,?,?)",
                           (data["currentHumidity"], 20, data["isWatering"], data["isForceWatering"]))
        except sqlite3.Error as e:
            print(f"Water insert error: {e}")
        connection.commit()
        connection.close()
        # pourcentage d'humidité
        # nombre de ml d'everser (time(s)*débie)
        # date et heurs

    def dbGetAvgWeek(self, startdate, enddate):
        connection = createDBConnection()
        cursor = connection.cursor()
        try:
            cursor.execute(f"""           
            SELECT AVG(humidity), AVG(water) 
            FROM water WHERE timestamp 
            BETWEEN '{startdate}' AND '{enddate}'""")
        except sqlite3.Error as e:
            pass
        return cursor.fetchone()

    # def dbBetweenDate(self, args):
    #     connection = createDBConnection()
    #     cursor = connection.cursor()
    #     if(args.get('startdate') is not None and args.get('enddate') is not None):
    #         query = f"SELECT * FROM water WHERE timestamp BETWEEN '{startdate}' AND '{enddate}'"
    #     elif(args.get('startdate') is not None):
    #         startdate = datetime(args.get('startdate'))
    #         # enddate = startdate.set
    #         query = f"SELECT * FROM water WHERE timestamp BETWEEN '{startdate}' AND '{enddate}'"
    #     try:
    #         cursor.execute(query)
    #         data = cursor.fetchall()
    #     except sqlite3.Error as e:
    #         print(f"Cannot get information {e}")
    #     connection.close()
    #     return data

# SELECT timestamp, humidity, water, watering, forceWater FROM `water` WHERE strftime('%Y-%m-%d %H:%M:%S', timestamp) BETWEEN '2019-08-18 14:13:47' AND '2019-08-18 14:14:27';
