import parsing_utils



# fen  = '8/8/8/8/8/8/7p/8 b - - 0 1'
# num_board = parsing_utils.fen_to_int_board(fen)
# print(num_board)

board = parsing_utils.int64_to_binary_board(18014398509481984)
parsing_utils.print_chess_board(board)

# board = 4096  # Represents a1
# location = parsing_utils.convert_bit_to_location(board)
# print(location)  # Output: a1

