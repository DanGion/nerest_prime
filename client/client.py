import pika
import uuid
from flask import Flask, jsonify, request

app = Flask(__name__)


class NearestPrimeRpcClient(object):
    _response = None
    _corr_id = None

    def __init__(self):
        host = 'rabbitmq'
        port = 5672
        print('%s:%s' % (host, port))
        parameters = pika.ConnectionParameters(host,
                                               port,
                                               '/',
                                               pika.PlainCredentials('guest', 'guest'))
        self._connection = pika.BlockingConnection(parameters)

        self._channel = self._connection.channel()

        result = self._channel.queue_declare(queue='', exclusive=True)
        self._callback_queue = result.method.queue

        self._channel.basic_consume(
            queue=self._callback_queue,
            on_message_callback=self._on_response,
            auto_ack=True)

    def _on_response(self, ch, method, props, body):
        if self._corr_id == props.correlation_id:
            self._response = body

    def call(self, n):
        self._corr_id = str(uuid.uuid4())
        self._channel.basic_publish(
            exchange='',
            routing_key='nearest_prime',
            properties=pika.BasicProperties(
                reply_to=self._callback_queue,
                correlation_id=self._corr_id,
            ),
            body=str(n))
        while self._response is None:
            self._connection.process_data_events()
        return int(self._response)


@app.route('/', methods=['GET'])
def get_root():
    return 'POST JSON содерщащий только число (пр. 1) в ./prime/nearest'


@app.route('/prime/nearest', methods=['POST'])
def get_nearest():
    content = request.get_json(silent=True)
    return jsonify(NearestPrimeRpcClient().call(content))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

