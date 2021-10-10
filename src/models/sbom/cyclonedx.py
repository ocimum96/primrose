from elasticsearch_dsl import connections
from elasticsearch.exceptions import NotFoundError
import json
from datetime import datetime, timezone
from common.logger import Logger

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
                r = es.index(index=self.indexname, body=jsonContent, id=id)
                if r is not None and "_id" in r:
                    idCreated = r["_id"]
                    return idCreated
                else:
                    return None


class Data:
    def get(self, id):
        l = Logger.getLogger(__name__)
        l.info("Get SBOM by ID {} ".format(id))
        try:
            es = connections.get_connection()
            res = es.get(index=Parser.indexname, id=id)
            return res['_source']
        except NotFoundError as e:
            l.info("Doc not found.")
            l.debug(e)
            return None
        except Exception as e:
            l.critical("Exception occured while ES call.")
            l.debug(e)
            return None