
import sqlite3
from config import Configuration


def createDBConnection():
    config = Configuration().configObj['database']['host']
    return sqlite3.connect(config)