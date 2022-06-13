import random
from math import inf, ceil

class node():
    def __init__(self):
        self.state = chess.Board()
        self.children = set()
        self.parent = None
        self.N = 0
        self.n = 0
        self.v = 0
        self.win = 0
        
def winrate(curr_node):
    if curr_node.n == 0:
        return 0
    else:
        return curr_node.win / curr_node.n
    
def expand(curr_node, white):
    if len(curr_node.children) == 0:
        return curr_node
    
    if white:
        return expand(random.choice(list(curr_node.children)), 0)

    else:
        return expand(random.choice(list(curr_node.children)), 1)
    
def rollout(curr_node, ngram):
    if chess.Board.outcome(curr_node.state) != None:
        board = curr_node.state
        if board.result() == '1-0':
            return (1, curr_node)
        elif board.result() ==' 0-1':
            return (-1, curr_node)
        else:
            return (0.5, curr_node)
    
    all_moves = [curr_node.state.san(i) for i in list(curr_node.state.legal_moves)]
    epsgrd = random.randrange(10)
    epsgrd_limit = 3
    
    if epsgrd > epsgrd_limit and ngram:
        ngram_move = ngram_enhanced_3gram(curr_node)
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push(ngram_move)
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.children.add(child)
    else:
        for move in all_moves:
            tmp_state = chess.Board(curr_node.state.fen())
            tmp_state.push_san(move)
            child = node()
            child.state = tmp_state
            child.parent = curr_node
            curr_node.children.add(child)
        
    rnd_state = random.choice(list(curr_node.children))
    return rollout(rnd_state, False)

def ngram_enhanced_2gram(curr_node):
    base_board = chess.Board(curr_node.state.fen())
    base_score = -inf
    temp_best = ''
    base_sample = random.sample(list(base_board.legal_moves), ceil(len(list(base_board.legal_moves))/3))
    for i in base_sample:
        temp_board_i = chess.Board(base_board.fen())
        temp_score_i = 0
        if temp_board_i.is_capture(i):
            temp_score_i = 1
        temp_board_i.push(i)
        temp_sample_i = random.sample(list(temp_board_i.legal_moves), ceil(len(list(temp_board_i.legal_moves))/3))
        for j in temp_sample_i:
            temp_board_j = chess.Board(temp_board_i.fen())
            temp_score_j = 0
            if temp_board_j.is_capture(j):
                temp_score_j = -1
            if base_score <= (temp_score_i + temp_score_j):
                base_score = temp_score_i + temp_score_j
                temp_best = i
    return temp_best

def ngram_enhanced_3gram(curr_node):
    base_board = chess.Board(curr_node.state.fen())
    base_score = -inf
    temp_best = ''
    base_sample = random.sample(list(base_board.legal_moves), ceil(len(list(base_board.legal_moves))/3))
    for i in base_sample:
        temp_board_i = chess.Board(base_board.fen())
        temp_score_i = 0
        if temp_board_i.is_capture(i):
            temp_score_i = 1
        temp_board_i.push(i)
        temp_sample_i = random.sample(list(temp_board_i.legal_moves), ceil(len(list(temp_board_i.legal_moves))/3))
        for j in temp_sample_i:
            temp_board_j = chess.Board(temp_board_i.fen())
            temp_score_j = 0
            if temp_board_j.is_capture(j):
                temp_score_j = -1
            temp_board_j.push(j)
            temp_sample_j = random.sample(list(temp_board_j.legal_moves), ceil(len(list(temp_board_j.legal_moves))/3))
            for k in temp_sample_j:
                temp_board_k = chess.Board(temp_board_j.fen())
                temp_score_k = 0
                if temp_board_k.is_capture(k):
                    temp_score_k = 1
                if base_score <= (temp_score_i + temp_score_j + temp_score_k):
                    base_score = temp_score_i + temp_score_j + temp_score_k
                    temp_best = i
    return temp_best

def ngram_enhanced_4gram(curr_node):
    base_board = chess.Board(curr_node.state.fen())
    base_score = -inf
    temp_best = ''
    base_sample = random.sample(list(base_board.legal_moves), ceil(len(list(base_board.legal_moves))/3))
    for i in base_sample:
        temp_board_i = chess.Board(base_board.fen())
        temp_score_i = 0
        if temp_board_i.is_capture(i):
            temp_score_i = 1
        temp_board_i.push(i)
        temp_sample_i = random.sample(list(temp_board_i.legal_moves), ceil(len(list(temp_board_i.legal_moves))/3))
        for j in temp_sample_i:
            temp_board_j = chess.Board(temp_board_i.fen())
            temp_score_j = 0
            if temp_board_j.is_capture(j):
                temp_score_j = -1
            temp_board_j.push(j)
            temp_sample_j = random.sample(list(temp_board_j.legal_moves), ceil(len(list(temp_board_j.legal_moves))/3))
            for k in temp_sample_j:
                temp_board_k = chess.Board(temp_board_j.fen())
                temp_score_k = 0
                if temp_board_k.is_capture(k):
                    temp_score_k = 1
                temp_board_k.push(k)
                temp_sample_k = random.sample(list(temp_board_k.legal_moves), ceil(len(list(temp_board_k.legal_moves))/3))
                for s in temp_sample_k:
                    temp_board_s = chess.Board(temp_board_k.fen())
                    temp_score_s = 0
                    if temp_board_s.is_capture(s):
                        temp_score_s = -1
                    if base_score <= (temp_score_i + temp_score_j + temp_score_k + temp_score_s):
                        base_score = temp_score_i + temp_score_j + temp_score_k + temp_score_s
                        temp_best = i
    return temp_best

def rollback(curr_node, reward):
    while curr_node.parent != None:
        curr_node.n += 1
        curr_node.v += reward
        curr_node.N += 1
        if reward == 1:
            curr_node.win += 1
        curr_node = curr_node.parent
    return curr_node

def mcts(curr_node, over, white, iterations):
    if(over != None):
        return -1
    
    all_moves = [root.state.san(move) for move in list(root.state.legal_moves)]
    map_state_move = dict()

    for move in all_moves:
        tmp_state = chess.Board(root.state.fen())
        tmp_state.push_san(move)
        child = node()
        child.state = tmp_state
        child.parent = root
        root.children.add(child)
        map_state_move[child] = move
        
    while iterations > 0:
        if white:
            ex_child = expand(curr_node, 0)
            reward,state = rollout(ex_child, True)
            curr_node = rollback(state, reward)
            iterations -= 1
        else:
            ex_child = expand(curr_node, 1)
            reward,state = rollout(ex_child, True)
            curr_node = rollback(state, reward)
            iterations -= 1
            
    if white:
        mx = -inf
        selected_move = ''
        for child in curr_node.children:
            tmp = winrate(child)
            if tmp > mx:
                mx = tmp
                selected_move = map_state_move[i]
        return selected_move
    else:
        mn = inf
        selected_move = ''
        for child in curr_node.children:
            tmp = winrate(child)
            if tmp < mn:
                mn = tmp
                selected_move = map_state_move[i]
        return selected_move

