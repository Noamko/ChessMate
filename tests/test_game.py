# create a grpc client
import unittest
import sys
import os
sys.path.append(f"{os.getcwd()}/Chessm8/GameManager")
import time
from GameManager import GameManager
from Agent import StockfishAgent, SerialAgent
import chess

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.manger = GameManager()
    def test_auto_game(self):
        stockfishAgentWhite = StockfishAgent(10, 1000)
        stockfishAgentBlack = StockfishAgent(10, 1000)
        game_thread = self.manger.create_game(stockfishAgentWhite, stockfishAgentBlack)
        game_thread.start()
        game_thread.join()
    
    def test_agent_notifiers(self):
        stockfishAgent = StockfishAgent(10, 1000)
        serialAgent = SerialAgent()

        pass

if __name__ == '__main__':
    unittest.main()