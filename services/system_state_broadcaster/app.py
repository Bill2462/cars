import yaml
from app.broadcaster import ValueBroadcaster
from app.ina219 import INA219
from app.jetson_status import *

def load_config_file(filepath: str) -> dict:
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

class BatteryBroadcaster:
    def __init__(self):
        self.ina = INA219(addr=66)

    def __call__(self):
        return self.ina.getBusVoltage_V()

def main():
    cfg = load_config_file("config.yaml")

    broadcaster = ValueBroadcaster((
        ("battery_voltage", BatteryBroadcaster()),
        ("cpu_usage", cpu_usage),
        ("gpu_usage", gpu_usage),
        ("power_mode", power_mode),
        ("power_usage", power_usage),
        ("memory_usage", memory_usage),
        ("disk_usage", disk_usage)),
        cfg["address"], cfg["delay"])

    broadcaster.run()

if __name__ == "__main__":
    main()
