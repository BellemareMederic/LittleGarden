from threading import Thread
from datetime import datetime
import time, random, logging, config, sqlite3
import json

class Water(Thread):
    def __init__(self, waterTime, afterWaterTime, loopInterval=600, targetMoist = 0.20):
        Thread.__init__(self)
        self.parameter = {
            "waterTime": waterTime,
            "afterWaterTime": afterWaterTime,
            "loopInterval": loopInterval,
            "targetMoist": targetMoist
        }
        self.status = {
            "isForceWatering": False,
            "isWatering": False
        }
    
    def run(self):
        # connection = sqlite3.connect(config.databaseName)
        # self.cursor = connection.cursor()
        while True:
            self.checkHumidity()
            while (self.status["currentHumidity"] < self.parameter["targetMoist"] or self.status["isForceWatering"]):
                #Regarder si on nous somme dans la bonne plage horraire
                self.doWatering()
                self.isForceWatering = False
                time.sleep(self.parameter["afterWaterTime"])  
                self.checkHumidity()              
            time.sleep(self.parameter["loopInterval"])
    
    def checkHumidity(self):
        self.status["currentHumidity"] = random.randint(0,100)/100
        
    def doWatering(self):
        #open water pompe
        self.status["isWatering"] = True
        time.sleep(self.parameter["waterTime"])
        self.status["isWatering"] = False
        #close water pompe

    def writeToDatabase(self, data):
        pass
        # self.cursor.execute(f"INSERT INTO humidity (humidity, watering) VALUES ({data.humidity},{data.watering})")

    def getParam(self):
        """
        Return object parameter 
        """
        return self.parameter 
        

    def getStatus(self):
        """
        Return status information about the current object
        """
        return self.status
    
    