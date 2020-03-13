#!/usr/bin/env python3
"""
LittleGarden automatic controler
"""
from lib.Water import Water
from lib.Light import Light
from lib.Temperature import Temperature
from datetime import datetime, timedelta
from functools import wraps
import time
from config import Configuration
from flask import Flask, jsonify, request, Response, render_template
from flask_cors import CORS, cross_origin
from lib.DBConnection import *

__author__ = "Médéric Bellemare"
__version__ = "0.1.0"
__license__ = "MIT"


def needAPIKey(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if("KEY" in request.headers):
            if("api-key" in mainConfig['webserver']):
                if(request.headers["KEY"] != mainConfig['webserver']['api-key']):
                    return Response("401 - Access denied.", 401)
            else:
                raise Exception(
                    "You need to define you api-key in the config.yml")
        else:
            return Response("401 - Access denied.", 401)
        return func(*args, **kwargs)

    return decorated_function


def server(config=None):
    app = Flask(__name__, static_folder="./dist/static",
                template_folder="./dist")
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.update(dict(DEBUG=True))

    @app.route("/", methods=['GET'])
    def hello_world():
        return render_template("index.html")

    @app.route("/api/v1/status", methods=['GET', 'POST'])
    @needAPIKey
    def routeWaterStatus():
        if request.method == "GET":
            # return jsonify(waterThread.getStatus())
            return jsonify({
                "serverTime": datetime.now(),
                "water": waterThread.status,
                "light": lightThread.status,
                "temperature": temperatureThread.status
            })
        elif request.method == "POST":
            if "name" in request.json:
                return request.json["name"]
            return Response(status=501)

    @app.route("/api/v1/force/<class_>", methods=["GET"])
    @needAPIKey
    def routeWaterForce(class_):
        if(class_ == "water"):
            waterThread.status["isForceWatering"] = True
        elif(class_ == "light"):
            lightThread.status["isForceLight"] = True
        else:
            return Response(f"Cannot find the service =(", 406)
        return Response(f"OK i will force the {class_}", 200)

    @app.route("/api/v1/parameter", methods=['GET', 'POST', 'OPTIONS'])
    @needAPIKey
    def routeWaterParameter():
        if request.method == "GET":
            return jsonify(mainConfig)

        elif request.method == "POST":
            return jsonify(request.json)

        elif request.method == "OPTIONS":
            keys = [i for i in mainConfig.keys()]
            return {"options": keys}

    @app.route("/api/v1/history", methods=['GET'])
    @cross_origin(origin='*')
    @needAPIKey
    def history(): 
        # return jsonify(dict(name='water', data=waterThread.dbBetween(request.args)), dict(name='light', data=lightThread.dbBetween(request.args)), dict(name='temperature', data=temperatureThread.dbBetween(request.args)))
        return jsonify({'water': dict(name='water', data=waterThread.getAvgHumidityDay(request.args)),
                        'light': dict(name="light", data='light'),
                        'temperature': dict(name="temperature", data='temperature')})
        return Response(f"Missing parameter")

    @app.route("/api/v1/history/avg", methods=['GET'])
    @cross_origin(origin='*')
    @needAPIKey
    def avg():
        humidity, water = waterThread.dbGetAvgWeek(request.args.get('startdate'), request.args.get('enddate'))
        # return jsonify(dict(name='water', data=waterThread.dbBetween(request.args)), dict(name='light', data=lightThread.dbBetween(request.args)), dict(name='temperature', data=temperatureThread.dbBetween(request.args)))
        return jsonify(moyenne = dict(humidity=humidity,water=water))

    return app


if __name__ == "__main__":
    mainConfig = Configuration().configObj

    dbsql = createDBConnection()

    waterThread = Water(mainConfig)
    waterThread.setDaemon(True)
    waterThread.start()
    lightThread = Light(mainConfig)
    lightThread.setDaemon(True)
    lightThread.start()
    temperatureThread = Temperature(mainConfig)
    temperatureThread.setDaemon(True)
    temperatureThread.start()

    webServer = server()
    webServer.run(host=mainConfig['webserver']['host'],
                  port=mainConfig['webserver']['port'], 
                  threaded=True,
                  use_reloader=False)
