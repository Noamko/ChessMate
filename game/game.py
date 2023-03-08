import platform
import stockfish
sf = None

if platform.system() == "Darwin":
    sf = stockfish.Stockfish("/opt/homebrew/bin/stockfish")
elif platform.system() == "Linux":
    sf = stockfish.Stockfish("/usr/bin/stockfish")

class game:
    DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    def __init__(self, fen=DEFAULT_FEN):
        if sf.is_fen_valid(fen):
            self.fen = fen
        else:
            raise ValueError("Invalid FEN")
            
    def get_board_state(self):
        return sf.get_board_visual()
    
    def get_fen(self):
        return sf.get_fen_position()

    def get_evaluation(self):
        return sf.get_evaluation()

    def move(self, move):
        if sf.is_move_correct(move_value=move):
            sf.make_moves_from_current_position(moves=[move])
            return True
        else:
            return False
    