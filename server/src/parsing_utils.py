# Get int with just one bit turn on and return the location
def convert_bit_to_square(board):
    for i in range(64):
        if board & (1 << i):
            file = i % 8
            rank = (i // 8)
            return chr(ord('h') - file) + str(rank + 1)
        

def print_chess_board(board):
    for row in board:
        print(' '.join(str(cell) for cell in row))

def int64_to_binary_board(num):
    chessboard = [[0 for _ in range(8)] for _ in range(8)]
    for i in range(64):
        if (num & (1 << (63 - i))) != 0:
            row = i // 8
            col = i % 8
            chessboard[row][col] = 1
    return chessboard

def fen_to_int_board(fen):
    int_board = 0
    fen_parts = fen.split()

    # The FEN string represents the board state using ranks separated by '/'
    ranks = fen_parts[0].split('/')

    for rank_index, rank in enumerate(ranks):
        file_index = 0
        for char in rank:
            if char.isdigit():
                file_index += int(char)
            else:
                piece_bit = 63 - (8 * rank_index + file_index)
                int_board |= 1 << piece_bit
                file_index += 1

    return int_board
def position_to_int(pos):
    num = 1
    num <<= 8 * (int(pos[1]) - 1) + ord('h') - ord(pos[0])
    return num

def row_major_to_position(board):
    index = 0
    for i in range(8):
        if board >> (i + 1) * 8 == 0:
            index = i
            break
    file = 0
    for i in range(8):
        if board >> (i + 1) + (index * 8) == 0:
            file = i
            break
    return chr(ord('h') - file) + str(index + 1) 

def row_to_col(board):
    new_board = 0
    for i in range(64):
        if (1 << i) & board == 1 << i:
            pos = row_major_to_position((1 << i) & board)
            new_board += position_to_int_col_major(pos)
    return new_board

def position_to_int_col_major(pos):
    num = 1
    num <<= ((ord('h') - ord(pos[0])) * 8) + 8 - int(pos[1]) 
    return num

