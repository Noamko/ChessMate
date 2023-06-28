from board_parser import MoveCalculator
import parsing_utils
fen1 = 'rnbq1rk1/8/4b3/p2p2p1/1ppp4/p6p/PPPPP1PP/RNBQKBNR w KQq - 0 1'
fen2 = 'rnbq1Bk1/8/4b3/p2p2p1/1ppp4/p6p/PPPPP1PP/RNBQK1NR w KQq - 0 1'
middle_board = 'rnbq2k1/8/4b3/p2p2p1/1ppp4/p6p/PPPPP1PP/RNBQK1NR w KQq - 0 1'
b1 = parsing_utils.fen_to_int_board(fen1)
b2 = parsing_utils.fen_to_int_board(fen2)
b3 = parsing_utils.fen_to_int_board(middle_board)
mcalc = MoveCalculator(start_board=b1)

move_num = mcalc.your_turn('a1h8')
board = parsing_utils.int64_to_binary_board(move_num)
parsing_utils.print_chess_board(board)