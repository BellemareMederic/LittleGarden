import yaml


class Configuration():
    def __init__(self):
        self.config = {
                'database': {'host': 'littleGarden', 'password': '', 'username': ''},
                'light': {'horaire': {'start': '08:25:00', 'end': '12:42:00'}, 'loop_delay': 10},
                'shutup': {'start': '20:00:00', 'end': '24:00:00'},
                'water': {'after': 5, 'loop_delay': 10, 'open': 10, 'targeted_moister': 2},
                'temperature': {'loop_delay': 10}
            }
        self.loadConfig()

    def loadConfig(self):
        with open("config.yml", 'r') as ymlfile:
            for doc in yaml.load_all(ymlfile, Loader=yaml.FullLoader):
                config.update(doc)
            self.config = config

    def saveConfig(self):
        print("saving data")
        with open('config.yml', 'w') as ymlfile:
            yaml.dump(self.config, ymlfile)

    def changeConfig(self, config):
        self.config = config
        self.saveConfig()