import threading
import time
class Chessm8Engine:
    def __init__(self, board_ctl, stockfish, lichess=None):
        self.lichess = lichess
        self.board_ctl = board_ctl
        self.stockfish = stockfish
    
    def start(self):
        # start a thread for board state changes
        state_thread = threading.Thread(target=self.board_state_loop)
        state_thread.start()


    def board_state_changed(self, state):
        pass

    def board_state_loop(self):
        while True:
            state = self.board_ctl.get_board_state()
            self.board_state_changed(state)
            time.sleep(0.5)
            


