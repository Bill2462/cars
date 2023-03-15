import yaml
import threading
import zmq
import json
import sys
from PIL import Image
from io import BytesIO
from flask import Flask, request, send_file

class TelemetryReceiver:
    def __init__(self, address):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(address)
        self.socket.subscribe("")
        
        self.buf = {}

    def _process_data(self):
        topic = self.socket.recv_string()
        value = self.socket.recv_pyobj()
        self.buf[topic] = value

    def start(self):
        def wrapper():
            while 1:
                self._process_data()
            
        self.thread = threading.Thread(target=wrapper)
        self.thread.start()
    
    def get_all(self):
        return self.buf

    def get_by_topic(self, topic):
        return self.buf[topic]
    
def load_config_file(filepath: str) -> dict:
    with open(filepath, "r") as f:
        return yaml.safe_load(f)
    
def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, "JPEG", quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype="image/jpeg")

def form_json_response(input):
    if not input:
        return {}
    
    # Case for get_all
    if isinstance(input, dict):
        return input

    return {"timestamp": input[0], "data": input[1]}

config_filepath = sys.argv[1]
cfg = load_config_file(config_filepath)

motor_command_receiver = TelemetryReceiver(cfg["motor_command_address"])
system_telemetry_receiver = TelemetryReceiver(cfg["system_telemetry_address"])
user_telemetry_receiver = TelemetryReceiver(cfg["user_telemetry_address"])
user_telemetry_img_receiver = TelemetryReceiver(cfg["user_telemetry_img_address"])

system_telemetry_receiver.start()
motor_command_receiver.start()
user_telemetry_receiver.start()
user_telemetry_img_receiver.start()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Server is running"

@app.route("/motor_commands")
def get_motor_commands():
    return json.dumps(form_json_response(motor_command_receiver.get_by_topic("motor_commands")))

@app.route("/system_telemetry")
def get_system_telemetry():
    return json.dumps(form_json_response(system_telemetry_receiver.get_all()))

@app.route("/user_telemetry")
def get_user_telemetry():
    name = request.args.get("name")
    print(name)
    return json.dumps(form_json_response(user_telemetry_receiver.get_by_topic(name)))

@app.route("/images")
def get_image():
    image_name = request.args.get("name")
    image = Image.fromarray(user_telemetry_img_receiver.get_by_topic(image_name)[1])
    return serve_pil_image(image)
