import unittest
from common import helpers
from models.sbom.cyclonedx import Parser 
from elasticsearch_dsl import Index, Document, Text, Date
import json

class TestCyclonedx(unittest.TestCase):

    @classmethod
    def setUpClass(cls):        
        helpers.EShelper.init_es()
    
    @classmethod
    def tearDownClass(cls):        
        helpers.EShelper.remove_connection()
    
    def setUp(self):
        self.toDeleteDoc = []
        self.toDeleteIndices = []
        return super().setUp()

    def test_from_file(self):
        fileToTest = "sbom/ut_files/sbom1.json"
        p = Parser()
        p.indexname = "test-" + Parser.indexname        
        testDocPurl = "sbom:cyclonedx/org.ocimum.primrose.sbom/cyclonedx@0.0.1"
        testDocId = p.fromFile(fileToTest, purl=testDocPurl)
        assert testDocId is not None
        self.toDeleteDoc.append(testDocId)

        i = Index(p.indexname)
        
        assert i.exists()
        self.toDeleteIndices.append(p.indexname) 

        @i.document
        class doc(Document):
            serialNumber = Text()
            created_at = Date()
        
        serialNoToCheck = ""
        with open(fileToTest) as f:
            serialNoToCheck = json.loads(f.read())["serialNumber"]
        
        fromEs = doc().get(testDocId)
        
        assert fromEs is not None

        assert fromEs.serialNumber.__str__() == serialNoToCheck

        assert fromEs.created_at is not None
    
    def tearDown(self):
        i = Index("test-" + Parser.indexname)
        if (i.exists()):
            @i.document
            class doc(Document):
                serialNumber = Text()
            dlist = doc.mget(self.toDeleteDoc)
            for d in dlist:
                d.delete()
        return super().tearDown()

if __name__=="__main__":
    unittest.main()