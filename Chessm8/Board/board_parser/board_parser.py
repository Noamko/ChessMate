from parsing_utils import convert_bit_to_location, position_to_int
# h1 is 1 and a8 is 9223372036854775808
CASTLING_DOWN_RIGHT = 15
CASTLING_DOWN_LEFT = 232
CASTLING_UP_LEFT = 16717361816799281152
CASTLING_UP_RIGHT = 1080863910568919040
def int_to_binary(num):
    return '{0:064b}'.format(num)

def fen_to_board(fen):
    board = [[0] * 8 for _ in range(8)]
    rows = fen.split('/')[::-1]
    col = 0
    row = 0
    for c in rows[0]:
        if c.isdigit():
            col += int(c)
        else:
            board[row][col] = 1
            return board

def count_changed_bits(num1, num2):
    xor_result = num1 ^ num2
    count = 0

    while xor_result:
        count += xor_result & 1
        xor_result >>= 1

    return count

def count_set_bits(num):
    binary_string = bin(num)[2:]  # Convert to binary and remove '0b' prefix
    count = binary_string.count('1')
    return count



class MoveCalculator:
    # Start board number 18446462598732906495
    def __init__(self, start_board=18446462598732906495, num_of_pieces=32):
        self.board = start_board
        self.num_of_pieces = num_of_pieces

    # TODO - take care of upgrade situation.
    def my_turn(self,current_board ,last_move, turn):
        # Check the number of changes on board.
        num_of_changes = count_changed_bits(current_board, self.board)

        
        # piece has taken
        if num_of_changes == 1:
            return self.piece_eating(current_board,last_move)

        # piece move without taking another piece.
        elif num_of_changes == 2:
            return self.move_without_eating(current_board=current_board)
        # Em pason
        elif num_of_changes == 3:
            pass
        # Castling
        elif num_of_changes == 4:
            return self.castling(current_board)

        raise Exception("Invalid move")

    def set_board(self, board):
        self.board = board
    # TODO - fix the big castling
    def castling(self, current_board):
        changed_position = current_board ^ self.board

        if changed_position == CASTLING_DOWN_RIGHT:
            return "e1g1"
        if changed_position == CASTLING_DOWN_LEFT:
            return "down_left"
        if changed_position == CASTLING_UP_LEFT:
            return "up_left"
        if changed_position == CASTLING_UP_RIGHT:
            return "up_right"
        raise Exception('Invalid move')
    
    def en_passant(self, current_board):
        pass
    # When eating the last board is without the piece that been eaten and the the piece that move
    def piece_eating(self, current_board, last_move):
        move = ''
        changed_position = current_board ^ self.board
        move_from = changed_position & self.board
        move += convert_bit_to_location(move_from)
        from_to = last_move ^ self.board
        move_to = from_to & current_board
        move += convert_bit_to_location(move_to)
        return move

    def move_without_eating(self, current_board):
        move = ''
        changed_position = current_board ^ self.board
        move_from = changed_position & self.board
        move += convert_bit_to_location(move_from)
        move_to = changed_position & current_board
        move += convert_bit_to_location(move_to)
        return move
    # return number that light just the pieces that changed.
    def your_turn(self, uci):
        pos1 = position_to_int(uci[:2])
        pos2 = position_to_int(uci[2:])
        return pos1 + pos2