from datetime import datetime
from elasticsearch_dsl import Document, Nested, Boolean, \
    InnerDoc, Text, Date


class ModelDependencyLink(InnerDoc):
    dependencyType = Text()
    dependencyText = Text()


class ModelLibrary(Document):
    group = Text()
    artifacts = Text()
    version = Text()
    fileType = Text()
    latestVersion = Text()
    licenseType = Text()
    src = Text()

    tags = []
    lastModifiedAt = Date()
    lastModifiedBy = Text()
    createdAt = Date() 
    dependencies = Nested(ModelDependencyLink)

#     def __init__(self, group, artifacts, version):
#        self.group = group
#        self.artifacts = artifacts
#        self.version = version

    class Index:
        name = 'maven-library'
    
    def save(self, **kwargs):
        if not self.group or not self.artifacts or not self.version:
            print("GAV ID missing!!")
            return 1 
        self.createdAt = datetime.now()
        self.lastModifiedAt = datetime.now()
        return super().save(** kwargs)
    
    def add_dependency(self, dependencyType, text):
        self.dependencies.append(ModelDependencyLink(dependencyType=dependencyType, dependencyText=text))
    
    def add_tag(self, text):
        if text not in self.tags:
            self.tags.append(text)

