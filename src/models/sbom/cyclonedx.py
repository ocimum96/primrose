from elasticsearch_dsl import connections
import json
from datetime import datetime, timezone

class Parser:
    indexname = "sbom-cyclonedx"
    timeStampField = "created_at"

    def __init__(self):
        super().__init__()
    def fromFile(self, filepath, purl=None, id=None):
        es = connections.get_connection()
        if filepath.endswith('.json'):
            with open(filepath) as f:
                content = f.read()
                jsonContent = json.loads(content)                
                jsonContent[Parser.timeStampField] = datetime.now(tz=timezone.utc).isoformat()
                if purl is not None:
                    jsonContent["purl"] = purl
                r = es.index(index=self.indexname, body= jsonContent, id=id)
                if r is not None and "_id" in r:
                    idCreated = r["_id"]
                    return idCreated
                else:
                    return None

