import lichess
import json

lich = lichess.blinchess()
game_id = lich.challange_ai()['id']
lich.make_move(game_id=game_id , move='e2e4')
