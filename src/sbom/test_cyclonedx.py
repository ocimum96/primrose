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

    def test_from_file(self):
        fileToTest = "sbom/ut_files/sbom1.json"
        p = Parser()
        p.indexname = "test-" + Parser.indexname
        p.fromFile(fileToTest)
        i = Index(p.indexname)
        
        assert i.exists()

        @i.document
        class doc(Document):
            serialNumber = Text()
        
        s = i.search()
        serialNoToCheck = ""
        with open(fileToTest) as f:
            serialNoToCheck = json.loads(f.read())["serialNumber"]
        
        r = s.execute()
        
        assert s.count() > 0

        for d in s:
            assert d.serialNumber.__str__() == serialNoToCheck
    
    def tearDown(self):
        i = Index("test-" + Parser.indexname)
        if (i.exists()):
            s = i.search()
            for d in s:
                d.delete()
        return super().tearDown()

if __name__=="__main__":
    unittest.main()