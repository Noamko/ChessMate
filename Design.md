# Project design

## Introduction

The project is seperared into 3 parts:
1. The board (arduino)
2. The server (raspberry pi)
3. mobile app (android, ios)

## Board

The board is the physical part of the project, it is the chess board that the user plays on.
The board is connected to the server via serial communication.

### Board information

The board is a 8x8 grid of hall sensors, the sensors are connected to the arduino in a multiplexed way.
The arduino can enable one collum at a time and read the input from all the rows.
This gives us a 64 input with only 16 pins.

The board is connected to the server via serial communication.

### Board design
 TODO: add image

## Server

The server is the part of the project that is connected to the internet.
The server is connected to the board via serial communication.

### Server information

The server is a raspberry pi 4, it controls all the logic of the game.
running on ubuntu 20.04.

