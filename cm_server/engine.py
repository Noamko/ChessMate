import threading
import datetime
import time
import sys
import os
sys.path.append(f"{os.getcwd()}/Chessm8/build/proto")
sys.path.append(f"{os.getcwd()}/Chessm8/Board")
from concurrent import futures
import grpc
from message_pb2 import CommandRequest, CommandResponse, CommandError
import message_pb2_grpc
from GameManager import GameManager
from GameManager import Agent
import Board
from Board import Commands

class CMEngine(message_pb2_grpc.CommandServicer):
    def __init__(self):
        self.game_manager = GameManager.GameManager()
    
        # init board
        self.board_com = Board.SerialCommunication()
        self.board_notification_observer_thread = threading.Thread(target=self.serialHandler)

        # self.board_com.send(Board.BoardRequest.create(command=Commands.PING_REQUEST, args=[]))
        self.board_notification_observer_thread.start()
        self.state_observers = []

    def Execute(self, request, context):
        response = CommandResponse()
        # get the oneof field
        command = request.WhichOneof("command")
        if command == "challengeAI":
            if self.current_game is not None:
                res.error.msg = "Already in a game"
                return response
            else:
                # create a new game
                level = request.challengeAI.level
                color = request.challengeAI.color

                stockfish_agent = Agent.StockfishAgent(10, level)
                # serial_agent = Agent.SerialAgent(lambda: parser.get_move())
                termianl_agent = Agent.TerminalAgent()
                
                
                if color == "white":
                    self.current_game = self.game_manager.create_game(stockfish_agent, serial_agent)
                else:
                    self.current_game = self.game_manager.create_game(serial_agent, stockfish_agent)

                # wait for board state

                self.current_game_thread = threading.Thread(target=self.current_game.start)
                self.current_game_thread.start()
                return response
       
        response.error.msg = "No such command"
        return response

    def waitForBoard(self):
        pass

    def serialHandler(self):
        while True:
            id = int.from_bytes(self.board_com.read(1))
            if id == Commands.BOARD_STATE_CHANGED:
                # get the board state
                data_len_bytes = self.board_com.read(4)
                data_len = int.from_bytes(data_len_bytes, byteorder='little')
                data_bytes = self.board_com.read(data_len)
                state = int.from_bytes(data_bytes, byteorder='little')

                for observer in self.state_observers:
                    observer.notify(state)
                print(f"Board state changed to {state}")
            elif id == Commands.PING_RESPONSE:
                print("Ping response")
            elif id == Commands.LOG_MESSAGE:
                # get the message
                data_len_bytes = self.board_com.read(4)
                data_len = int.from_bytes(data_len_bytes, byteorder='little')
                data_bytes = self.board_com.read(data_len)
                message = data_bytes.decode("utf-8")
                print(f"{datetime.datetime.now()} board: {message}")

    def start(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        message_pb2_grpc.add_CommandServicer_to_server(self, server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()
