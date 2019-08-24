from threading import Thread
import time, random, config, sqlite3
import json
from datetime import datetime
import Util

class Water(Thread):
    def __init__(self, configurationObj):
        Thread.__init__(self)
        self.parameter = configurationObj
        self.dbCreate()
        self.status = {
            "isForceWatering": False,
            "isWatering": False,
        }
    
    def run(self):
        start = datetime.time(datetime.strptime(self.parameter["shutup"]["start"],"%H:%M:%S")) 
        end = datetime.time(datetime.strptime(self.parameter["shutup"]["end"],"%H:%M:%S"))
        while True:
            currentTime = datetime.time(datetime.now())
            self.checkHumidity()
            if(not Util.timeBetweem(start,end,currentTime)):
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
        self.status["currentHumidity"] = random.randint(0,100)/100
        
    def doWatering(self):
        #open water pompe
        self.status["isWatering"] = True
        self.dbInsert()
        time.sleep(self.parameter["water"]["open"])
        self.status["isWatering"] = False
        #close water pompe

    def dbCreate(self):
        connection = sqlite3.connect(self.parameter["database"]["host"])
        cursor = connection.cursor()
        try:
            cursor.execute(f"""CREATE TABLE water(
                timestamp TEXT DEFAULT (datetime('now','localtime')),
                humidity FLOAT,
                water FLOAT,
                watering INT,
                forceWatering INT

            )""")
        except sqlite3.Error as e:
            print(e)

        connection.commit()
        connection.close()

    def dbInsert(self):
        connection = sqlite3.connect(self.parameter["database"]["host"])
        cursor = connection.cursor()
        data = self.status
        try:
            cursor.execute(f"INSERT INTO water (humidity, water, watering, forceWatering) VALUES (?,?,?,?)",(data["currentHumidity"],20,data["isWatering"],data["isForceWatering"]))
        except sqlite3.Error as e:
            print(f"Water insert error: {e}")
        connection.commit()
        connection.close()
        #pourcentage d'humidité
        #nombre de ml d'everser (time(s)*débie)
        #date et heurs
    
# SELECT timestamp, humidity, water, watering, forceWater FROM `water` WHERE strftime('%Y-%m-%d %H:%M:%S', timestamp) BETWEEN '2019-08-18 14:13:47' AND '2019-08-18 14:14:27';