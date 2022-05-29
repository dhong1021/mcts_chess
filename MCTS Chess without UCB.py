import chess
import random
from math import log,sqrt,e,inf

class node():
    def __init__(self):
        self.state = chess.Board()  # state = 보드의 상태
        self.action = ''
        self.children = set()
        self.parent = None
        self.N = 0  # Number of times parent node has been visited
        self.n = 0  # number of times child node has been visited
        self.v = 0  # winning score of current node

def rollout(curr_node): 
    if(curr_node.state.is_game_over()): # 현재 노드에서 게임이 끝나면 (leaf 노드에 도달)
        board = curr_node.state
        if(board.result()=='1-0'): # chess library result: 이기면 '1-0' 지면 '0-1' 비기면 '1/2-1/2'를 return
            return (1,curr_node) # 이겼으면 +1
        elif(board.result()=='0-1'):
            return (-1,curr_node) # 졌으면 -1
        else:
            return (0.5,curr_node) # 비겼으면 +0.5
    
    all_moves = [move for move in list(curr_node.state.legal_moves)] # 이동 가능한 모든 이동의 리스트
    
    for i in all_moves:
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push(i) # 현재 보드에서 가능한 이동을 하나씩 해봄
        child = node() # 자식 노드를 하나 만들고
        child.state = tmp_state 
        child.parent = curr_node # 현재 노드가 부모가 됨
        curr_node.children.add(child) # 현재 노드에 모든 이동들이 자식 노드로 추가됨
    rnd_state = random.choice(list(curr_node.children)) # 자식들 중 랜덤 선택

    return rollout(rnd_state)

def expand(curr_node,white): # white = 1
    if(len(curr_node.children)==0): # 자식 없음 = leaf 노드에 도달
        return curr_node
    
    if(white):
        return expand(random.choice(list(curr_node.children)),0) # white턴에는 max_ucb를 가진 자식을 다음 노드로 선택하고 expand

    else:
        return expand(random.choice(list(curr_node.children)),1) # black턴에는 min_ucb를 가진 자식을 다음 노드로 선택하고 expand

def rollback(curr_node,reward):
    curr_node.n+=1  # 노드의 방문수 1 증가
    curr_node.v+=reward  # 노드의 승점을 reward만큼 증가 (이기면 +1, 지면 -1, 비기면 +0.5)
    while(curr_node.parent!=None): # 부모가 있으면 (root 노드에 갈 때 까지)
        curr_node.N+=1 # 부모 노드의 방문수 1증가
        curr_node = curr_node.parent # 현재 노드를 부모 노드로 바꾸면서 한단계씩 윗노드로 올라감
    return curr_node

def mcts_pred(curr_node,over,white,iterations=10): # 반복횟수 설정 iterations
    if(over): # board.is_game_over()
        return -1
    
    all_moves = [move for move in list(curr_node.state.legal_moves)] # 가능한 모든 이동 리스트
    map_state_move = dict()
    
    for i in all_moves:  
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push(i)  
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.children.add(child)
        map_state_move[child] = i
        
    while(iterations>0): 
        if(white):
            ex_child = expand(random.choice(list(curr_node.children)),0)
            reward,state = rollout(ex_child)
            curr_node = rollback(state,reward)
            iterations-=1  # expand -> rollout -> rollback -> iteration -= 1
            
        else:
            ex_child = expand(random.choice(list(curr_node.children)),1)
            reward,state = rollout(ex_child)
            curr_node = rollback(state,reward)
            iterations-=1
            
    if(white):
        selected_move = map_state_move[random.choice(list(curr_node.children))]
        return selected_move
    
    else:
        selected_move = map_state_move[random.choice(list(curr_node.children))]
        return selected_move