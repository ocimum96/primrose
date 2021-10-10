import models.protobuf.primrose_pb2_grpc
import models.protobuf.primrose_pb2
from common.logger import Logger
from models.sbom.cyclonedx import Data as SbomData
from json import dumps as JsonDumps

class SbomServiceServicer(models.protobuf.primrose_pb2_grpc.SbomServiceServicer):

    def Get(self, request, context):
        l = Logger.getLogger(__name__)
        l.info("Called Get RPC.")
        l.debug("Get by id: {}".format(request.sbomID))
        sbomData = SbomData()
        getRes = sbomData.get(request.sbomID)
        if getRes is not None:
            resp = models.protobuf.primrose_pb2.SbomResponse(sbom=JsonDumps(getRes),
            status = models.protobuf.primrose_pb2.Status(code=0)) 
            return resp
        else:
            return models.protobuf.primrose_pb2.SbomResponse(sbom="",
            status=models.protobuf.primrose_pb2.Status(code=1, msg="Response data is None."))
    
    def Create(self, request, context):
        l = Logger.getLogger(__name__)
        l.info("Called Create RPC.")
        if request.id is not None:
            l.debug("ID: {}".format(request.id)) 
        sbomData = SbomData()
        res = sbomData.create(request.content, request.id if request.id is not "" else None )
        return models.protobuf.primrose_pb2.Status(code=0 if res else 2 )

    def Update(self, request, context):
        l = Logger.getLogger(__name__)
        l.info("Called Update RPC on id {}.".format(request.id))
        sbomData = SbomData()
        res = sbomData.update(request.id, request.newSBomContent)
        return models.protobuf.primrose_pb2.Status(code=0 if res else 3)

    def Delete(self, request, context):
        l = Logger.getLogger(__name__)
        l.info("Called Delete RPC on id {}.".format(request.id))
        sbomData = SbomData()
        res = sbomData.delete(request.id)
        return models.protobuf.primrose_pb2.Status(code=0 if res else 4)