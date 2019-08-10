


from Water import Water
import argparse
import sys
import os
import logging
import config

# Author Médéric Bellemare
# Début du projet 03-08-2019



if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", filename='software.log',level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    # parser.add_argument("-r", "--run", help="Run the automatique task with current configuration file", action="store_true")
    parser.add_argument("-v", "--verbose",type=int, help="Application talk to you more", choices=[0,1,2], default=0)
    args = parser.parse_args()
    if args.verbose in (0,1,2):
        root = logging.getLogger()
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

    pump = Water(5,10,1,0.1)
    pump.start()
    pump.join()

    