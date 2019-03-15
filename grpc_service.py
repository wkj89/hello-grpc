import grpc

import greeter_pb2_grpc
import greeter_pb2
import socket
import time
from concurrent import futures
from log import init_system_logger
init_system_logger()

import logging

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Greeter(greeter_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        hostname = socket.gethostname()
        metadata = context.invocation_metadata()
        logging.info(metadata)
        logging.info("get request from %s ,hostname: %s" % (request.name, hostname))
        return greeter_pb2.HelloReply(message='Hello, %s , from %s!' % (request.name, hostname))

    def SayHelloAgain(self, request, context):
        return greeter_pb2.HelloReply(message='Hello again, %s!' % request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
