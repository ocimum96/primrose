import models.protobuf.primrose_pb2_grpc
from common.logger import Logger

class MvnDocServiceServicer(models.protobuf.primrose_pb2_grpc.MavenDocServiceServicer):

    def Get(self, request, context):
        l = Logger.getLogger(__name__)
        l.info("Called Get RPC.")
        
        resp = models.protobuf.primrose_pb2.MavenGetRespose(doc="{test}") 
        return resp