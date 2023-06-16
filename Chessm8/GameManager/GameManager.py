
import threading
import time
import stockfish
import chess

class GameManager:
    def __init__(self):
        self.current_game = None
        self.current_game_thread = None
        self.rpc_thread = None
        self.board = chess.Board()


    def create_game(self, level, color, black_timer, white_timer):
        # create the game
        ai_agent = stockfish_agent(level=level)
        serial_agent = serial_agent()
        self.current_game = game(level, color, black_timer, white_timer)
        self.current_game_thread = threading.Thread(target=self.current_game.start)
        self.current_game_thread.start()

class Game:
    def __init__(self, level, black_timer, white_timer):
        self.level = level
        self.black_timer = black_timer
        self.white_timer = white_timer
        self.board = None
        self.stockfish = stockfish.Stockfish()
    
    def start(self) -> GameResult:
        # start the game   
        self.board = chess.Board()
        self.stockfish.set_fen_position(self.board.fen())
        board = chess.Board()
        while not board.is_game_over():
            # Get the player's move
            move = input("Enter your move: ")

            # Attempt to push the move to the board
            try:
                board.push_san(move)
            except ValueError:
                print("Invalid move, try again.")
                continue

            # Print the updated board
            print(board)

        # Game is over
        result = board.result()
        print("Game over. Result: {}".format(result))
                    




