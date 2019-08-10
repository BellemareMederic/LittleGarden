from threading import Thread
from datetime import datetime
import time, random, logging, config, sqlite3

class Water(Thread):
    def __init__(self, waterTime, afterWaterTime, timeInterval=600, targetMoist = 0.20):
        Thread.__init__(self)
        self.waterTime = waterTime
        self.afterWaterTime = afterWaterTime
        self.targetMoist = targetMoist
        self.timeInterval = timeInterval
    
    def run(self):
        connection = sqlite3.connect(config.databaseName)
        self.cursor = connection.cursor()
        while True:
            humidity = self.checkHumidity()
            while (humidity < self.targetMoist):
                #Regarder si on nous somme dans la bonne plage horraire
                self.wateringSeconds()
                time.sleep(self.afterWaterTime)  
                humidity = self.checkHumidity()              
            time.sleep(self.timeInterval)
    
    def checkHumidity(self):
        humidity = random.randint(0,100)/100
        logging.debug(f"Current humidity :{humidity}")
        return humidity
        
    def wateringSeconds(self):
        #open water pompe
        logging.info("Humidity is to low. Starting water pump")
        time.sleep(self.waterTime)
        logging.info("Stopping water pump")
        #close water pompe

    def writeToDatabase(self,data):
        self.cursor.execute(f"INSERT INTO humidity (humidity, watering) VALUES ({data.humidity},{data.watering})")