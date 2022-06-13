import random
import chess
from math import inf

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
    
def expand(cur_node, white):
    if len(cur_node.children) == 0:
        return cur_node
    
    if white:
        return expand(random.choice(list(cur_node.children)), 0)

    else:
        return expand(random.choice(list(cur_node.children)), 1)
    
def pure_rollout(cur_node):
    if chess.Board.outcome(cur_node.state) != None:
        board = cur_node.state
        if board.result() == '1-0':
            return (1, cur_node)
        elif board.result() ==' 0-1':
            return (-1, cur_node)
        else:
            return (0.5, cur_node)
    
    all_moves = [cur_node.state.san(i) for i in list(cur_node.state.legal_moves)]
    
    for i in all_moves:
        temp_state = chess.Board(cur_node.state.fen())
        temp_state.push_san(i)
        child = node()
        child.state = temp_state
        child.parent = cur_node
        cur_node.children.add(child)
    random_state = random.choice(list(cur_node.children))

    return pure_rollout(random_state)

def rollback(cur_node, reward):
    while cur_node.parent != None:
        cur_node.n += 1
        cur_node.v += reward
        cur_node.t += 1
        if reward == 1:
            cur_node.win += 1
        cur_node = cur_node.parent
    return cur_node

def mcts_Pure(cur_node, over, white, iterations):
    if(over != None):
        return -1
    
    all_moves = [root.state.san(move) for move in list(root.state.legal_moves)]
    state_moves = dict()

    for i in all_moves:
        temp_state = chess.Board(root.state.fen())
        temp_state.push_san(i)
        child = node()
        child.state = temp_state
        child.parent = root
        root.children.add(child)
        state_moves[child] = i
        
    while iterations > 0:
        if white:
            expand_child = expand(cur_node, 0)
            reward,state = pure_rollout(expand_child)
            cur_node = rollback(state, reward)
            iterations -= 1
        else:
            expand_child = expand(cur_node, 1)
            reward,state = pure_rollout(expand_child)
            cur_node = rollback(state, reward)
            iterations -= 1
            
    if white:
        mx = -inf
        selected_move = ''
        for i in cur_node.children:
            temp = winrate(i)
            if temp > mx:
                mx = temp
                selected_move = state_moves[i]
        return selected_move
    else:
        mn = inf
        selected_move = ''
        for i in cur_node.children:
            temp = winrate(i)
            if temp < mn:
                mn = temp
                selected_move = state_moves[i]
        return selected_move
