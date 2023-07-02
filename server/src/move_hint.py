import chess


from board_parser.parsing_utils import convert_bit_to_square, position_to_int

def get_possible_moves(fen, square):
    board = chess.Board(fen)
    piece_moves = []

    # Generate all legal moves for the specific piece on the given square
    for move in board.legal_moves:
        if move.from_square == square:
            piece_moves.append(move.uci())
    return piece_moves

def get_square(curr_board, prev_board):
    xor_board = curr_board ^ prev_board
    position = convert_bit_to_square(xor_board)
    res =  chess.parse_square(position)
    return res
# Get the fen of prev board
def get_hints(fen, curr_board, prev_board):
    square = get_square(curr_board=curr_board, prev_board=prev_board)
    possible_moves = get_possible_moves(fen, square)
    res = 0
    for move in possible_moves:
        res |= position_to_int(move[2:])
    return res

