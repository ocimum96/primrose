from rpc.server import GrpcServer
from common.helpers import EShelper
from common.logger import Logger

if __name__ == '__main__':
    l = Logger.getLogger(__name__)
    l.info("Creating ES connection..")
    EShelper.init_es()
    l.info("Starting GRPC server..")
    GrpcServer().serve(1)