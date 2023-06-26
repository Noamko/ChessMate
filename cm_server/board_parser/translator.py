from parsing_utils import position_to_int, print_chess_board, int64_to_binary_board

# Perpose, translate from col major to row major and from row major to col major.
# board is a number that represent a board with just one peice.
def cols_major_to_position(board):
    file = 0
    for i in range(8):
        if board >> (i + 1) * 8 == 0:
            file = i
            break
    index = 0
    for i in range(8):
        if board >> (i + 1) + (file * 8) == 0:
            index = i
            break
    return chr(ord('h') - file) + str(8 - index)

def col_to_row(board):
    new_board = 0
    for i in range(64):
        if (1 << i) & board == 1 << i:
            pos = cols_major_to_position((1 << i) & board)
            new_board += position_to_int(pos)
    return new_board

def uci_to_board(uci):
    pos1 = 1
    pos1 <<= (ord('h') - ord(uci[0])) * 8 +(8 - int(uci[1]))
    pos2 = 1
    pos2 <<= (ord('h') - ord(uci[2])) * 8 +(8 - int(uci[3]))
    return pos1 + pos2
