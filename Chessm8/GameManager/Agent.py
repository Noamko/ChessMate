
import stockfish
import chess

class ChessAgent:
    def __init__(self, callbacks = []):
        self.callbacks = callbacks
    def do_move(self, board, callbacks):
        pass

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
    def __init__(self, depth, level, callbacks = []):
        super.__init__(callbacks)
        self.engine = stockfish.Stockfish()
        self.engine.set_depth(depth)
        self.engine.set_skill_level(level)

    def do_move(self, board):
        # Print the updated board
        # Get the engine's move
        self.engine.set_fen_position(board.fen())
        move = self.engine.get_best_move()

        print("Engine move: {}".format(move))
        # Make the move on the board
        if move is not None:
            board.push_uci(move)
            for callback in self.callbacks:
                callback(move)

class SerialAgent(ChessAgent):
    def __init__(self, serial_port, callbacks = []):
        super.__init__(callbacks)
        self.port = serial_port
    def do_move(self, board):
        move = get_move_callback()
        board.push_uci(move)
        for callback in self.callbacks:
            callback(move)

        
        
      
                
