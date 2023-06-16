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
    
    def test_challenge_ai(self):
        lich = lichess()
        game = lich.challenge_ai()
        self.assertNotEqual(game["id"], "")
        cancel = lich.cancel_challenge(game["id"])
        self.assertTrue(cancel)

    def test_game_state(self):
        lich = lichess()
        game = lich.challenge_ai()
        self.assertNotEqual(game['id'] , "")
        board = Board()
        stream = board.game_state(game["id"])
        self.assertNotEqual(next(stream) , "")
        self.assertEqual(board.resign_game(game["id"]) , True)

    def test_get_current_challenges(self):
        lich = lichess()
        challenges = lich.get_current_challenges()
        self.assertNotEqual(challenges , '')

    def test_cancel_challenge(self):
        lich = lichess()
        game = lich.challenge_ai()
        self.assertNotEqual(game['id'] , "")
        cancel = lich.cancel_challenge(game['id'])
        self.assertEqual(cancel , True)

    def test_create_challenge(self):
        lich = lichess()
        challenge = lich.create_challenge('nir_assistent')
        self.assertIsNotNone(challenge)

if __name__ == '__main__':
    unittest.main()
    