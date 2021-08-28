from elasticsearch_dsl import connections
import json

class Parser:
    indexname = "sbom-cyclonedx"

    def __init__(self):
        super().__init__()
    def fromFile(self, filepath, id=None):
        es = connections.get_connection()
        if filepath.endswith('.json'):
            with open(filepath) as f:
                content = f.read()
                es.index(index=self.indexname, body= json.loads(content), id=id)
