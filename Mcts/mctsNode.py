from __future__ import annotations
import logging
import numpy as np

from drawplayer import SingletonDrawPlayer
from gamestate import GameState
from rolloutstrategyhelper import RolloutStrategyHelper


class MctsNode:
    # 이 작업은 상위 MCTS 노드의 플레이어, 즉 이전 게임 상태가 수행한 작업입니다. 이 정보는 승률을 계산할 때 매우 중요합니다(아래 참조).
    def __init__(self, game_state: GameState, parent: MctsNode, action=None):
        self.game_state = game_state
        self.parent = parent
        self.action = action
        self.children = np.array([], dtype=MctsNode)
        self.untried_actions = game_state.get_valid_moves()
        self.wins = dict(map(lambda player: (player, 0), game_state.players))
        self.wins[SingletonDrawPlayer] = 0
        self.visits = 0

    def select(self, c) -> MctsNode:
        leaf_node = self
        while not leaf_node.is_terminal:
            if not leaf_node.is_fully_expanded:
                return leaf_node.expand()
            else:
                leaf_node = leaf_node.select_child_with_max_ucb(c)

        return leaf_node

    def expand(self) -> MctsNode:
        logging.debug(f'Expanding for {self.__repr__()}')
        action = self.untried_actions.pop()
        new_game_state = self.game_state.make_move(action)
        child_node = MctsNode(new_game_state, self, action)
        self.children = np.append(self.children, child_node)
        logging.debug(f'Created {child_node.__repr__()}')
        return child_node

    # rollout strategy에 의존하여 학습한다..
    def rollout(self):
        logging.debug(f'Rollout now for {self.__repr__()}')
        rollout_state = self.game_state
        while not rollout_state.is_game_over:
            move = MctsNode.get_move_from_rollout_strategy(rollout_state)
            rollout_state = rollout_state.make_move(move)
        logging.debug(f'The winner of this rollout: {rollout_state.winner}')
        return rollout_state.winner

    def backpropagate(self, who_won):
        self.visits += 1
        self.wins[who_won] += 1
        if self.parent is not None:
            self.parent.backpropagate(who_won)

    # 이 비율은 승리를 최대화하려고 합니다. 손실을 최소화하려고 하지 않습니다.
    def select_child_with_max_ucb(self, c) -> MctsNode:
        ucb_values = list(map(lambda child: MctsNode.get_ucb(child, c), self.children))
        return self.children[np.argmax(ucb_values)]

    @staticmethod
    def get_ucb(child: MctsNode, c: float):
        return child.win_ratio + c * np.sqrt(np.log(child.parent.visits) / child.visits)

    @staticmethod
    def get_move_from_rollout_strategy(rollout_state: GameState) -> int:
        return RolloutStrategyHelper.get_heuristic_move(rollout_state)

    @property
    def win_ratio(self):
        if self.parent is None:  # In case it's the parent node.
            return 0
        # If the node hasn't been visited, then the win_ratio (part of ucb) is inf. This means it will be selected.
        # One thing to try is wins - loses.
        if self.visits == 0:
            return np.inf
        return self.wins[self.parent.game_state.current_player] / self.visits

    @property
    def is_fully_expanded(self):
        return len(self.children) == len(self.game_state.get_valid_moves())

    @property
    def is_terminal(self):
        return self.game_state.winner is not None

    def __get_self_ucb(self, c=np.sqrt(2)):
        if self.parent is not None:
            return self.win_ratio + c * np.sqrt(np.log(self.parent.visits) / self.visits)
        return 0

    def __repr__(self):
        return f'TreeNode: {id(self)}'

    def __str__(self):
        return f'TreeNode: {id(self)}, action: {self.action}, number of visits: {self.visits}, ' \
               f'win ratio: {self.win_ratio}, ucb: {self.__get_self_ucb()} fully expanded: {self.is_fully_expanded}, ' \
               f'children: {self.children}, turn: {self.game_state.turn}, game: \n{self.game_state}'
