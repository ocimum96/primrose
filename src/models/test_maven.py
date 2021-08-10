import unittest
from models.maven import ModelLibrary
import common as c


class TestMavenModels(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):        
        c.Helpers.init_es()
        ModelLibrary.init()
    
    @classmethod
    def tearDownClass(cls):        
        c.Helpers.remove_connection()
    
    def setUp(self):
        self.libFlogger5 = ModelLibrary(group="com.google",artifacts="flogger",version="5.0") 
        self.libFlogger5.meta.id = "com.google:flogger:5.0"
        return super().setUp()

    def test_create_maven_model(self):
        self.libFlogger5.fileType = "pom"
        self.libFlogger5.lastModifiedBy = "ut"
        self.libFlogger5.latestVersion = "6.12"
        self.libFlogger5.licenseType = "MIT"
        self.libFlogger5.src = "https://github.com/google/flogger"
        # self.libFlogger5.tags = ["logger"]
        self.libFlogger5.add_dependency("pom", "org.apache.commons:lang:0.1")
        self.libFlogger5.add_dependency("pom", "org.oracle.xyz:abc:1.0")
        self.libFlogger5.add_tag("built-from-src")
        self.libFlogger5.add_tag("logger")
        self.libFlogger5.save()

        testFlogger = ModelLibrary.get(self.libFlogger5.meta.id)
        assert testFlogger.group is not None
        assert testFlogger.artifacts is not None
        assert testFlogger.version is not None

        assert "logger" in testFlogger.tags 
        assert len(testFlogger.dependencies) == 2
    
    def tearDown(self):
        self.libFlogger5.get(id="com.google:flogger:5.0")
        self.libFlogger5.delete()
        return super().tearDown()


    
