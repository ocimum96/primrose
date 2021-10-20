from elasticsearch_dsl import connections
from elasticsearch.exceptions import NotFoundError
import json
from datetime import datetime, timezone
from common.logger import Logger

class Parser:
    indexname = "sbom-cyclonedx"
    timeStampField = "modified-at"

    def __init__(self):
        super().__init__()
    def fromFile(self, filepath, purl=None, id=None):
        es = connections.get_connection()
        if filepath.endswith('.json'):
            with open(filepath) as f:
                content = f.read()
                jsonContent = json.loads(content)                
                Parser.filtersBeforeUpdate(jsonContent)
                if purl is not None:
                    jsonContent["purl"] = purl
                r = es.index(index=self.indexname, body=jsonContent, id=id)
                if r is not None and "_id" in r:
                    idCreated = r["_id"]
                    return idCreated
                else:
                    return None
    
    @staticmethod
    def filterBeforeUpdate(sbomDict):
        sbomDict[Parser.timeStampField] = datetime.now(tz=timezone.utc).isoformat()


class Data:    

    def __init__(self):
        self.l = Logger.getLogger(__name__)
        super().__init__()

    def get(self, id):        
        self.l.info("Get SBOM by ID {} ".format(id))
        try:
            es = connections.get_connection()
            res = es.get(index=Parser.indexname, id=id)
            return res['_source']
        except NotFoundError as e:
            self.l.info("Doc not found.")
            self.l.debug(e)
            return None
        except Exception as e:
            self.l.critical("Exception occured while ES call.")
            self.l.debug(e)
            return None

    
    def create(self, data, docId=None):        
        self.l.info("Creating SBOM..")
        res = False
        try:
            es = connections.get_connection()
            jsonContent = json.loads(data)
            Parser.filterBeforeUpdate(jsonContent)
            res = es.index(index=Parser.indexname, id=docId, body=jsonContent)
        except Exception as e:
            self.l.critical("ES: Create call failed.")
            self.l.debug(e)
        self.l.info("ES:Create call returned " + str(res["result"]))
        return res

    def update(self, id, content):        
        self.l.info("Calling ES:Update..")
        resp = False
        try:
            es = connections.get_connection()
            jsonContent = json.loads(content)
            Parser.filterBeforeUpdate(jsonContent["doc"])
            resp = es.update(index=Parser.indexname, id=id, body=json.dumps(jsonContent))
        except KeyError as e:
            self.l.fatal("Update format not correct. Key not found: " + e)
        except Exception as e:
            self.l.critical("ES: Update call failed.")
            self.l.debug(e)
        return resp

    def delete(self, id):        
        self.l.info("Calling ES:delete on id {}.".format(id))
        res = False
        try:
            es = connections.get_connection()
            res = es.delete(index=Parser.indexname, id=id)
        except Exception as e:
            self.l.critical("ES: Delete call failed.")
            self.l.debug(e)
        return res
