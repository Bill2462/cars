import zmq
import time
import threading
import time

def time_ms():
    return int(round(time.time() * 1000))

class ValueBroadcaster:
    def __init__(self, producers, address="tcp://*:5556", delay=None):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(address)

        self.producers = producers
        self.address = address
        self.delay = delay
    
    def _send_values(self):
        for name, producer in self.producers:
            self.socket.send_string(name, zmq.SNDMORE)
            self.socket.send_pyobj((time_ms(), producer()))
    
    def run(self):
        def wrapper():
            while 1:
                self._send_values()
                time.sleep(self.delay)
            
        self.thread = threading.Thread(target=wrapper)
        self.thread.start()
