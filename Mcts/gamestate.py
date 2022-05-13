from __future__ import annotations
import numpy as np

from drawplayer import SingletonDrawPlayer


class GameState:
    def __init__(self, players: np.array, turn: int, game_board: np.array()):
        assert (turn == -1 or turn == 1)
        self.board_size = len(game_board)
        self.game_board = game_board
        self.players = players
        self.turn = turn
        self.winner = None
        self.move_map = dict(map(
            lambda x: (x, (np.int(x / self.board_size), x % self.board_size)),
            list(range(0, self.board_size ** 2))))
        self.reverse_move_map = {value: key for (key, value) in self.move_map.items()}

    # 플레이어 1에 -1을 할당하고 플레이어 2에 1을 할당합니다.
    def make_move(self, move_index: int) -> GameState:
        # Python에서 assert 문은 주어진 조건이 True 로 평가되는 경우 실행을 계속하는 데 사용됩니다.
        # assert 조건이 False로 평가되면 지정된 오류 메시지와 함께 AssertionError 예외가 발생합니다.
        assert (0 <= move_index <= self.board_size ** 2 - 1)
        assert (move_index in self.get_valid_moves())

        game_board = self.game_board.copy()
        move = self.move_map[move_index]
        game_board[move[0], move[1]] = self.turn

        return GameState(self.players, self.turn * -1, game_board)

    # 체스나 바둑과 같은 다른 완전한 정보 게임에서 이러한 움직임은 현재 플레이어에 따라 다릅니다.
    def get_valid_moves(self) -> list:
        moves = []
        for move in self.reverse_move_map.keys():
            if self.game_board[move[0]][move[1]] == 0:
                moves.append(self.reverse_move_map[move])

        return moves

    def copy(self) -> GameState:
        return GameState(self.players, self.turn, self.game_board.copy())

    @property
    def current_player(self):
        if self.turn == -1:
            return self.players[1]
        else:
            return self.players[0]

    @property
    def is_game_over(self):  # 게임이 아직 진행 중이면 승리한 플레이어와 None을 반환합니다.
        winning_possibilities = self.__get_winning_possibilities()

        if GameState.__check_board(winning_possibilities, self.board_size):
            self.winner = self.players[0]

        if GameState.__check_board(winning_possibilities, - self.board_size):
            self.winner = self.players[1]

        zeros_indices, = np.where(self.game_board.flatten() == 0)
        if len(zeros_indices) == 0:
            self.winner = SingletonDrawPlayer

        return self.winner is not None

    def __get_winning_possibilities(self):
        row_sum = self.game_board.sum(0)
        col_sum = self.game_board.sum(1)
        diagonal = [self.game_board.trace()]
        inv_diagonal = [self.game_board[::-1].trace()]
        return np.concatenate((row_sum, col_sum, diagonal, inv_diagonal))

    @staticmethod
    def __check_board(winning_possibilities, winning_number):
        return any(winning_possibilities == winning_number)

    def __repr__(self):
        return self.game_board.__repr__()