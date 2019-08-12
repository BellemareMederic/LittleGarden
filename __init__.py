#!/usr/bin/env python3
"""
LittleGarden automatic controle
"""
__author__ = "Médéric Bellemare"
__version__ = "0.1.0"
__license__ = "MIT"


from Water import Water
import config, os, argparse, time
import threading
from flask import Flask, jsonify, request, Response

test = 0

def create_app(config=None):
    app = Flask(__name__)
    # See http://flask.pocoo.org/docs/latest/config/
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    

    # Definition of the routes. Put them into their own file. See also
    # Flask Blueprints: http://flask.pocoo.org/docs/latest/blueprints
    @app.route("/")
    def hello_world():
        return "Hello there please read the user manuel :D"

    @app.route("/api/v1/water/status", methods=['GET','POST','OPTIONS'])
    def routeWaterStatus():
        if request.method == "GET":
            return jsonify(waterThread.getStatus())
        elif request.method == "POST":
            if "name" in request.json:
                return request.json["name"]
            return Response(status = 501)
        elif request.method == "OPTIONS":
            keys=[i for i in waterThread.parameter.keys()]
            return {"options":keys}
        
    @app.route("/api/v1/water/parameter", methods=['GET','POST','OPTIONS'])
    def routeWaterParameter():
        print(request.method)
        if request.method == "GET":
            return jsonify(waterThread.parameter)
        elif request.method == "POST":
            return jsonify(request.json)
        elif request.method == "OPTIONS":
            keys=[i for i in waterThread.parameter.keys()]
            return {"options":keys}
    
    @app.route("/api/v1/light/status")
    def routeLightStatus():
        return Response(status = 501)
    
    @app.route("/api/v1/light/parameter")
    def routeLightParameter():
        return Response(status = 501)
    

    return app
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", action="store", default="8000")
    args = parser.parse_args()
    port = int(args.port)

    waterThread = Water(5,10,1)
    waterThread.setDaemon(True)
    waterThread.start()
    
    webServer = create_app()
    webServer.run(host="127.0.0.1", port=port, threaded=True)

