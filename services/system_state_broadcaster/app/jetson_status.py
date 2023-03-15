import subprocess
import psutil

def cpu_usage():
    """Gets the Jetson's current CPU usage fraction
    
    Returns:
        float: The current CPU usage fraction.
    """
    return psutil.cpu_percent()

def gpu_usage():
    """Gets the Jetson's current GPU usage fraction
    
    Returns:
        float: The current GPU usage fraction.
    """
    with open('/sys/devices/gpu.0/load', 'r') as f:
        return float(f.read().strip('\n')) / 1000.0

def power_mode():
    """Gets the Jetson's current power mode
    
    Gets the current power mode as set by the tool ``nvpmodel``.
    
    Returns:
        str: The current power mode.  Either 'MAXN' or '5W'.
    """
    return subprocess.check_output("nvpmodel -q | grep -o '5W\|MAXN'", shell = True ).decode('utf-8').strip('\n')

def power_usage():
    """Gets the Jetson's current power usage in Watts
    
    Returns:
        float: The current power usage in Watts.
    """
    with open("/sys/devices/50000000.host1x/546c0000.i2c/i2c-6/6-0040/iio:device0/in_power0_input", 'r') as f:
        return float(f.read()) / 1000.0

def memory_usage():
    """Gets the Jetson's current RAM memory usage fraction
    
    Returns:
        float: The current RAM usage fraction.
    """
    return float(subprocess.check_output("free -m | awk 'NR==2{printf \"%.2f\", $3*100/$2 }'", shell = True ).decode('utf-8')) / 100.0

def disk_usage():
    """Gets the Jetson's current disk memory usage fraction
    
    Returns:
        float: The current disk usage fraction.
    """
    return float(subprocess.check_output("df -h | awk '$NF==\"/\"{printf \"%s\", $5}'", shell = True ).decode('utf-8').strip('%')) / 100.0
