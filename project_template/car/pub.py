import zmq
import time

class ZmqPublisher:
    def __init__(self, address):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(address)
        time.sleep(1)

    def send(self, topic, value):
        self.socket.send_string(topic, zmq.SNDMORE)
        self.socket.send_pyobj(value)
