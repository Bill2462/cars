import zmq
from motor_controller import MotorController, MotorCommand, InvalidCommandValue

class ZmqReceiver:
    def __init__(self, motor_controller: MotorController, address="tcp://localhost:5555",
                 topic=b"motor_commands"):

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(address)
        self.socket.setsockopt(zmq.SUBSCRIBE, topic)

        self.motor_controller = motor_controller
        self.error = False
    
    def run_command(self, cmd: str):
        if cmd == "CLEAR_ERROR":
            self.error = False
            print("Error cleared!")
        
    def run(self):
        while True:
            _ = self.socket.recv_string()
            packet = self.socket.recv_pyobj()

            if "cmd" in packet.keys():
                self.run_command(packet["cmd"])
            
            if self.error:
                continue

            try:
                command = MotorCommand(packet["throttle"], packet["steering"], packet["duration"])
                self.motor_controller.execute_command(command)
            
            except InvalidCommandValue as e:
                print(e.what())
                self.error = True
            
            except KeyError as e:
                print(e.what())
                self.error = True
