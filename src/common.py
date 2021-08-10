from elasticsearch_dsl import connections

class Helpers:
    
    @staticmethod
    def init_es():
        connections.create_connection(hosts=['localhost:49154'])
    
    @staticmethod
    def remove_connection():
        connections.remove_connection("default")
