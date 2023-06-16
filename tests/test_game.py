# create a grpc client
import unittest
import sys
import os
sys.path.append(f"{os.getcwd()}/Chessm8/GameManager")
import time
from GameManager import GameManager
from Agent import StockfishAgent
import chess

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.manger = GameManager()
    def test_auto_game(self):
        stockfishAgentWhite = StockfishAgent(1, 1000)
        stockfishAgentBlack = StockfishAgent(1, 1000)
        game_thread = self.manger.create_game(stockfishAgentWhite, stockfishAgentBlack)
        game_thread.start()


if __name__ == '__main__':
    unittest.main()