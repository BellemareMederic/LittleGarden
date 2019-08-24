#!/usr/bin/env python3
"""
LittleGarden automatic controle
"""
__author__ = "Médéric Bellemare"
__version__ = "0.1.0"
__license__ = "MIT"


from Water import Water
from Light import Light
import os, argparse, time
import threading
from datetime import datetime, timedelta
import time
from config import Configuration
from flask import Flask, jsonify, request, Response

def server(config=None):
    app = Flask(__name__)
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})
    
    @app.route("/")
    def hello_world():
        return "Hello there please read the user manuel :D"

    @app.route("/api/v1/status", methods=['GET','POST'])
    def routeWaterStatus():
        if request.method == "GET":
            # return jsonify(waterThread.getStatus())
            return jsonify({
                "serverTime": datetime.now(),
                "water": waterThread.status,
                "light": lightThread.status
            })
        elif request.method == "POST":
            if "name" in request.json:
                return request.json["name"]
            return Response(status = 501)

    @app.route("/api/v1/force/<class_>", methods=["GET"])
    def routeWaterForce(class_):
        if(class_ == "water"):
            waterThread.status["isForceWatering"] = True
        elif(class_ == "light"):
            lightThread.forceLight()
        else:
            return Response(f"Cannot find the service =(", 406)
        return Response(f"OK i will force the {class_}", 200)
        
    @app.route("/api/v1/parameter", methods=['GET','POST','OPTIONS'])
    def routeWaterParameter():
        if request.method == "GET":
            return jsonify(mainConfig)

        elif request.method == "POST":
            return jsonify(request.json)

        elif request.method == "OPTIONS":
            keys=[i for i in mainConfig.keys()]
            return {"options":keys}

        
    return app

if __name__ == "__main__":

    mainConfig = Configuration().configObj

    waterThread = Water(mainConfig)
    waterThread.setDaemon(True)
    waterThread.start()
    lightThread = Light(mainConfig)
    lightThread.setDaemon(True)
    lightThread.start()

    webServer = server()
    webServer.run(host=mainConfig['webserver']['host'], port=mainConfig['webserver']['port'],threaded=True,use_reloader=False)

    