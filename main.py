import board, pieces, mmab, mcts

from functools import partial
import logging
import numpy as np
import random
import sys

from player import Player

# from gamestate import GameState
# from minimax import Minimax
# from montecarlotreesearch import MonteCarloTreeSearch
# from player import Player



p1 = Player('P1', mcts.MCTS.get_MCTS_move(board, []))
p2 = Player('P2', mmab.MMAB.get_MMAB_move(board, []))
# p2 = Player('P2', lambda game_state: random.choice(game_state.get_valid_moves()))
players = [p1, p2]



#
# Entry point.
#
board = board.Board.new()
print(board.to_string())


i = 0
while True:
    MCTS_move = mcts.MCTS.get_MCTS_move(board, [])
    if (MCTS_move == 0):
        if (board.is_check(pieces.Piece.WHITE)):
            print("Checkmate. Black Wins.")
            break
        else:
            print("Stalemate.")
            break

    board.perform_move(MCTS_move)
    print("MCTS move: " + MCTS_move.to_string())
    print(board.to_string())
    
    player = players[i % 2]
    
    i += 1

    MMAB_move = mmab.MMAB.get_MMAB_move(board, [])
    if (MMAB_move == 0):
        if (board.is_check(pieces.Piece.BLACK)):
            print("Checkmate. White wins.")
            break
        else:
            print("Stalemate.")
            break

    board.perform_move(MMAB_move)
    print("MMAB move: " + MMAB_move.to_string())
    print(board.to_string())
    
    player = players[i % 2]
    
    i += 1
