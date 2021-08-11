import json

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        
class Logger(metaclass=Singleton):
    pass

class Myapp(metaclass=Singleton):
    ConfigFilePath = "config.json"
    def __init__(self):
        print("my app init called..")
        with open(self.ConfigFilePath, 'r') as configFile:
            self.ConfigData = json.load(configFile)
        super().__init__()
                                                                                                                                                                                                
app = Myapp()     