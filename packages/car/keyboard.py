import evdev
import threading

class Keyboard:
    def __init__(self, address='/dev/input/event2'):
        self.device = evdev.InputDevice(address)
        
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
    
    def _process_event(self, event):
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            if key_event.keycode  == "KEY_UP":
                self.UP = key_event.keystate > 0

            if key_event.keycode == "KEY_DOWN":
                self.DOWN = key_event.keystate > 0
                
            if key_event.keycode == "KEY_LEFT":
                self.LEFT = key_event.keystate > 0

            if key_event.keycode == "KEY_RIGHT":
                self.RIGHT = key_event.keystate > 0
    
    def start_listening(self):
        def wrapper():
            for event in self.device.read_loop():
                self._process_event(event)
        
        self.thread = threading.Thread(target=wrapper)
        self.thread.start()
