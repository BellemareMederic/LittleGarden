from threading import Thread
import time
import sqlite3

class Temperature(Thread):
    def __init__(self, globalConf):
        Thread.__init__(self)
        self.parameter = globalConf
        self.dbCreate()
        self.status = {}

    def run(self):
        while(True):
            self.getTemperature()
            time.sleep(self.parameter["temperature"]["loop_delay"])

    def getTemperature(self):
        """
        Lire les donnée de temperature
        """
        #TODO: il faut lire les vrai donnée ici
        self.status["temperature"] = 0
        self.dbInsert()

    def dbCreate(self):
        """
        crée la table dans la database si elle n'existe pas.
        """

        connection = sqlite3.connect(self.parameter["database"]["host"])
        cursor = connection.cursor()
        try:
            cursor.execute(f"""CREATE TABLE temperature(
                timestamp TEXT DEFAULT (datetime('now','localtime')),
                temperature REAL
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
            cursor.execute("INSERT INTO temperature(temperature) VALUES (?)", (str(
                int(self.status["temperature"]))))
        except sqlite3.Error as e:
            print(f"Temperature insert error: {e}")

        connection.commit()
        connection.close()
