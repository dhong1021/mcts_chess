import chess
import random
from math import log,sqrt,e,inf

import chess.svg
import time
from IPython.display import SVG

from copy import deepcopy


# MCTS
class node():
    def __init__(self):
        self.state = chess.Board()  # state = 보드의 상태
        self.action = ''
        self.children = set()
        self.parent = None
        self.N = 0  # Number of times parent node has been visited
        self.n = 0  # number of times child node has been visited
        self.v = 0  # winning score of current node

# def ucb1(curr_node):
#     ans = curr_node.v+2*(sqrt(log(curr_node.N+e+(10**-6))/(curr_node.n+(10**-10))))
#     return ans

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
    
    # max_ucb = -inf
    if(white):
        # idx = -1
        # max_ucb = -inf
        # sel_child = None
        # for i in curr_node.children:
        #     tmp = ucb1(i)
        #     if(tmp>max_ucb):
        #         idx = i
        #         max_ucb = tmp
        #         sel_child = i
        return (expand(random.choice(list(curr_node.children)), 0)) # white턴에는 random한 자식을 다음 노드로 선택하고 expand

    else:
        # idx = -1
        # min_ucb = inf
        # sel_child = None
        # for i in curr_node.children:
        #     tmp = ucb1(i)
        #     if(tmp<min_ucb):
        #         idx = i
        #         min_ucb = tmp
        #         sel_child = i
        return (expand(random.choice(list(curr_node.children)), 1)) # black턴에는 random한 자식을 다음 노드로 선택하고 expand

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
            # idx = -1
            # max_ucb = -inf
            # sel_child = None
            # for i in curr_node.children:
            #     tmp = ucb1(i)
            #     if(tmp>max_ucb):
            #         idx = i
            #         max_ucb = tmp
            #         sel_child = i
            ex_child = expand(random.choice(list(curr_node.children)), 0)
            reward,state = rollout(ex_child)
            curr_node = rollback(state,reward)
            iterations-=1  # expand -> rollout -> rollback -> iteration -= 1
            
        else:
            # idx = -1
            # min_ucb = inf
            # sel_child = None
            # for i in curr_node.children:
            #     tmp = ucb1(i)
            #     if(tmp<min_ucb):
            #         idx = i
            #         min_ucb = tmp
            #         sel_child = i
            ex_child = expand(random.choice(list(curr_node.children)), 1)
            reward,state = rollout(ex_child)
            curr_node = rollback(state,reward)
            iterations-=1
            
    if(white):
        # mx = -inf
        # idx = -1
        # selected_move = ''
        # for i in (curr_node.children):
        #     tmp = ucb1(i)
        #     if(tmp>mx):
        #         mx = tmp
        selected_move = map_state_move[child]
        return selected_move
    
    else:
        # mn = inf
        # idx = -1
        # selected_move = ''
        # for i in (curr_node.children):
        #     tmp = ucb1(i)
        #     if(tmp<mn):
        #         mn = tmp
        selected_move = map_state_move[child]
        return selected_move
    
    
    
# MMAB
def minimaxRoot(depth, board,isMaximizing):
    possibleMoves = board.legal_moves
    bestMove = -9999
    bestMoveFinal = None
    for x in possibleMoves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = max(bestMove, minimax(depth - 1, board,-10000,10000, not isMaximizing))
        board.pop()
        if( value > bestMove):
            print("Best score: " ,str(bestMove))
            print("Best move: ",str(bestMoveFinal))
            bestMove = value
            bestMoveFinal = move
    return bestMoveFinal

def minimax(depth, board, alpha, beta, is_maximizing):
    if(depth == 0):
        return -evaluation(board)
    possibleMoves = board.legal_moves
    if(is_maximizing):
        bestMove = -9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = max(bestMove,minimax(depth - 1, board,alpha,beta, not is_maximizing))
            board.pop()
            alpha = max(alpha,bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = 9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = min(bestMove, minimax(depth - 1, board,alpha,beta, not is_maximizing))
            board.pop()
            beta = min(beta,bestMove)
            if(beta <= alpha):
                return bestMove
        return bestMove


def calculateMove(board):
    possible_moves = board.legal_moves
    if(len(possible_moves) == 0):
        print("No more possible moves...Game Over")
        sys.exit()
    bestMove = None
    bestValue = -9999
    n = 0
    for x in possible_moves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        boardValue = -evaluation(board)
        board.pop()
        if(boardValue > bestValue):
            bestValue = boardValue
            bestMove = move

    return bestMove

def evaluation(board):
    i = 0
    evaluation = 0
    x = True
    try:
        x = bool(board.piece_at(i).color)
    except AttributeError as e:
        x = x
    while i < 63:
        i += 1
        evaluation = evaluation + (getPieceValue(str(board.piece_at(i))) if x else -getPieceValue(str(board.piece_at(i))))
    return evaluation


def getPieceValue(piece):
    if(piece == None):
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "N" or piece == "n":
        value = 30
    if piece == "B" or piece == "b":
        value = 30
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 90
    if piece == 'K' or piece == 'k':
        value = 900
    #value = value if (board.piece_at(place)).color else -value
    return value


def main():
    board = chess.Board()
    SVG(chess.svg.board(board = board,size=400))

    while True:
        # MCTS move
        root = node()
        white = 1
        mov = mcts_pred(root, board.is_game_over(), white)
        board.push(mov)
        print("MCTS Turn:")
        SVG(chess.svg.board(board = board,size=400))
        time.sleep(1)
        print(board)
        print("\n")

        # MMAB move
        print("MMAB Turn:")
        move = minimaxRoot(3,board,True)
        move = chess.Move.from_uci(str(move))
        board.push(move)
        SVG(chess.svg.board(board = board,size=400))
        time.sleep(1)
        print(board)
        print("\n")
    
    board.outcome()
        
if __name__ == "__main__":
    main()
