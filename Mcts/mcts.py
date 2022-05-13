import numpy as np
import logging

from gamestate import GameState
from mctsNode import MctsNode


class Mcts:
    # 학습, 테스트는 없다.
    # 실제 게임 트리의 깊이에 관계없이 시뮬레이션에 따라 최선의 움직임만 얻는다.
    # number_of_simulation = inf, MCTS --> Minimax.
    @staticmethod
    def get_best_move(game_state: GameState, number_of_simulation=100):
        root = MctsNode(game_state, None)
        for i in range(number_of_simulation):
            logging.debug(f'\nIteration number: {i + 1}')
            leaf_node = root.select(c=np.sqrt(2))  # @Todo: Move this c to be a parameter of MCTS
            winner = leaf_node.rollout()
            leaf_node.backpropagate(winner)

        Mcts.__print_tree(root)

        # 마지막으로 행동을 selection 할 때 explore 해서는 안 됩니다.
        return root.select_child_with_max_ucb(c=0).action

    @staticmethod
    def __print_tree(root: MctsNode):
        logging.debug('\n 현재 트리 인쇄:')
        queue = [root]
        while queue:
            popped_node = queue.pop()
            logging.debug(popped_node)
            for child_node in popped_node.children:
                queue.append(child_node)
        logging.debug('\n')
