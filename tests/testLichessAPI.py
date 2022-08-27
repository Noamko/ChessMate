import unittest

from lichess import lichess
class TestLichess(unittest.TestCase):
    
    def test_challange_ai(self):
        lich = lichess()
        game = lich.challange_ai()
        self.assertNotEqual(game["id"], "")
        cancel = lich.cancel_challenge(game["id"])
        self.assertTrue(cancel)