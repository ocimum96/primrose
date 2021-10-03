from elasticsearch_dsl import connections
from common.application import Application

class EShelper:
    
    @staticmethod
    def init_es():
        connections.create_connection(hosts=[Application.GetInstance().ConfigData["es"]["host"]])
    
    @staticmethod
    def remove_connection():
        connections.remove_connection("default")
