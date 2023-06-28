
import stockfish
import chess
import threading

import os
import sys
from board_parser import MoveCalculator
from StateObserver import  StateObserver
from queue import Queue
from translator import col_to_row

class ChessAgent:
    def __init__(self):
        self.move_observers = []
    def do_move(self, board):
        pass
    def registerMoveObserver(self, observer):
        self.move_observers.append(observer)

class TerminalAgent(ChessAgent):
    def do_move(self, board):
        # Print the updated board
        print(board)
        # Get the user's move
        while True:
            move = input("Enter your move in UCI format: ")
            # Make the move on the board
            try:
                board.push_uci(move)
                break
            except ValueError:
                print("Illegal move, try again")
                continue

class StockfishAgent(ChessAgent):
    def __init__(self, depth, level):
        self.engine = stockfish.Stockfish()
        self.engine.set_depth(depth)
        self.engine.set_skill_level(level)
        self.move_observers = []

    def do_move(self, board):
        # Print the updated board
        # Get the engine's move
        self.engine.set_fen_position(board.fen())
        move = self.engine.get_best_move()

        print("Engine move: {}".format(move))
        # Make the move on the board
        if move is not None:
            board.push_uci(move)
            for observer in self.move_observers:
                observer.notify_move(move)
           

class EndTurnObserver:
    def notify_end_turn(self):
        pass

class SerialAgent(ChessAgent, StateObserver, EndTurnObserver):
    def __init__(self):
        self.lock = threading.Lock()
        self.last_state = 0
        self.current_state = 0
        self.move_queue = Queue()
        self.move_calculator = MoveCalculator()
        self.last_move = None
    
    def notify_state_changed(self, state):
        self.last_state = self.current_state
        self.current_state = state
        print("xor state: {}".format(self.current_state ^ self.last_state))
        # if self.is_my_turn:
        #     # get hints
        #     # fen

    def notify_end_turn(self, new_state):
        self.move_calculator.set_board(col_to_row(new_state))
        self.last_move = self.move_calculator.my_turn(self.current_state ,self.last_state)
        if self.last_move is not None:
            self.move_queue.put(self.last_move)
            print("SerialAgent: {}".format(self.last_move))
            return True
        else:
            print("SerialAgent: Illegal move")
            return False

    def do_move(self, board):
        # wait for move
        move = self.move_queue.get()
        if board.is_legal(chess.Move.from_uci(move)):
            board.push_uci(move)
        else:
            print("Illegal move: {}".format(move))