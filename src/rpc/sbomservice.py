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
            status=models.protobuf.primrose_pb2.Status(code=0)) 
            return resp
        else:
            return models.protobuf.primrose_pb2.SbomResponse(sbom="",
            status=models.protobuf.primrose_pb2.Status(code=1, msg="Response data is None."))