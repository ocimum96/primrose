import models.protobuf.primrose_pb2_grpc
from common.logger import Logger
from common.application import Application
from models.maven import ModelLibrary as MavenModel
from json import dumps

class MvnDocServiceServicer(models.protobuf.primrose_pb2_grpc.MavenDocServiceServicer):

    def Get(self, request, context):
        l = Logger.getLogger(__name__)
        l.info("Called RPC Get by id {}".format(request.id))

        dataModel = MavenModel()
        resp = models.protobuf.primrose_pb2.MavenGetRespose()
        status = models.protobuf.primrose_pb2.Status(code=0)
        try:
            dataModel.get(id=request.id)
            print(dataModel.groupID)
            resp.doc = dumps(dataModel.to_dict())
        except Exception as e:
            l.critical("Get called failed.")
            l.debug(e)
            status.msg = str(e)
            status.code = 1
        # resp.status = status        
        l.debug("Got data: " + resp.doc)
        return resp
    
    def Create(self, request, context):
        l = Logger.getLogger(__name__)
        l.info("Called RPC to create maven doc {}:{}:{}".format(request.groupID, request.artifactID, request.version))

        dataModel = MavenModel(groupID=request.groupID, artifactID=request.artifactID, version=request.version)
        if request.id or request.id != '' :
            l.info("Using ID :{}".format(request.id))
            dataModel.meta.id = request.id
        resp = ""
        try:
            resp = dataModel.save()
        except Exception as e:
            l.critical("Error on ES:save call.")
            l.debug(e)
        l.info("ES create call returned : {}".format(resp))
        return models.protobuf.primrose_pb2.Status(code=1, msg=str(resp))