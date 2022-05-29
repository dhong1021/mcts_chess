#!/usr/bin/env python
# coding: utf-8

# In[1]:


import chess
import random
from math import log,sqrt,e,inf

class node():
    def __init__(self):
        self.state = board  
        self.action = ''
        self.children = set()
        self.parent = None
        self.N = 0  
        self.n = 0  
        self.v = 0  
        
def rollout(curr_node): 
    if(curr_node.state.is_game_over()):
        board = curr_node.state
        if(board.result()=='1-0'): 
            return (1,curr_node) 
        elif(board.result()=='0-1'):
            return (-1,curr_node) 
        else:
            return (0.5,curr_node) 

    for move in list(curr_node.state.legal_moves):
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push(move) 
        child = node() 
        child.state = tmp_state 
        child.parent = curr_node 
        curr_node.children.add(child) 
    rnd_state = random.choice(list(curr_node.children))

    return rollout(rnd_state)

def expand(curr_node,white): 
    if(len(curr_node.children)==0): 
        return curr_node
    
    sel_child = random.choice(list(curr_node.children))
    if(white):
        return expand(sel_child,0)
    else:
        return expand(sel_child,1) 
    
def rollback(curr_node,reward):
    curr_node.n+=1  
    curr_node.v+=reward 
    while(curr_node.parent!=None): 
        curr_node.N+=1 
        curr_node = curr_node.parent 
    return curr_node

def mcts_pred(curr_node,over,white,iterations=10):
    if(over): 
        return -1

    map_state_move = dict()

    for move in list(curr_node.state.legal_moves):  
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push(move)  
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.children.add(child)
        map_state_move[child] = move

    while(iterations>0): 
        sel_child = random.choice(list(curr_node.children))
        if(white):
            ex_child = expand(sel_child,0)
            reward,state = rollout(ex_child)
            curr_node = rollback(state,reward)
            iterations-=1
        else:
            ex_child = expand(sel_child,1)
            reward,state = rollout(ex_child)
            curr_node = rollback(state,reward)
            iterations-=1

    if(white):
        mx = -inf
        selected_move = ''
        for child in curr_node.children:
            tmp = child.v
            if (tmp>mx):
                mx = tmp
                selected_move = map_state_move[child]
        return selected_move
    else:
        mn = inf
        selected_move = ''
        for child in curr_node.children:
            tmp = child.v
            if(tmp<mn):
                mn = tmp
                selected_move = map_state_move[child]
        return selected_move


# In[2]:


def evaluate_board():  # 보드 상태를 평가
    
    if board.is_checkmate():  
        if board.turn:
            return -9999  # white(ai)가 체크메이트면 -9999점
        else:
            return 9999  # black(user)가 체크메이트면 9999점
    if board.is_stalemate():  # 그외 draw의 경우엔 0점
        return 0
    if board.is_insufficient_material():
        return 0
    
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    
    material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)  # 각각의 가중치 x (white-black)개수
    
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq= pawnsq + sum([-pawntable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq= sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq= bishopsq + sum([-bishopstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)] 
                                    for i in board.pieces(chess.KING, chess.BLACK)])
    
    eval = material + pawnsq + knightsq + bishopsq+ rooksq+ queensq + kingsq
    if board.turn:
        return eval  # 내 턴엔 양의 점수를
    else:
        return -eval  # 상대 턴엔 음의 
    
# 말의 위치에 따른 점수표

pawntable = [
 0,  0,  0,  0,  0,  0,  0,  0,
 5, 10, 10,-20,-20, 10, 10,  5,
 5, -5,-10,  0,  0,-10, -5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
50, 50, 50, 50, 50, 50, 50, 50,
 0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  5,  5,  0,-20,-40,
-30,  5, 10, 15, 15, 10,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 10, 15, 15, 10,  0,-30,
-40,-20,  0,  0,  0,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

bishopstable = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  5,  0,  0,  0,  0,  5,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

rookstable = [
  0,  0,  0,  5,  5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, 10, 10, 10, 10, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

queenstable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  5,  5,  5,  5,  5,  0,-10,
  0,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

kingstable = [
 20, 30, 10,  0,  0, 10, 30, 20,
 20, 20,  0,  0,  0,  0, 20, 20,
-10,-20,-20,-20,-20,-20,-20,-10,
-20,-30,-30,-40,-40,-30,-30,-20,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30]

def alphabeta( alpha, beta, depthleft ):  # 알파, 베타, depth = 몇 번 실험해볼지
    bestscore = -9999
    if( depthleft == 0 ): 
        return quiesce( alpha, beta )
    for move in board.legal_moves: # 가능한 움직임들 중에서
        board.push(move)   # 하나의 움직임 실행
        score = -alphabeta( -beta, -alpha, depthleft - 1 ) # depth 하나 줄이고 -알파베타가 score
        board.pop() # 움직임 실행 전 상태로 복귀
        if( score >= beta ): 
            return score
        if( score > bestscore ):
            bestscore = score
        if( score > alpha ):
            alpha = score   
    return bestscore # 최고 score를 리턴

def quiesce( alpha, beta ):
    stand_pat = evaluate_board() # 현재 보드판의 점수
    if( stand_pat >= beta ):
        return beta
    if( alpha < stand_pat ):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)        
            score = -quiesce( -beta, -alpha )
            board.pop()

            if( score >= beta ):
                return beta
            if( score > alpha ):
                alpha = score  
    return alpha

def selectmove(depth):
    bestMove = chess.Move.null()
    bestValue = -99999
    alpha = -100000
    beta = 100000
    for move in board.legal_moves: # 가능한 움직임들중에
        board.push(move) # 하나의 움직임을 택했을 때
        boardValue = -alphabeta(-beta, -alpha, depth-1) # depth를 하나 줄이고 -알파베타 값을 가져온다
        if boardValue > bestValue:
            bestValue = boardValue;
            bestMove = move  # 그 값이 가장 크면 그 움직임을 택한다
        if( boardValue > alpha ):
            alpha = boardValue # 매 반복마다 alpha값은 boardValue 값으로
        board.pop() # 하나의 움직임을 하기 전의 상태로 다시 돌아가서 테스트
    movehistory.append(bestMove)
    return bestMove


# In[4]:


board = chess.Board()
movehistory = []

while (not board.is_checkmate() and not board.is_stalemate() and not board.is_insufficient_material() and not board.is_seventyfive_moves() and not board.is_fivefold_repetition() and not board.is_fifty_moves()):
    if(board.turn):
        print("turn: MCTS")
        root = node()
        condition = board.is_game_over() or board.can_claim_draw()
        mov = mcts_pred(root, condition, board.turn, 1)
        board.push(mov)
        
    else:
        print("turn: MMAB")
        mov = selectmove(1)
        board.push(mov)
    print(mov)
    print('a b c d e f g h')
    print('---------------')
    print(board)
    print()
    
print(chess.Board.outcome(board))
if board.is_fifty_moves():
    print("fifty moves")


# In[ ]:




