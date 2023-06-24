import os
import sys
sys.path.append(f"{os.getcwd()}/cm_server/build/proto")
sys.path.append(f"{os.getcwd()}/cm_server/Board")
from message_pb2 import CommandRequest, CommandResponse, CommandError
from GameManager import GameManager
from StateObserver import WaitForStateObserver
from concurrent import futures
from Board import BoardControl
import message_pb2_grpc
import StateObserver
import threading
import grpc
import time



class CMEngine(message_pb2_grpc.CommandServicer):
    def __init__(self):
        self.game_manager = GameManager.GameManager()
       
        self.board_ctl = BoardControl() # Board communication

    def start(self):
         # start grpc server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        message_pb2_grpc.add_CommandServicer_to_server(self, server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()
        
        # self.board_ctl.initialize()
    
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

        # challengeAI command
        #  > create a new game
        #  > wait for board state

        if command == "challengeAI":
            if self.game_manager.current_game  is not None:
                res.error.msg = "Already in a game"
                return response
            else:
                # create a new game
                level = request.challengeAI.level
                color = request.challengeAI.color

                stockfish_agent = Agent.StockfishAgent(10, level)
                # serial_agent = Agent.SerialAgent(lambda: parser.get_move())
                serial_agent = Agent.SerialAgent()
                
                waitforstate = WaitForStateObserver(0xffff00000000ffff) 
                self.board_ctl.registerStateObserver(waitforstate) 
                waitforstate.wait() # wait for the board to be ready
                
                if color == "white":
                    self.current_game = self.game_manager.create_game(stockfish_agent, serial_agent)
                else:
                    self.current_game = self.game_manager.create_game(serial_agent, stockfish_agent)

                # wait for the game to finish
                return response
       
        elif command == "getBoardState":
            response.getBoardState.state = 0xffff00000000ffff
            return response
            print("getBoardState")
        response.error.msg = "No such command"
        return response
