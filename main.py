import lichess
import json

lich = lichess.lichess()
game_info = lich.challange_ai()
board = lichess.Board(game_info['id'])
game_state = board.game_state()
board.resign_game()
print(game_state)
