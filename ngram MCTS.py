import random
import chess
from math import inf, ceil

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
    
def Ngram_rollout(cur_node, ngram):
    if chess.Board.outcome(cur_node.state) != None:
        board = cur_node.state
        if board.result() == '1-0':
            return (1, cur_node)
        elif board.result() ==' 0-1':
            return (-1, cur_node)
        else:
            return (0.5, cur_node)
    
    all_moves = [cur_node.state.san(i) for i in list(cur_node.state.legal_moves)]
    epsgrd = random.randrange(10)
    epsgrd_limit = 3
    
    if epsgrd > epsgrd_limit and ngram:
        ngram_move = ngram_enhanced_3gram(cur_node)
        temp_state = chess.Board(cur_node.state.fen())
        temp_state.push(ngram_move)
        child = node()
        child.state = temp_state
        child.parent = cur_node
        cur_node.children.add(child)
    else:
        for i in all_moves:
            temp_state = chess.Board(cur_node.state.fen())
            temp_state.push_san(i)
            child = node()
            child.state = temp_state
            child.parent = cur_node
            cur_node.children.add(child)
        
    random_state = random.choice(list(cur_node.children))
    return Ngram_rollout(random_state, False)

def ngram_enhanced_2gram(cur_node):
    base_board = chess.Board(cur_node.state.fen())
    base_score = -inf
    temp_best = ''
    base_sample = random.sample(list(base_board.legal_moves), ceil(len(list(base_board.legal_moves))/2))
    for i in base_sample:
        temp_board_i = chess.Board(base_board.fen())
        temp_score_i = 0
        if temp_board_i.is_capture(i):
            temp_score_i = 1
        temp_board_i.push(i)
        temp_sample_i = random.sample(list(temp_board_i.legal_moves), ceil(len(list(temp_board_i.legal_moves))/2))
        for j in temp_sample_i:
            temp_board_j = chess.Board(temp_board_i.fen())
            temp_score_j = 0
            if temp_board_j.is_capture(j):
                temp_score_j = -1
            if base_score <= (temp_score_i + temp_score_j):
                base_score = temp_score_i + temp_score_j
                temp_best = i
    return temp_best

def ngram_enhanced_3gram(cur_node):
    base_board = chess.Board(cur_node.state.fen())
    base_score = -inf
    temp_best = ''
    base_sample = random.sample(list(base_board.legal_moves), ceil(len(list(base_board.legal_moves))/2))
    for i in base_sample:
        temp_board_i = chess.Board(base_board.fen())
        temp_score_i = 0
        if temp_board_i.is_capture(i):
            temp_score_i = 1
        temp_board_i.push(i)
        temp_sample_i = random.sample(list(temp_board_i.legal_moves), ceil(len(list(temp_board_i.legal_moves))/2))
        for j in temp_sample_i:
            temp_board_j = chess.Board(temp_board_i.fen())
            temp_score_j = 0
            if temp_board_j.is_capture(j):
                temp_score_j = -1
            temp_board_j.push(j)
            temp_sample_j = random.sample(list(temp_board_j.legal_moves), ceil(len(list(temp_board_j.legal_moves))/2))
            for k in temp_sample_j:
                temp_board_k = chess.Board(temp_board_j.fen())
                temp_score_k = 0
                if temp_board_k.is_capture(k):
                    temp_score_k = 1
                if base_score <= (temp_score_i + temp_score_j + temp_score_k):
                    base_score = temp_score_i + temp_score_j + temp_score_k
                    temp_best = i
    return temp_best

def ngram_enhanced_4gram(cur_node):
    base_board = chess.Board(cur_node.state.fen())
    base_score = -inf
    temp_best = ''
    base_sample = random.sample(list(base_board.legal_moves), ceil(len(list(base_board.legal_moves))/2))
    for i in base_sample:
        temp_board_i = chess.Board(base_board.fen())
        temp_score_i = 0
        if temp_board_i.is_capture(i):
            temp_score_i = 1
        temp_board_i.push(i)
        temp_sample_i = random.sample(list(temp_board_i.legal_moves), ceil(len(list(temp_board_i.legal_moves))/2))
        for j in temp_sample_i:
            temp_board_j = chess.Board(temp_board_i.fen())
            temp_score_j = 0
            if temp_board_j.is_capture(j):
                temp_score_j = -1
            temp_board_j.push(j)
            temp_sample_j = random.sample(list(temp_board_j.legal_moves), ceil(len(list(temp_board_j.legal_moves))/2))
            for k in temp_sample_j:
                temp_board_k = chess.Board(temp_board_j.fen())
                temp_score_k = 0
                if temp_board_k.is_capture(k):
                    temp_score_k = 1
                temp_board_k.push(k)
                temp_sample_k = random.sample(list(temp_board_k.legal_moves), ceil(len(list(temp_board_k.legal_moves))/2))
                for s in temp_sample_k:
                    temp_board_s = chess.Board(temp_board_k.fen())
                    temp_score_s = 0
                    if temp_board_s.is_capture(s):
                        temp_score_s = -1
                    if base_score <= (temp_score_i + temp_score_j + temp_score_k + temp_score_s):
                        base_score = temp_score_i + temp_score_j + temp_score_k + temp_score_s
                        temp_best = i
    return temp_best

def rollback(cur_node, reward):
    while cur_node.parent != None:
        cur_node.n += 1
        cur_node.v += reward
        cur_node.t += 1
        if reward == 1:
            cur_node.win += 1
        cur_node = cur_node.parent
    return cur_node

def mcts_Ngram(cur_node, over, white, iterations):
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
            reward,state = Ngram_rollout(expand_child, True)
            cur_node = rollback(state, reward)
            iterations -= 1
        else:
            expand_child = expand(cur_node, 1)
            reward,state = Ngram_rollout(expand_child, True)
            cur_node = rollback(state, reward)
            iterations -= 1
            
    if white:
        mx = -inf
        selected_move = ''
        for j in cur_node.children:
            temp = winrate(j)
            if temp > mx:
                mx = temp
                selected_move = state_moves[j]
        return selected_move
    else:
        mn = inf
        selected_move = ''
        for j in cur_node.children:
            temp = winrate(j)
            if temp < mn:
                mn = temp
                selected_move = state_moves[j]
        return selected_move
