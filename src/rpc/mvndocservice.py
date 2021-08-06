import models.protobuf.primrose_pb2_grpc
from common.logger import Logger
from common.application import Application
from models.maven import ModelLibrary as MavenModel
from json import dumps

class MvnDocServiceServicer(models.protobuf.primrose_pb2_grpc.MavenDocServiceServicer):

    def Get(self, request, context):
        l = Logger.getLogger(__name__)
        l.info("Called RPC Get by id {}".format(request.id))

        dataModel = None
        resp = models.protobuf.primrose_pb2.MavenGetRespose()
        # status = models.protobuf.primrose_pb2.Status(code=0)
        try:
            dataModel = MavenModel.get(id=request.id)
            resp.doc = dumps(dataModel.to_dict(), default=str) 
        except Exception as e:
            l.critical("Get call failed.")
            l.debug(e)
            # status.msg = str(e)
            # status.code = 1
        # resp.status = status        
        l.debug("Returning data: " + resp.doc)
        return resp
    
    def Create(self, request, context):
        l = Logger.getLogger(__name__)
        l.info("Called RPC to create maven doc {}:{}:{}".format(request.groupID, request.artifactID, request.version))

        dataModel = MavenModel(groupID=request.groupID, artifactID=request.artifactID, version=request.version)
        if request.id or request.id != '' :
            l.info("Using ID :{}".format(request.id))
            dataModel.meta.id = request.id
        if request.purl or request.purl != '' :
            dataModel.purl = request.purl
        resp = ""
        try:
            resp = dataModel.save()
        except Exception as e:
            l.critical("Error on ES:save call.")
            l.debug(e)
        l.info("ES create call returned : {}".format(resp))
        return models.protobuf.primrose_pb2.Status(code=0 if str(resp) == "created" or 
        str(resp) == "updated" else 1, msg=str(resp))

    def Delete(self, request, context):
        l = Logger.getLogger(__name__)
        l.info("Calling ES:Delete on {}".format(request.id))
        dataModel = None
        errCode = 0
        errMsg = ""
        try:
            dataModel = MavenModel()
            dataModel.meta.id = request.id
            dataModel.delete()
        except Exception as e:
            l.critical("Delete call failed.")
            l.debug(e)
            errCode = 1
            errMsg = str(e)

        return models.protobuf.primrose_pb2.Status(code=errCode, msg=errMsg)

    # def Update(self, request, context):
    #     l = Logger.getLogger(__name__)
    #     l.info("Calling ES:Update on {}".format(request.id))
    #     l.debug(request.content)
    #     dataModel = None
    #     errCode = 0
    #     errMsg = ""
    #     try:
    #         dataModel = MavenModel()
    #         dataModel.meta.id = request.id
    #         dataModel.update()
    #     except Exception as e:
    #         l.critical("Update call failed.")
    #         l.debug(e)
    #         errCode = 1
    #         errMsg = str(e)

    #     return models.protobuf.primrose_pb2.Status(code=errCode, msg=errMsg)
        