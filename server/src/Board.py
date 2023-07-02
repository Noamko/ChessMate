import serial
import time
import threading
import datetime
import serial.tools.list_ports


import os
import sys
from  board_parser import MoveCalculator

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
        self.state_observers_callbacks = []
        self.board_serial_listener_thread = threading.Thread(target=self.serialHandler)
        self.last_two_states = [0, 0]
        
    def registerStateObserver(self, observer):
        self.state_observers.append(observer)
    def registerStateCallback(self, callback):
        self.state_observers_callbacks.append(callback)
    
    def unregisterStateObserver(self, observer):
        self.state_observers.remove(observer)
    def unregisterStateCallback(self, callback):
        self.state_observers_callbacks.remove(callback)
    
    def initialize(self):
        self.board_com = SerialCommunication()
        self.board_serial_listener_thread.start()
    
    def sendMessage(self, message: bytes):
        self.board_com.send(message)
    
    def setLedsState(self, state: int, colors: [int] = []):
        led_state = 0
        for i in range(0, 8):
            b = state >> i * 8 & 0xFF
            if i % 2 != 0:
                # reverse the bits
                b = int('{:08b}'.format(b)[::-1], 2)
            led_state |= b << i * 8
        command = Commands.SET_LEDS_STATE_REQUEST
        command = command.to_bytes(1, "little")
        data_len = 8
        data_len = data_len.to_bytes(4, "little")
        data = led_state.to_bytes(8, "big")
        self.board_com.send(command + data_len + data)
    
    def getBoardState(self):
        return self.last_two_states[1]
      
    def serialHandler(self):
        while True:
            id = int.from_bytes(self.board_com.read(1)) # blocking
            if id == Commands.BOARD_STATE_CHANGED:
                # get the board state
                data_len_bytes = self.board_com.read(4)
                data_len = int.from_bytes(data_len_bytes, byteorder='little')
                data_bytes = self.board_com.read(data_len)
                state = int.from_bytes(data_bytes, byteorder='little')

                ### patch to fix 2 broken cells
                state = state | 0x200000001 
                ### end of patch

                self.last_two_states[0] = self.last_two_states[1]
                self.last_two_states[1] = state

                for observer in self.state_observers:
                    observer.notify_state_changed(state)
                for callback in self.state_observers_callbacks:
                    callback(state)

                print(f"board state changed: {format(state, '064b')} ({state})")
            
            elif id == Commands.GET_BOARD_STATE_RESPONSE:
                # get the board state
                data_len_bytes = self.board_com.read(4)
                data_len = int.from_bytes(data_len_bytes, byteorder='little')
                data_bytes = self.board_com.read(data_len)
                state = int.from_bytes(data_bytes, byteorder='little')
                print(f"board state: {format(state, '064b')} ({state})")
                
            elif id == Commands.PING_RESPONSE:
                print("Ping response")
            elif id == Commands.LOG_MESSAGE:
                # get the message
                data_len_bytes = self.board_com.read(4)
                data_len = int.from_bytes(data_len_bytes, byteorder='little')
                data_bytes = self.board_com.read(data_len)
                message = data_bytes.decode("utf-8")
                print(f"{datetime.datetime.now()} board: {message}")