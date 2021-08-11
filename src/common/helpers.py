from elasticsearch_dsl import connections
import common.myapp as myapp

class EShelper:
    
    @staticmethod
    def init_es():
        connections.create_connection(hosts=[myapp.app.ConfigData["es"]["host"]])
    
    @staticmethod
    def remove_connection():
        connections.remove_connection("default")
