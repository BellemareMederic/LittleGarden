
import sqlite3
from config import Configuration


def createDBConnection():
    config = Configuration().config['database']['host']
    return sqlite3.connect(config)