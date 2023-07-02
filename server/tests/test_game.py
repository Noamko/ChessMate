import unittest
import sys
import os
# os.chdir("/Users/noamk/projects/ChessMate")

sys.path.append(f"{os.getcwd()}/server/src")
# sys.path.append(f"../GameManager")
# import GameManager
# import StockfishAgent
# import Board.Board
# import CMGame.Managment




class TestBoard(unittest.TestCase):
    def setUp(self):
        print(os.getcwd())
        self.manger = GameManager.GameManager()
        
    def test_auto_game(self):
        stockfishAgentWhite = StockfishAgent(10, 1000)
        stockfishAgentBlack = StockfishAgent(10, 1000)
        game_thread = self.manger.create_game(stockfishAgentWhite, stockfishAgentBlack)
        game_thread.start()
        game_thread.join()
    

if __name__ == '__main__':
    unittest.main()