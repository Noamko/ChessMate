import serial
import time
import commands

class BoardMessage:
    @staticmethod
    def create(self, command, args_len, args) -> bytes:
        pass

class SerialCommunication:
    def __init__(self, port, baudrate):
        self.serial = serial.Serial(port, baudrate)
        time.sleep(5) # wait for the board to boot
    def send(self, data):
        self.serial.write(data)
    def read(self, count) -> bytes:
        return self.serial.read(count)
    
class BoardController:
    def __init__(self, board_communication):
        self.board_communication = board_communication
    def set_leds_state(self, state):
        pass
    def get_board_state(self):
        res = self.board_communication.send(b"state")
        if res > -1:
            return res
        raise Exception("Failed to get board state")
