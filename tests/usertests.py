
# Epic 2 user story 2 tests
# As a player, I would like to play against players of my skill
def test_player_skill(board):
    # assert if the player's skill level is greater than or equal to the opponent's skill level times 1.5
    assert lichess.get_player_skill() >= board.get_opponent_skill() * 1.5


# Epic 3 user story 3 test
# As a User, I would like to be able to log in and logout of my account
def test_login_logout():
    # first log in with a dummy account that we created for this test and test if we are acctually logged in
    lichess.login("testuser", "testpassword")
    assert lichess.is_logged_in() == True
    assert lichess.get_username() == "testuser" # test if the username is correct
    # then log out and test if we are acctually logged out

    lichess.logout()
    assert lichess.is_logged_in() == False
    assert lichess.get_username() == None # test if the username is None after logging out

    
# Epic 1 user story 1 test
# As a player, I would like to be able to play against a computer
def test_play_computer():
    # create a new game against a computer
    game = lichess.board.create_game("3") # 3 is the ai level
    # test if the game is created
    assert game.id != None
    # test if the game is against a computer
    assert game.opponent == "ai"
    # test if the game is against the correct ai level
    assert game.ai_level == "3"
    
# Epic 1 user story 2 test
# As a player, I would like to improve my chess skills by solving chess puzzles
def test_solve_puzzle():
    # get the daily puzzle and test if it is a puzzle
    puzzle = lichess.puzzle.get_daily_puzzle()
    assert puzzle != None
    

# Epic 1 user story 4 test
# “As a player, I would like to be able to play against another player (on the same board) but get an indication of moves that I should take”
def test_play_with_hint():
    # create a basic board with starting FEN
    board = lichess.board.create_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # the user should now move the pieces and see if the hint is correct
    # we cannot assert this in the code since it need to be visualized by the user
    # we can however assert that the hint is a valid move
    assert board.get_hint() in board.get_legal_moves()

