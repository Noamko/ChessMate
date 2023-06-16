# create a grpc client
import unittest
import sys
import os
sys.path.append(f"{os.getcwd()}/Chessm8/Board")
# print(f"{os.getcwd()}/Boarasdasdadsad")
# sys.path.append("../Board")
import time
import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        # print(f"{os.getcwd()}/Board")
        self.board_com = Board.BoardCommunication()
    def test_leds(self):
        print("turn on leds")
        self.board_com.send(bytes([0x0]))
        time.sleep(1)
        print("turn off leds")
        self.board_com.send(bytes([0x1]))


if __name__ == '__main__':
    unittest.main()