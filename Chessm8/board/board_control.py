import serial

class BoardControl:
    def __init__(self, board_communication):
        self.board_communication = board_communication

    def get_board_state(self):
        res = self.board_communication.send(b"state")
        if res > -1:
            return res
        raise Exception("Failed to get board state")
