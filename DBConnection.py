
import sqlite3


class DBConnection(object):
    connector = null

    def __init__(self, Config):
        self.connector = sqlite3.connect(Config.parameter['database']['host'])

    def createConnection(self):
        return sqlite3.connect()