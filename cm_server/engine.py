import os
import sys
sys.path.append(f"{os.getcwd()}/cm_server/build/proto")
sys.path.append(f"{os.getcwd()}/cm_server/Board")
from message_pb2 import CommandRequest, CommandResponse, CommandError
from GameManager import GameManager
from StateObserver import WaitForStateObserver
from concurrent import futures
from Board import BoardControl
from GameManager import Agent
import message_pb2_grpc
import StateObserver
import threading
import grpc
import time
from queue import Queue

sys.path.append(f"{os.getcwd()}/cm_server/board_parser")
import board_parser
import translator



class CMEngine(message_pb2_grpc.CommandServicer):
    def __init__(self):
        self.game_manager = GameManager.GameManager()
        self.board_ctl = BoardControl() # Board communication
        self.move_queue = Queue()

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

        # challengeAI command
        #  > create a new game
        #  > wait for board state

        if command == "challengeAI":
            if self.game_manager.current_game  is not None:
                res.error.msg = "Already in a game"
                return response
            else:
                # create a new game
                level: int = request.challengeAI.level
                color = request.challengeAI.color

              
                # stockfish_agent2 = Agent.StockfishAgent(10, level)
                # serial_agent = Agent.SerialAgent(lambda: parser.get_move())
                # serial_agent = Agent.SerialAgent()
                stockfish_agent = Agent.StockfishAgent(10, level)
                serialAgent = Agent.SerialAgent(self.move_queue)
                # waitforstate = WaitForStateObserver(128) 
                # self.board_ctl.registerStateObserver(waitforstate) 
                # waitforstate.wait() # wait for the board to be ready
                print("Board is ready")


             
                if color == 0:
                    self.current_game = self.game_manager.create_game(serialAgent, stockfish_agent)
                else:
                    self.current_game = self.game_manager.create_game(stockfish_agent, serialAgent)
                return response

        elif command == "endTurn":
            # This section is executed after the user has ended his turn (aka pressed the clock on the app)
            print("beton")
            self.move_queue.put([self.board_ctl.last_two_states[0],self.board_ctl.last_two_states[1]])
            # self.current_game.white_agent.notify(self.board_ctl.last_two_states)
            # self.current_game.opponent_agent.register_callback(opponents_waiter.set) # Noam
            # self.current_game.user_agent.set_move(user_move) (this will release stockfish to make their move) # Noam
            # waiter.wait() # Noam
            # opponents_move = oponnetMove.move exmaple: a2c3 # Noam 
            
            # At this point we have the user move and the opponent moves as uci and the virtual board is already updated! nice!
            # Now we need to indicate the human to move the oponnent pieces on the board
            # we will do this by lighting up the squares that the oponnent moved from and to

            # opennent_move_from opponents_move[0:2] exmaple : opponents_move[0:2] = b2 # Noam
            # opennent_move_to opponents_move[2:4] exmaple : opponents_move[2:4] = c3 # Noam

            # from_square = parser.to_square(opennent_move_from) exmaple :  parser.to_square(a1) = 0x8000000000000000 # Nir
            # to_square = parser.to_square(opennent_move_to) # Nir
            
            # leds_to_lit =  from_square | to_square # Noam
            # self.board_ctl.setLedsState(leds_to_lit) # Noam

            # get the desired state
            # current_fen = self.current_game.board.fen() # Noam
            # new_state = parser.to_state(current_fen) # Nir

            # wait for state change
            # waitforstate = WaitForStateObserver(new_state) #Noam
            # self.board_ctl.registerStateObserver(waitforstate) #Noam
            # waitforstate.wait()

            # DONE! now we can return the response
            # return the response
            # response.endTurn.move = opponents_move
            return response

        elif command == "getBoardState":
            response.getBoardState.state = 0xffff00000000ffff
            return response
            print("getBoardState")
        response.error.msg = "No such command"
        return response
