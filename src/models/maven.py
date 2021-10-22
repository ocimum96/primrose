from datetime import datetime, timezone
from elasticsearch_dsl import Document, Nested, Boolean, \
    InnerDoc, Text, Date, Q
from common.logger import Logger
from common.application import Application
from packageurl import PackageURL


class ModelDependencyLink(InnerDoc):
    scope = Text()
    bomRef = Text() #PURL

class VersionInfo(InnerDoc):
    latestVersion = Text()
    lastCheck = Date(timezone.utc)

class LicenseInfo(InnerDoc):
    class License(InnerDoc):
        id = Text()
        class TextInfo(InnerDoc):
            contentType = Text()
            encoding = Text()
            content = Text()
        text = Nested(TextInfo)
        url = Text()
        name = Text()
    license = Nested(License)

class CopyrightsInfo(InnerDoc):
    id = Text()
    name = Text()
    email = Text()

class ModelLibrary(Document):
    groupID = Text(required=True)
    artifactID = Text(required=True)
    version = Text(required=True)
    purl = Text(required=True)
    fileType = Text() #POM or JAR
    versionInfo = Nested(VersionInfo)
    licenseInfo = [] #Array of LicenseInfo
    copyrightsInfo = Nested(CopyrightsInfo)
    scm = Text() #SCM URL

    tags = []
    lastModifiedAt = Date(timezone.utc) #timestamp field
    dependencies = [] #Nested(ModelDependencyLink)

    class Index:
        name =  Application.GetInstance().ConfigData["mvn"]["index"] #'maven-library'
    
    def save(self, **kwargs):
        l = Logger.getLogger(__name__)
        if not self.groupID or not self.artifactID or not self.version:
            print("GAV ID missing!!")
            return False
        self.lastModifiedAt = datetime.now(tz=timezone.utc).isoformat()
        if not self.purl or self.purl == '':
            purl = PackageURL(type="maven", namespace=self.groupID, name=self.artifactID,
                version=self.version, qualifiers=None, subpath=None)
            self.purl = purl.to_string()
            l.debug("set PURL as {}".format(self.purl))

        l.debug("PURL: {}".format(self.purl))
        if not hasattr(self.meta, 'id'):
            # no 'id' set, then its a create call not update call
            # so if mvn doc already exists for this PURL, dont create new.
            l.debug("Search for PURL if already exists: {}".format(self.purl))
            q = Q({
                    "bool": {
                        "must": [
                        {
                            "match_phrase": {
                            "purl": self.purl
                            }
                        }
                        ]
                    }
                    })
            s = ModelLibrary.search().query(q)
            searchResponse = s.execute()
            l.debug(s.to_dict())
            l.debug("Search by PURL hit count : {}".format(str(searchResponse.hits.total.value)))
            if searchResponse.hits.total.value > 0 :
                l.info("MVN doc with PURL {} already exists. Skipping creation.".format(self.purl))
                resp = "exists"
                return resp        


        l.info("Calling ES:save API...")
        resp = super().save(** kwargs)
        l.info("ES:Save returned: " + str(resp))
        return resp
    
    def add_dependency(self, scope, bomRef):
        self.dependencies.append(ModelDependencyLink(scope=scope, bomRef=bomRef))

    def add_versionInfo(self, latestVersion):
        self.versionInfo = VersionInfo(latestVersion=latestVersion, lastCheck=datetime.now(tz=timezone.utc).isoformat())
    
    def add_license(self, dataDict):
        # https://cyclonedx.org/use-cases/#license-compliance

        l = Logger.getLogger(__name__)
        license =  LicenseInfo.License()
        try:
            if "id" in dataDict:
                #SPDX License ID
                license.id = dataDict["id"]
                if "url" in dataDict:
                    license.url = dataDict["url"]
            elif "name" in dataDict:
                license.name = dataDict["name"]
            if "text" in dataDict:
                    if "content" in dataDict["text"]:
                        textInfo = LicenseInfo.License.TextInfo(content=dataDict["text"]["content"])
                        textInfo.contentType = "text/plain" if not "contentType" in dataDict["text"] else dataDict["contentType"]
                        textInfo.encoding = "none" if not "encoding" in dataDict["text"] else dataDict["encoding"]
                        license.TextInfo = textInfo
        except KeyError as e:
            l.critical("Key error: " + e)
            return False
        licenseInfo = LicenseInfo(license=license)
        self.licenseInfo.append(licenseInfo)
        return True

    def add_copyright(self, id, name, email):
        self.copyrightsInfo = CopyrightsInfo(id=id, name=name, email=email)

    def add_fileType(self, format):
        self.fileType = "JAR" if format != "" or format != "POM" else "POM"

    def add_scm(self, url):
        self.scm = url
    
    def add_tag(self, text):
        if text not in self.tags:
            self.tags.append(text)

