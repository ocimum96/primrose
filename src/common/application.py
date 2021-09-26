from common.logger import Logger
import json

class _singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Application(metaclass=_singleton):
    _configFilePath = "config.json"

    def __init__(self):
        l = Logger.getLogger(__name__)
        l.info("my app init called.")
        with open(self._configFilePath, 'r') as configFile:
            self.ConfigData = json.load(configFile)
        super().__init__()
    
    @staticmethod
    def GetInstance():
        return Application()