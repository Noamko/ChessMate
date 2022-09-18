import unittest
from lichess import lichess, LichessAccount, Board

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
        lich = lichess()
        game = lich.challange_ai()
        self.assertNotEqual(game["id"], "")
        cancel = lich.cancel_challenge(game["id"])
        self.assertTrue(cancel)

    def test_make_move(self):
        lich = lichess()
        game = lich.challange_ai()
        board = Board(game['id'])
        if game['player'] != 'white':
            self.assertTrue(board.make_move('e2e4'))
        else:
            self.assertTrue(board.make_move('e7e6'))
        self.assertTrue(board.resign_game())

    # def test_fetch_game_state(self):
    #     lich = lichess()
    #     game = lich.challange_ai()
    #     board = Board(game['id'])
    #     board.make_move('e2e4')
    #     self.assertIsNotNone(board.fetch_game_state())
        
if __name__ == '__main__':
    unittest.main()
    