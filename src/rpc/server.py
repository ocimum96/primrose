from grpc import server as grpcServer
from concurrent import futures
import models.protobuf.primrose_pb2_grpc
from rpc.sbomservice import SbomServiceServicer

# add the following import statement to use server reflection
from grpc_reflection.v1alpha import reflection

class GrpcServer:
    def serve(self, max_workers):
        server = grpcServer(futures.ThreadPoolExecutor(max_workers=max_workers))
        models.protobuf.primrose_pb2_grpc.add_SbomServiceServicer_to_server(
            SbomServiceServicer(), server)
        SERVICE_NAMES = (
        models.protobuf.primrose_pb2.DESCRIPTOR.services_by_name['SbomService'].full_name,
        reflection.SERVICE_NAME,)
        reflection.enable_server_reflection(SERVICE_NAMES, server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()