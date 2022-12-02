# ChessMate

raspberry pi (Server) 
app (UI)
arduinio (board) (Serial io)

## happy flow
open app -> connect to board using bt -> new game -> stockfish/lichess(online) 
--> python-chess init game --> (board check : check that the start position have all the pieces on the board)
--> game communication: ()

### Application:
UI
Settings
Screens:
Lichess login

### Menu:
1. new game -> stockfish/Lichess -> stockfish -> game stteings -> start, ->> lichess -> connect if not connected and game settings -> start
2. Settings

#Arduino - Raspberry pi COM
Our arduino consists of 64 hall sensors, all 64 sensors form a grid.
Each collum can be enabled seperatly (only once column can be enabled at a time) and we can read input from one row.
Giving us a multiplex 64 input with only 16 pins.

to understand how arduino reads the Data see [board information](Board/README.md).


