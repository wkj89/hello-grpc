import grpc
import greeter_pb2_grpc
import greeter_pb2
import prometheus_client
from prometheus_client import Counter

from flask import Response, Flask, request, make_response
from interceptor import header_adder_interceptor
from log import init_log

init_log()
app = Flask(__name__)

requests_total = Counter("request_count", "Total request cout of the host")
channel = grpc.insecure_channel('test-greeter:50051')

header_interceptor = header_adder_interceptor(request)

intercept_channel = grpc.intercept_channel(channel, header_interceptor)

greeter_client = greeter_pb2_grpc.GreeterStub(intercept_channel)

retry_count = {}


@app.route("/metrics")
def requests_count():
    return Response(prometheus_client.generate_latest(requests_total),
                    mimetype="text/plain")


@app.route('/<name>', methods=['GET'])
def hello(name):
    requests_total.inc()
    response = greeter_client.SayHello(greeter_pb2.HelloRequest(name=name, age=1))
    return response.message


@app.route('/retry/<name>', methods=['GET'])
def retry(name):
    global retry_count
    pre_count = retry_count.get(name, 0)

    n = retry_count.get(name, '')
    if n:
        n += 1
        retry_count[name] = n
    else:
        n = 1
        retry_count[name] = n
    response = make_response()
    response.status_code = 503

    response.response = "pre retry count {}".format(pre_count)
    return response


@app.route('/live', methods=['GET'])
def live():
    return 'ok'


if __name__ == '__main__':
    app.run("0.0.0.0", 4000)
