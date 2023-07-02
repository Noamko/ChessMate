
import Board
import threading
class StateObserver:
    def notify_state_changed(self, state):
        pass

class WaitForStateObserver(StateObserver):
    def __init__(self, state):
        self.state = state
        self.event = threading.Event()
    def notify_state_changed(self, state):
        # consider setting leds to green where pieces are in place and red where pieces are not in place
        if state == self.state:
            self.event.set()
    def wait(self):
        self.event.wait()
        
# test observer


                

                
        