#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
from math import inf, log, sqrt, e

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

def ucb(curr_node):
    c = sqrt(2)
    ucb_value = winrate(curr_node) + c * sqrt(log(curr_node.N + e + (10**-6)) / (curr_node.n + (10**-10)))
    return ucb_value
    
def expand(curr_node, white):
    if len(curr_node.children) == 0:
        return curr_node
    
    if(white):
        max_ucb = -inf
        sel_child = None
        for child in curr_node.children:
            tmp = ucb(child)
            if tmp > max_ucb:
                max_ucb = tmp
                sel_child = child
        return expand(sel_child, 0)
    
    else:
        min_ucb = inf
        sel_child = None
        for child in curr_node.children:
            tmp = ucb(child)
            if tmp < min_ucb:
                min_ucb = tmp
                sel_child = child
        return expand(sel_child, 1)
    
def rollout(curr_node):
    if chess.Board.outcome(curr_node.state) != None:
        board = curr_node.state
        if board.result() == '1-0':
            return (1, curr_node)
        elif board.result() ==' 0-1':
            return (-1, curr_node)
        else:
            return (0.5, curr_node)
    
    all_moves = [curr_node.state.san(i) for i in list(curr_node.state.legal_moves)]
    
    for move in all_moves:
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push_san(move)
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.children.add(child)
    rnd_state = random.choice(list(curr_node.children))

    return rollout(rnd_state)

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
            max_ucb = -inf
            sel_child = None
            for child in curr_node.children:
                tmp = ucb(child)
                if tmp > max_ucb:
                    max_ucb = tmp
                    sel_child = child
            ex_child = expand(sel_child, 0)
            reward,state = rollout(ex_child)
            curr_node = rollback(state, reward)
            iterations -= 1
        else:
            min_ucb = inf
            sel_child = None
            for child in curr_node.children:
                tmp = ucb(child)
                if tmp < min_ucb:
                    min_ucb = tmp
                    sel_child = child
            ex_child = expand(sel_child, 1)
            reward,state = rollout(ex_child)
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

