import chess
import chess.pgn
import chess.engine
import random
import time
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

def ucb1(curr_node):
    ans = curr_node.v+2*(sqrt(log(curr_node.N+e+(10**-6))/(curr_node.n+(10**-10))))
    return ans

def rollout(curr_node): 
    if(curr_node.state.is_game_over()): # 현재 노드에서 게임이 끝나면 (leaf 노드에 도달)
        board = curr_node.state
        if(board.result()=='1-0'): # chess library result: 이기면 '1-0' 지면 '0-1' 비기면 '1/2-1/2'를 return
            return (1,curr_node) # 이겼으면 +1
        elif(board.result()=='0-1'):
            return (-1,curr_node) # 졌으면 -1
        else:
            return (0.5,curr_node) # 비겼으면 +0.5
    
    all_moves = [curr_node.state.san(i) for i in list(curr_node.state.legal_moves)] # 이동 가능한 모든 이동의 리스트
    
    for i in all_moves:
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push_san(i) # 현재 보드에서 가능한 이동을 하나씩 해봄
        child = node() # 자식 노드를 하나 만들고
        child.state = tmp_state 
        child.parent = curr_node # 현재 노드가 부모가 됨
        curr_node.children.add(child) # 현재 노드에 모든 이동들이 자식 노드로 추가됨
    rnd_state = random.choice(list(curr_node.children)) # 자식들 중 랜덤 선택

    return rollout(rnd_state)

def expand(curr_node,white): # white = 1
    if(len(curr_node.children)==0): # 자식 없음 = leaf 노드에 도달
        return curr_node
    
    max_ucb = -inf
    if(white):
        idx = -1
        max_ucb = -inf
        sel_child = None
        for i in curr_node.children:
            tmp = ucb1(i)
            if(tmp>max_ucb):
                idx = i
                max_ucb = tmp
                sel_child = i
        return(expand(sel_child,0)) # white턴에는 max_ucb를 가진 자식을 다음 노드로 선택하고 expand

    else:
        idx = -1
        min_ucb = inf
        sel_child = None
        for i in curr_node.children:
            tmp = ucb1(i)
            if(tmp<min_ucb):
                idx = i
                min_ucb = tmp
                sel_child = i
        return expand(sel_child,1) # black턴에는 min_ucb를 가진 자식을 다음 노드로 선택하고 expand

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
    
    all_moves = [curr_node.state.san(i) for i in list(curr_node.state.legal_moves)] # 가능한 모든 이동 리스트
    map_state_move = dict()
    
    for i in all_moves:
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push_san(i)
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.children.add(child)
        map_state_move[child] = i
        
    while(iterations>0):
        if(white):
            idx = -1
            max_ucb = -inf
            sel_child = None
            for i in curr_node.children:
                tmp = ucb1(i)
                if(tmp>max_ucb):
                    idx = i
                    max_ucb = tmp
                    sel_child = i
            ex_child = expand(sel_child,0)
            reward,state = rollout(ex_child)
            curr_node = rollback(state,reward)
            iterations-=1
        else:
            idx = -1
            min_ucb = inf
            sel_child = None
            for i in curr_node.children:
                tmp = ucb1(i)
                if(tmp<min_ucb):
                    idx = i
                    min_ucb = tmp
                    sel_child = i

            ex_child = expand(sel_child,1)

            reward,state = rollout(ex_child)

            curr_node = rollback(state,reward)
            iterations-=1
    if(white):
        
        mx = -inf
        idx = -1
        selected_move = ''
        for i in (curr_node.children):
            tmp = ucb1(i)
            if(tmp>mx):
                mx = tmp
                selected_move = map_state_move[i]
        return selected_move
    else:
        mn = inf
        idx = -1
        selected_move = ''
        for i in (curr_node.children):
            tmp = ucb1(i)
            if(tmp<mn):
                mn = tmp
                selected_move = map_state_move[i]
        return selected_move




board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci('stockfish')

white = 1
moves = 0
pgn = []
game = chess.pgn.Game()
evaluations = []
sm = 0
cnt = 0
while((not board.is_game_over())):
    all_moves = [board.san(i) for i in list(board.legal_moves)]
    #start = time.time()
    root = node()
    root.state = board
    result = mcts_pred(root,board.is_game_over(),white)
    #sm+=(time.time()-start)
    board.push_san(result)
    #print(result)
    pgn.append(result)
    white ^= 1
    #cnt+=1
    
    moves+=1
    #board_evaluation = evaluate(board.fen().split()[0])
    #evaluations.append(board_evaluation)
#print("Average Time per move = ",sm/cnt)
print(board)
print(" ".join(pgn))
print()
#print(evaluations)
print(board.result())
game.headers["Result"] = board.result()
#print(game)
engine.quit()
