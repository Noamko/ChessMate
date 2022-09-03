import unittest
from lichess import lichess, LichessAcccount, Board
class TestLichessAPI(unittest.TestCase):
    # Account information tests
    def test_get_email(self):
        lichess = LichessAcccount()
        email = lichess.getEmail()
        self.assertNotEqual(email, "")
    
    def test_get_account(self):
        lichess = lichess()
        account = lichess.get_account()
        self.assertNotEqual(account, "")
    
    def test_challange_ai(self):
        lich = lichess()
        game = lich.challange_ai()
        self.assertNotEqual(game["id"], "")
        cancel = lich.cancel_challenge(game["id"])
        self.assertTrue(cancel)
    def test_blah(self):
        self.assertTrue(True)