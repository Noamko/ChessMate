import threading
import time
import sys
import os
sys.path.append("build/proto")
from concurrent import futures
import grpc
from message_pb2 import CommandRequest, CommandResponse, CommandError
import message_pb2_grpc

class CMEngine(message_pb2_grpc.CommandServicer):
    def __init__(self):
        self.current_game = None
        self.current_game_thread = None
        self.rpc_thread = None
    
    def Execute(self, request, context):
        response = CommandResponse()
        # get the oneof field
        command = request.WhichOneof("command")
        if command == "challengeAI":
            if self.current_game is not None:
                res.error.msg = "Already in a game"
                return response
            else:
                level = request.challengeAI.level
                color = request.challengeAI.color
                black_timer = request.challengeAI.black_timer
                white_timer = request.challengeAI.white_timer
                ai_agent = stockfish_agent(level=level)
                serial_agent = serial_agent()

                waitForBoard()

                self.current_game = game(level, color, black_timer, white_timer)
                self.current_game_thread = threading.Thread(target=self.current_game.start)
                self.current_game_thread.start()
                return response
       
        response.error.msg = "No such command"
        return response

    def start(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        message_pb2_grpc.add_CommandServicer_to_server(self, server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()
