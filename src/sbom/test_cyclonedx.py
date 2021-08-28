import unittest
from common import helpers
from sbom.cyclonedx import Parser 
from elasticsearch_dsl import Index, Document, Text
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
        testDocId = "test-doc-1"
        p.fromFile(fileToTest, id=testDocId)
        self.toDeleteDoc.append(testDocId)

        i = Index(p.indexname)
        
        assert i.exists()
        self.toDeleteIndices.append(p.indexname) 

        @i.document
        class doc(Document):
            serialNumber = Text()
        
        serialNoToCheck = ""
        with open(fileToTest) as f:
            serialNoToCheck = json.loads(f.read())["serialNumber"]
        
        fromEs = doc().get(testDocId)
        
        assert fromEs is not None

        assert fromEs.serialNumber.__str__() == serialNoToCheck
    
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