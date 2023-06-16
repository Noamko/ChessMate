import serial
import time
import commands

class BoardRequest:
    @staticmethod
    def create(command, args) -> bytes:
        return bytes([command, len(args)] + args)

class BoardResponse:
    def __init__(self, data):
        self.id = data[0]
        self.args_len = data[1:5]
        self.args = data[5:]

class BoardMessage:
    @staticmethod
    def create(command, args) -> bytes:
        return bytes([command, len(args)] + args)

class SerialCommunication:
    def __init__(self, port, baudrate):
        self.serial = serial.Serial(port, baudrate)
        time.sleep(3) # wait for the board to boot
    def send(self, data):
        self.serial.write(data)
    def read(self, count) -> bytes:
        return self.serial.read(count)
