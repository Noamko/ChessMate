from mimetypes import init
from urllib import request
from lichess import lichess , Board 
import requests
lich = lichess()
x = lich.create_challenge('nir_assistent')
print(x)

class lichessBoard:
    def send_move(self, move):
        # liches api shit
        pass
class StockfishBoard:
    def send_move(self, move):
        # stockfish api
        pass

class board():
    # send move
    # get board state
    # print board
    def send_move(self, move):
        pass
    def get_board_state(self) -> state:
        pass
    def print_board(self):
        exmaple = """
        r . b q k b . r
        p p p p . Q p p
        . . n . . n . .
        . . . . p . . .
        . . B . P . . .
        . . . . . . . .
        P P P P . P P P
        R N B . K . N R
        """
        pass
    pass
class game:
    init(board)
    def new_game(self, board):
        pass
    pass

class server:
    # connect to android app (later)
    # open menu: (new game, settings):
        # new game: (local(stockfish), online(lichess))
            # stockfish: (level) -> start game
            # lichess -> connect to lichess -> (search for game) -> start game
    # engine:
        # 1.  
        # 2. 


    def __init__(self) -> None:
        pass
    def start(self):
        pass



