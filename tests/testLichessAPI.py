import unittest
from lichess import blinchess, LichessAccount, Board
class TestLichessAPI(unittest.TestCase):
    # Account information tests
    def test_get_email(self):
        lichess = LichessAccount()
        email = lichess.getEmail()
        self.assertNotEqual(email, "")
    
    def test_get_my_account(self):
        lichess = LichessAccount()
        account = lichess.get_my_account()
        self.assertNotEqual(account, "")
    
    def test_challange_ai(self):
        lich = blinchess()
        game = lich.challange_ai()
        self.assertNotEqual(game["id"], "")
        cancel = lich.cancel_challenge(game["id"])
        self.assertTrue(cancel)

    def test_make_move(self):
        lich = blinchess()
        game = lich.challange_ai()
        board = Board(game['id'])
        self.assertTrue(board.make_move('e2e4'))
        cancel = lich.cancel_challenge(game["id"])
        self.assertTrue(cancel)

    