
import threading
import time
import stockfish
import chess
import os
import sys
from Agent import ChessAgent, SerialAgent

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
    
    def get_current_game(self):
        return self.current_game
    
    def delete_game(self):
        self.current_game = None
        self.current_game_thread = None

class Game:
    def __init__(self, white_agent: SerialAgent, black_agent: ChessAgent):
        self.white_agent = white_agent
        self.black_agent = black_agent
        self.board = chess.Board()
        self.board.apply_mirror()
        self.abort_flag = False
        self.resign_flag = False
        
    def getFEN(self):
        return self.board.fen()

    def start(self):
        # start the game
        while not self.board.is_game_over() or self.abort_flag or resign_flag():
            self.white_agent.do_move(self.board)
            print(self.board)
            self.black_agent.do_move(self.board)
            print(self.board)
            # Print the updated board
        if self.abort_flag:
            print("Game aborted")
            return

        elif self.resign_flag:
            print("Game resigned")
            return
        # Game is over
        result = self.board.result()
        print("Game over. Result: {}".format(result))
        return result
    
    def abort(self):
        self.abort_flag = True
    
    def resign(self):
        self.abort_flag = True
                    




