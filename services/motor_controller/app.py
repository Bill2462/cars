import yaml
import sys
from app import ZmqReceiver, MotorController

def load_config_file(filepath: str) -> dict:
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

def main():
    config_filepath = sys.argv[1]
    config = load_config_file(config_filepath)

    motor_controller = MotorController(config)

    receiver = ZmqReceiver(motor_controller, address=config["address"])
    
    print("Starting receiver...")
    receiver.run()

if __name__ == "__main__":
    main()
