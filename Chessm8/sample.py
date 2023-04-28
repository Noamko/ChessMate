from game import game

if __name__ == '__main__':
    game = game.game()

    while True:
        print(game.get_board_state())
        move = input("Enter move: ")
        if game.move(move):
            print("Move made")
        else:
            print("Invalid move")