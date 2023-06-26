
import threading
import time
import stockfish
import chess
import os
import sys
sys.path.append(f"{os.getcwd()}/cm_server/GameManager")
from GameManager import Agent
from Agent import SerialAgent, ChessAgent

class GameManager:
    def __init__(self):
        self.current_game = None
        self.current_game_thread = None
        self.rpc_thread = None
        self.board = chess.Board()

    def create_game(self,white_agent, black_agent):
        # create the game
        self.current_game = Game(white_agent, black_agent)
        self.current_game_thread = threading.Thread(target=self.current_game.start)
        self.current_game_thread.start()
        return self.current_game

class Game:
    def __init__(self, white_agent: SerialAgent, black_agent: ChessAgent):
        self.white_agent = white_agent
        self.black_agent = black_agent
        
    def start(self):
        # start the game
        board = chess.Board()
        while not board.is_game_over():
            self.white_agent.do_move(board)
            print(board)
            self.black_agent.do_move(board)
            print(board)
            # Print the updated board

        # Game is over
        result = board.result()
        print("Game over. Result: {}".format(result))
        return result
                    




