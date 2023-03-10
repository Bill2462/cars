import yaml
from app import ZmqReceiver, MotorController

def load_config_file(filepath: str) -> dict:
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

def main():
    config = load_config_file("config.yaml")
    motor_controller = MotorController(config)
    receiver = ZmqReceiver(motor_controller, address=config["address"])
    print("Starting receiver...")
    receiver.run()

if __name__ == "__main__":
    main()
