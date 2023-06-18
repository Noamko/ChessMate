import serial
import time

class Commands:
    PING_REQUEST = 0xA0
    PING_RESPONSE = 0xA1
    BOARD_STATE_CHANGED = 0xAA
    GET_BOARD_STATE_REQUEST = 0xA2
    GET_BOARD_STATE_RESPONSE = 0xA3
    SET_LEDS_STATE_REQUEST = 0xA4
    SET_LEDS_STATE_RESPONSE = 0xA5
    GET_LAST_MODIFED_SQUARE_REQUEST = 0xA6
    GET_LAST_MODIFED_SQUARE_RESPONSE = 0xA7

class BoardRequest:
    @staticmethod
    def create(command, args) -> bytes:
        return bytes([command, len(args)]) + bytes(args) 

class BoardResponse:
    def __init__(self, data):
        self.id = data[0]
        self.args_len = data[1:5]
        self.args = data[5:]

class SerialCommunication:
    def __init__(self, port, baudrate):
        self.serial = serial.Serial(port, baudrate)
        time.sleep(3) # wait for the board to boot
    def send(self, data):
        self.serial.write(data)
    def read(self, count) -> bytes:
        return self.serial.read(count)


