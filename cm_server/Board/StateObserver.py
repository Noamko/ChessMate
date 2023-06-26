
import Board
class StateObserver:
    def notify(self, state):
        pass

class WaitForStateObserver(StateObserver):
    def __init__(self, state):
        self.state = state
        self.event = threading.Event()
    def notify(self, state):
        # consider setting leds to green where pieces are in place and red where pieces are not in place
        if state == self.state:
            self.event.set()
    def wait(self):
        self.event.wait()
        
# test observer
class PieceToLedStateObserver(StateObserver):
    def __init__(self, board_ctl):
        self.board_ctl = board_ctl
    def notify(self, state):
        sel.board_ctl.setLedsState(state)

                

                
        