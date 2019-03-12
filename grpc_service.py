import grpc

import greeter_pb2_grpc
import greeter_pb2
import logging
import socket
import time
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

file_handler = logging.FileHandler("/log/grpc.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] - %(levelname)s -%(filename)s -%(lineno)d - %(message)s')

file_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.INFO)


class Greeter(greeter_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        hostname = socket.gethostname()

        print("get request from %s ,hostname: %s" % (request.name, hostname))
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
