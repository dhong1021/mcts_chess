import board

from typing import Callable
#from gamestate import GameState


class Player:
    def __init__(self, name: str, strategy: Callable[[board], int]):
        self.name = name
        self.strategy = strategy

    def get_move(self, game_state: board):
        return self.strategy(game_state)

    def __repr__(self):
        return f'Player {self.name}'
