# Overview
This project consists of developing and implementing a computer program that can play a
game against a human opponent.The project will exemplify the minimax algorithm with alpha-
beta pruning, and designing good evaluation functions.

# Game description: Four Connect
Four Connect is also a two-player, fully observable, deterministic, zero-sum game. Players
take turn in dropping discs from the top of an upright board until one player can connect
four discs of the same color in a row horizontally, vertically or diagonally. It is typically
played in a 7 X 6 board (7 columns wide, 6 rows high). Detailed information about the
game can be found in: https://en.wikipedia.org/wiki/Connect_Four

# Project Requirements
- The AI program must be able to play a reasonable game against a human or AI opponent
- The program must have the following components
  - Searching the game tree using a suitable search algorithm
  - Running minimax algorithm on the game tree to select the right move
  - Implementation of alpha-beta pruning to make search faster
  - Design and implementation of an effective evaluation function to evaluate the
    goodness of any intermediate node (state of the board).
  - An early stopping mechanism to be able to abort search and return the minimax
    values based on the evaluation function.
