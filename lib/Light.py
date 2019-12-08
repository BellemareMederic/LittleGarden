from threading import Thread
from datetime import datetime
import time
import sqlite3
import lib.Util as Util

class Light(Thread):
    def __init__(self, globalConf):
        Thread.__init__(self)
        self.parameter = globalConf
        self.dbCreate()
        self.status = {
            "isOn": False,
            "isForceLight": False
        }

    def run(self):
        """
        Execution du thread
        """

        shutupStart = datetime.time(datetime.strptime(
            self.parameter["shutup"]["start"], "%H:%M:%S"))
        shutupEnd = datetime.time(datetime.strptime(
            self.parameter["shutup"]["end"], "%H:%M:%S"))
        lightOn = datetime.time(datetime.strptime(
            self.parameter["light"]["horaire"]["start"], "%H:%M:%S"))
        lightOff = datetime.time(datetime.strptime(
            self.parameter["light"]["horaire"]["end"], "%H:%M:%S"))
        while True:
            currentTime = datetime.time(datetime.now())
            if(not Util.timeBetweem(shutupStart, shutupEnd, currentTime)):
                if(Util.timeBetweem(lightOn, lightOff, currentTime) or self.status["isForceLight"] is True):
                    self.lightOn()
                else:
                    self.lightOff()
                self.dbInsert()
            time.sleep(self.parameter["light"]["loop_delay"])

    def lightOn(self):
        if(self.status['isOn'] is False):
            print("Turning On")
            self.status['isOn'] = True

    def lightOff(self):
        if(self.status["isOn"] is True):
            print("Turning Off")
            self.status["isOn"] = False

    def toggleLight(self):
        if(self.status["isOn"] is True):
            self.lightOff()
        else:
            self.lightOn()

    def dbCreate(self):
        """
        crée la table dans la database si elle n'existe pas.
        """

        connection = sqlite3.connect(self.parameter["database"]["host"])
        cursor = connection.cursor()
        try:
            cursor.execute(f"""CREATE TABLE light(
                timestamp TEXT DEFAULT (datetime('now','localtime')),
                light INTEGER,
                ForceLight INTEGER
            )""")
        except sqlite3.Error as e:
            print(e)

        connection.commit()
        connection.close()

    def dbInsert(self):
        """
        On insert l'objet status dans la base de donnée
        """

        connection = sqlite3.connect(self.parameter["database"]["host"])
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO light(light, ForceLight) VALUES (?,?)", (str(int(self.status["isOn"])), self.status["isForceLight"]))
        except sqlite3.Error as e:
            print(f"Light insert error: {e}")

        connection.commit()
        connection.close()

    def dbBetween(self, args):
        connection = sqlite3.connect(self.parameter["database"]["host"])
        cursor = connection.cursor()
        if(args.get('startdate') is not None and args.get('enddate') is not None):
            query = f"SELECT * FROM light WHERE timestamp BETWEEN '{startdate}' AND '{enddate}'"
        elif(args.get('startdate') is not None):
            startdate = datetime(args.get('startdate'))
            # enddate = startdate.set
            query = f"SELECT * FROM light WHERE timestamp BETWEEN '{startdate}' AND '{enddate}'"
        else:
            query = f"SELECT * FROM light WHERE timestamp"
        try:
            cursor.execute(query)
            data = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Cannot get information {e}")
        connection.close()
        return data
