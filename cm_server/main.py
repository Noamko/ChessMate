"""  Chess8 main file. 
        This file is the main file for the chessm8 project.
        It will be responsible for running the game and 
        communicating with the chess engine & the chess board.

    Basic flow:
        1. Initialize bluetooth connection with Android app (durint )
        2. Initialize ack with chessboard
        3. Initialize chess engine
        4. Wait for commands from Android app
"""
import sys
import time
import os
from engine import CMEngine

def main():
    # start chessm8 engine
    print("Starting ChesssMate ")
    engine = CMEngine()
    engine.start()

if __name__ == '__main__':
    main()
    