import grpc
import greeter_pb2_grpc
import greeter_pb2
import prometheus_client
from prometheus_client import Counter

from flask import Response, Flask, request

app = Flask(__name__)

requests_total = Counter("request_count", "Total request cout of the host")
channel = grpc.insecure_channel('test-greeter:50051')
greeter_client = greeter_pb2_grpc.GreeterStub(channel)


@app.route("/metrics")
def requests_count():
    return Response(prometheus_client.generate_latest(requests_total),
                    mimetype="text/plain")


@app.route('/<name>', methods=['GET'])
def hello(name):
    requests_total.inc()
    response = greeter_client.SayHello(greeter_pb2.HelloRequest(name=name))

    return response.message


@app.route('/live', methods=['GET'])
def live():
    return 'ok'


if __name__ == '__main__':
    app.run("0.0.0.0",4000)