from .pub import ZmqPublisher
from .misc import time_ms

class TelemetrySender:
    def __init__(self, address_regular="tcp://*:5557",
                 address_img="tcp://*:5558"):
        self.pub = ZmqPublisher(address_regular)
        self.pub_img = ZmqPublisher(address_img)

    def log_image(self, name, val):
        self.pub_img.send(name, (time_ms(), val))

    def log(self, name, val):
        self.pub.send(name, (time_ms(), val))
