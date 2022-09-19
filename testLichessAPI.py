import unittest
from lichess import lichess, LichessAccount, Board

class TestLichessAPI(unittest.TestCase):
    
    def test_get_email(self):
        lichess = LichessAccount()
        email = lichess.getEmail()
        self.assertNotEqual(email, "")
    
    def test_get_my_account(self):
        lichess = LichessAccount()
        account = lichess.get_my_account()
        self.assertNotEqual(account, "")
    
    def test_challange_ai(self):
        lich = lichess()
        game = lich.challange_ai()
        self.assertNotEqual(game["id"], "")
        cancel = lich.cancel_challenge(game["id"])
        self.assertTrue(cancel)

    def test_game_state(self):
        lich = lichess()
        game = lich.challange_ai()
        self.assertNotEqual(game['id'] , "")
        board = Board(game["id"])
        stream = board.game_state()
        self.assertNotEqual(next(stream) , "")
        self.assertEqual(board.resign_game() , True)
    
        
if __name__ == '__main__':
    unittest.main()
    