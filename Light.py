from threading import Thread
from datetime import datetime
import time
import Util
import sqlite3

class Light(Thread):
    def __init__(self, configurationObj):
        Thread.__init__(self)
        self.parameter = configurationObj
        self.dbCreate()
        self.status = {
            "isOn": False,
            "isForceLight": False
        }
        
    
    def run(self):
        shutupStart = datetime.time(datetime.strptime(self.parameter["shutup"]["start"],"%H:%M:%S")) 
        shutupEnd = datetime.time(datetime.strptime(self.parameter["shutup"]["end"],"%H:%M:%S"))
        lightOn = datetime.time(datetime.strptime(self.parameter["light"]["horaire"]["start"],"%H:%M:%S"))
        lightOff = datetime.time(datetime.strptime(self.parameter["light"]["horaire"]["end"],"%H:%M:%S"))
        while True:
            currentTime = datetime.time(datetime.now())
            if(not Util.timeBetweem(shutupStart,shutupEnd,currentTime)):
                if(Util.timeBetweem(lightOn,lightOff,currentTime) or self.status["isForceLight"] == True) :
                    self.lightOn()
                else:
                    self.lightOff()
                self.dbInsert()
            time.sleep(self.parameter["light"]["loop_delay"])
                

    def lightOn(self):
        if(self.status['isOn'] == False):
            print("Turning On")
            self.status['isOn'] = True

    def lightOff(self):
        if(self.status["isOn"] == True):
            print("Turning Off")
            self.status["isOn"] = False

    def toggleLight(self):
        if(self.status["isOn"] == True):
            self.lightOff()
        else:
            self.lightOn()

    def forceLight(self):
        if(self.status["isForceLight"] == False):
            self.status["isForceLight"] = True
        else:
            self.status["isForceLight"] = False

    def dbCreate(self):
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
        connection = sqlite3.connect(self.parameter["database"]["host"])
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO light(light, ForceLight) VALUES (?,?)",(str(int(self.status["isOn"])), self.status["isForceLight"]))
        except sqlite3.Error as e:
            print(f"Light insert error: {e}")

        connection.commit()
        connection.close()