import models.protobuf.primrose_pb2_grpc
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
        resp = models.protobuf.primrose_pb2.SbomResponse(sbom=JsonDumps(getRes)) 
        return resp