# create a grpc client
import unittest
import sys
import os
sys.path.append(f"{os.getcwd()}/Chessm8/Board")
import time
import Board
from Board import Commands

class TestBoard(unittest.TestCase):
    def setUp(self):
        # print(f"{os.getcwd()}/Board")
        self.board_com = Board.SerialCommunication("/dev/tty.usbserial-10", 115200)
    
    def test_board_communication(self):
        print("Seding ping")
        # create a ping message
        command = Commands.PING_REQUEST
        args = []
        message = Board.BoardMessage.create(command=command, args=args)
        self.board_com.send(message)

        print("Waiting for response")
        response = int.from_bytes(self.board_com.read(1))
        print(f"Got response: {response}")
        self.assertEqual(response, Commands.PING_RESPONSE)

    def test_get_board_state(self):
        command = Commands.GET_BOARD_STATE_REQUEST
        args = []
        message = Board.BoardMessage.create(command=command, args=args)
        self.board_com.send(message)

        print("Waiting for response")
        id = int.from_bytes(self.board_com.read(1))
        print(f"Got id: {id}")
        len_data = self.board_com.read(4)
        args_len = int.from_bytes(len_data, byteorder='little')
        print(f"Got args_len: {args_len}")
        args = self.board_com.read(8 * args_len)
        state = int.from_bytes(args, byteorder='little')
        self.assertEqual(id, Commands.GET_BOARD_STATE_RESPONSE)
        self.assertEqual(args_len, 1)
    
    def test_leds(self):
        command = Board.commands.SET_LEDS_STATE_REQUEST
        args = [0xff]
        message = Board.BoardMessage.create(command=command, args=args)
        self.board_com.send(message)

        print("Waiting for response")

        # response = int.from_bytes(self.board_com.read(1))
        # print("turn off leds")
        # self.board_com.send(bytes([0x1]))


if __name__ == '__main__':
    unittest.main()