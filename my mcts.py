import numpy as np
from collections import defaultdict

from __future__ import annotations
import logging


class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, parent_action=None):
        # 생성자 > 변수들 초기화

        self.state = state
        # 보드 상태(ex. 배열 nxn)
        self.parent = parent
        # 루트 노드
        self.parent_action = parent_action
        self.children = []
        # 현재 노드에서 가능한 모든 값 포함
        self._number_of_visits = 0
        # 현재 노드 방문 횟수
        self._results = defaultdict(int)
        self._results[1] = 0
        # 승
        self._results[-1] = 0
        # 패
        self._untried_actions = None
        # 가능한 모든 이동
        self._untried_actions = self.untried_actions()
        # 수행해야하는 이동
        return

    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    # 시도되지 않은 작업 목록 반환

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses
    # 승패 차이 반환

    def n(self):
        return self._number_of_visits
    # 각 노드 방문 횟수 반환

    def expand(self):

        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    # 현 상태 > 수행 작업 > 다음 상태 / 모든 가능한 자식 노드 -> 자식 배열 추가, 그에 따른 child_node 반환

    def is_terminal_node(self):
        return self.state.is_game_over()

    # 현재 노드가 마지막 노드인지 확인

    def rollout(self):
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():

            possible_moves = current_rollout_state.get_legal_actions()

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()

    # 현 상태에서 결과가 나올 때까지 전체 게임 시뮬레이션 후 결과 반환

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    # 노드 통계 업데이트 / 부모 노드에 도달할 때까지 각 노드의 방문 횟수 1씩 증가. + 승패도

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0
    # _untried_actions에서 하나씩, 크기가 0일 때 완전 확장

    def best_child(self, c_param=0.1):

        choices_weights = [(c.q() / c.n()) + c_param *
                           np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    # 완전 확장 후 자식 중 가장 좋은 것을 선택

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    # 이동 가능한 수 중 무작위로 선택

    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    # rollout 수행할 노트 select

    def best_action(self):
        simulation_no = 100

        for i in range(simulation_no):

            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)
    # 가장 좋은 수 / 확장, 시뮬레이션, 역전파 수행 명령

    def get_legal_actions(self):
        # 현 상황에서 가능한 모든 움직임 / chess 라이브러리 적용으로 대체

    def is_game_over(self):
        # 게임 규칙에 따라 반환 / chess 라이브러리 적용으로 대체

    def game_result(self):
        # 체크메이트, 교착 상태, 기물 부족 등 / 결과 값 산출

    def move(self, action):
        # 보드 초기 상태에서 배치하는 규칙 / chess 라이브러리 적용으로 대체

    def main():
        root = MonteCarloTreeSearchNode(state=initial_state)
        selected_node = root.best_action()
        return
