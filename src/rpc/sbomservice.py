import models.protobuf.primrose_pb2_grpc
from common.logger import Logger

class SbomServiceServicer(models.protobuf.primrose_pb2_grpc.SbomServiceServicer):

    def Get(self, request, context):
        l = Logger.getLogger(__name__)
        l.info("Called Get RPC.")
        l.debug("Get by id: {}".format(request.sbomID))
        resp = models.protobuf.primrose_pb2.SbomResponse(sbom="{ \"key\":44 }") 
        return resp