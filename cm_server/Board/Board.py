import serial
import time
import threading
import serial.tools.list_ports

class Commands:
    PING_REQUEST = 0xA0
    PING_RESPONSE = 0xA1
    BOARD_STATE_CHANGED = 0xAA
    GET_BOARD_STATE_REQUEST = 0xA2
    GET_BOARD_STATE_RESPONSE = 0xA3
    SET_LEDS_STATE_REQUEST = 0xA4
    SET_LEDS_STATE_RESPONSE = 0xA5
    LOG_MESSAGE = 0xA8

class BoardRequest:
    @staticmethod
    def create(command, data) -> bytes:
        return command.to_bytes() + len(data).to_bytes(4,"little") + bytes(data)

class BoardResponse:
    def __init__(self, data):
        self.id = data[0]
        self.args_len = data[1:5]
        self.args = data[5:]

class SerialCommunication:
    def __init__(self):
        # detect the port
        port = None
        for p in serial.tools.list_ports.comports():
            print(p.description)
            if p.pid != None:
                port = p.device
                break
        if port == None:
            raise "Failed to find serial port"
        self.serial = serial.Serial(port, 115200)
        time.sleep(3) # wait for the board to boot
    def send(self, data):
        self.serial.write(data)
    def read(self, count) -> bytes:
        return self.serial.read(count)

class BoardControl:
    def __init__(self):
        self.board_com = None
        self.state_observers = []
        self.board_serial_listener_thread = threading.Thread(target=self.serialHandler)
    def registerStateObserver(self, observer):
        self.state_observers.append(observer)
    
    def initialize(self):
        self.board_com = SerialCommunication()
        self.board_serial_listener_thread.start()
    
    def sendMessage(self, message: bytes):
        self.board_com.send(message)

    def serialHandler(self):
        while True:
            id = int.from_bytes(self.board_com.read(1)) # blocking
            if id == Board.Commands.BOARD_STATE_CHANGED:
                # get the board state
                data_len_bytes = self.board_com.read(4)
                data_len = int.from_bytes(data_len_bytes, byteorder='little')
                data_bytes = self.board_com.read(data_len)
                state = int.from_bytes(data_bytes, byteorder='little')
                for observer in self.state_observers:
                    observer.notify(state)
                print(f"Board state changed to {format(state, '064b')}")
            elif id == Board.Commands.PING_RESPONSE:
                print("Ping response")
            elif id == Board.Commands.LOG_MESSAGE:
                # get the message
                data_len_bytes = self.board_com.read(4)
                data_len = int.from_bytes(data_len_bytes, byteorder='little')
                data_bytes = self.board_com.read(data_len)
                message = data_bytes.decode("utf-8")
                print(f"{datetime.datetime.now()} board: {message}")