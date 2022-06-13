import random
import chess
from math import inf, log, sqrt, e

class node():
    def __init__(self):
        self.state = chess.Board()
        self.children = set()
        self.parent = None
        self.t = 0
        self.n = 0
        self.v = 0
        self.win = 0
        
def winrate(cur_node):
    if cur_node.n == 0:
        return 0
    else:
        return cur_node.win / cur_node.n

def ucb(cur_node):
    c = sqrt(2)
    ucb_value = winrate(cur_node) + c * sqrt(log(cur_node.t + e + (10**-6)) / (cur_node.n + (10**-10)))
    return ucb_value
    
def ucb_expand(cur_node, white_turn):
    if len(cur_node.children) == 0:
        return cur_node
    
    if white_turn:
        max_ucb = -inf
        selected_child = None
        for child in cur_node.children:
            temp = ucb(child)
            if temp > max_ucb:
                max_ucb = temp
                selected_child = child
        return ucb_expand(selected_child, False)
    
    else:
        min_ucb = inf
        selected_child = None
        for child in cur_node.children:
            temp = ucb(child)
            if temp < min_ucb:
                min_ucb = temp
                selected_child = child
        return ucb_expand(selected_child, True)
    
def ucb_rollout(cur_node):
    if chess.Board.outcome(cur_node.state) != None:
        board = cur_node.state
        if board.result() == '1-0':
            return (1, cur_node)
        elif board.result() ==' 0-1':
            return (-1, cur_node)
        else:
            return (0.5, cur_node)
    
    all_moves = [cur_node.state.san(move) for move in list(cur_node.state.legal_moves)]
    
    for move in all_moves:
        temp_state = chess.Board(cur_node.state.fen())
        temp_state.push_san(move)
        child = node()
        child.state = temp_state
        child.parent = cur_node
        cur_node.children.add(child)
    random_state = random.choice(list(cur_node.children))

    return ucb_rollout(random_state)

def rollback(cur_node, reward):
    while cur_node.parent != None:
        cur_node.n += 1
        cur_node.v += reward
        cur_node.t += 1
        if reward == 1:
            cur_node.win += 1
        cur_node = cur_node.parent
    return cur_node

def ucb_mcts(cur_node, over, white_turn, iterations):
    if(over != None):
        return -1
    
    all_moves = [root.state.san(move) for move in list(root.state.legal_moves)]
    state_moves = dict()

    for move in all_moves:
        temp_state = chess.Board(root.state.fen())
        temp_state.push_san(move)
        child = node()
        child.state = temp_state
        child.parent = root
        root.children.add(child)
        state_moves[child] = move
        
    while iterations > 0:
        if white_turn:
            max_ucb = -inf
            selected_child = None
            for child in cur_node.children:
                temp = ucb(child)
                if temp > max_ucb:
                    max_ucb = temp
                    selected_child = child
            expand_child = ucb_expand(selected_child, False)
            reward,state = ucb_rollout(expand_child)
            cur_node = rollback(state, reward)
            iterations -= 1
        else:
            min_ucb = inf
            selected_child = None
            for child in cur_node.children:
                temp = ucb(child)
                if temp < min_ucb:
                    min_ucb = temp
                    selected_child = child
            expand_child = ucb_expand(selected_child, True)
            reward,state = ucb_rollout(expand_child)
            cur_node = rollback(state, reward)
            iterations -= 1
            
    if white_turn:
        mx = -inf
        selected_move = ''
        for child in cur_node.children:
            temp = winrate(child)
            if temp > mx:
                mx = temp
                selected_move = state_moves[child]
        return selected_move
    else:
        mn = inf
        selected_move = ''
        for child in cur_node.children:
            temp = winrate(child)
            if temp < mn:
                mn = temp
                selected_move = state_moves[child]
        return selected_move

board = chess.Board()
while chess.Board.outcome(board) is None:
    if board.turn:
        root = node()
        root.state = board
        next_move = ucb_mcts(root, chess.Board.outcome(board), board.turn, 5)
        board.push_san(next_move)
        print(board)
    else:
        root = node()
        root.state = board
        next_move = ucb_mcts(root, chess.Board.outcome(board), board.turn, 5)
        board.push_san(next_move)
        print(board)
print(chess.Board.outcome(board))
