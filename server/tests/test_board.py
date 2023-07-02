# create a grpc client
import unittest
import time
import sys
import os
sys.path.append(f"{os.getcwd()}/server/src")

print(sys.path)

import Agent
# from Board import Commands
import serial.tools.list_ports
class TestBoard(unittest.TestCase):
    def setUp(self):
        # print(f"{os.getcwd()}/Board")
        self.board_com = None
        for port in serial.tools.list_ports.comports():
            print(f"port:::: {port.device}, {port.name}, {port.description}, {port.hwid}, {port.vid}, {port.pid}")
            if port.pid != None:
                self.board_com = Board.SerialCommunication()
                break
        if self.board_com is None:
            raise Exception("No board found")
    
    def test_board_communication(self):
        print("Seding ping")
        # create a ping message
        command = Commands.PING_REQUEST
        args = [0]
       
        self.board_com.send(bytes([command]) + bytes(args))

        print("Waiting for response")
        response = int.from_bytes(self.board_com.read(1), byteorder='little')
        print(f"Got response: {response}")
        self.assertEqual(response, Commands.PING_RESPONSE)

    def test_get_board_state(self):
        command = Commands.GET_BOARD_STATE_REQUEST
        args = [0]
        message = Board.BoardRequest.create(command=command, args=args)
        self.board_com.send(message)

        print("Waiting for response")
        id = int.from_bytes(self.board_com.read(1), byteorder='little')
        print(f"Got id: {id}")
        len_data = self.board_com.read(4)
        args_len = int.from_bytes(len_data, byteorder='little')
        print(f"Got args_len: {args_len}")
        args = self.board_com.read(8 * args_len)
        state = int.from_bytes(args, byteorder='little')
        self.assertEqual(id, Commands.GET_BOARD_STATE_RESPONSE)
        self.assertEqual(args_len, 1)
    
    def test_leds(self):
        command = Board.Commands.SET_LEDS_STATE_REQUEST
        args = [0xff, 0xff, 0x0, 0x0, 0x0, 0x0 ,0x0 ,0x0]
        message = Board.BoardRequest.create(command=command, data=args)
        self.board_com.send(message)

        print("Waiting for response")

        response = int.from_bytes(self.board_com.read(1), byteorder='little')
        print(f"Got response: {response}")
        self.assertEqual(response, Board.Commands.SET_LEDS_STATE_RESPONSE)


if __name__ == '__main__':
    unittest.main()
