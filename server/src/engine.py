import os
import sys
sys.path.append(f"{os.getcwd()}/server/build/proto")
from message_pb2 import CommandRequest, CommandResponse, CommandError
from Managment import GameManager
from concurrent import futures
from Board import BoardControl
import Agent
import message_pb2_grpc
import StateObserver
from StateObserver import PieceToLedStateObserver, WaitForStateObserver
import threading
import grpc
import time
from queue import Queue
import board_parser
import translator
import parsing_utils

class OpponentLedSetObserver():
    def __init__(self, board_ctl):
        self.board_ctl = board_ctl
    def notify_move(self, move):
        leds_to_lit = translator.uci_to_board(move)
        self.board_ctl.setLedsState(leds_to_lit)

class CMEngine(message_pb2_grpc.CommandServicer):
    def __init__(self):
        self.game_manager = GameManager()
        self.board_ctl = BoardControl() # Board communication
        self.move_queue = Queue()
        self.end_turn_observers = []

        # observer = PieceToLedStateObserver(self.board_ctl)
        # self.board_ctl.registerStateObserver(observer)

    def start(self):
        # initialize board
        self.board_ctl.initialize()

         # start grpc server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        message_pb2_grpc.add_CommandServicer_to_server(self, server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination() # blocking
        
    
    def Execute(self, request, context):
        response = CommandResponse()
        # get the oneof field
        command = request.WhichOneof("command")

        '''Command Handler
            > dispatch the command to the appropriate handler
            > return the response
            > if the command is not recognized, return an error
            > if the command is recognized but the arguments are invalid, return an error
        '''

        if command == "challengeAI":
            if self.game_manager.current_game  is not None:
                res.error.msg = "Already in a game"
                return response
            else:
                # create a new game
                level: int = request.challengeAI.level
                color = request.challengeAI.color

                stockfish_agent = Agent.StockfishAgent(10, level)
                stockfish_move_observer = OpponentLedSetObserver(self.board_ctl)
                stockfish_agent.registerMoveObserver(stockfish_move_observer)

                serialAgent = Agent.SerialAgent()
                self.board_ctl.registerStateObserver(serialAgent)
                self.end_turn_observers.append(serialAgent)

                # waitforstate = WaitForStateObserver(128)
                # self.board_ctl.registerStateObserver(waitforstate) 
                # waitforstate.wait() # wait for the board to be ready
                print("Board is ready")

                if color == 0:
                    self.game_manager.create_game(serialAgent, stockfish_agent)
                else:
                    self.game_manager.create_game(stockfish_agent, serialAgent)
                return response
        elif command == "challengeHuman":
            pass

        elif command == "endTurn":
            for observer in self.end_turn_observers:
                observer.notify_end_turn()
            time.sleep(5)
            # get the desired state
            current_fen = self.game_manager.get_current_game().getFEN()
            print(current_fen)
            new_state = parsing_utils.fen_to_int_board(current_fen)
            print("required state:")
            print_state_as_matrix(translator.col_to_row(new_state))
            waitforsate = WaitForStateObserver(translator.col_to_row(new_state))
            self.board_ctl.registerStateObserver(waitforsate)
            waitforsate.wait()
            print("wait for board release")
            self.board_ctl.setLedsState(0)
            return response

        elif command == "getBoardState":
            response.getBoardState.state = 0xffff00000000ffff
            return response
            print("getBoardState")
        response.error.msg = "No such command"
        return response



def print_state_as_matrix(state):
    binary_string = bin(state)[2:].zfill(64)
    # Split the binary string into rows of 8 characters
    rows = [binary_string[i:i+8] for i in range(0, 64, 8)]
    # Create the matrix by splitting each row into a list of integers
    print('#'*20)
    for row in rows:
        print('  '.join(row))
    print('#'*20)