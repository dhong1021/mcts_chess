import chess
import random
import time
from math import log,sqrt,e,inf, ceil

class node():
    def __init__(self):
        self.state = chess.Board()
        self.action = ''
        self.children = set()
        self.parent = None
        self.N = 0
        self.n = 0
        self.v = 0
        self.win = 0

def ucb1(curr_node):
    #ans = curr_node.v + 2 * (sqrt(log(curr_node.N + e + (10**-6))/(curr_node.n + (10**-10))))
    c = 0
    if curr_node.N == 0:
        c = 1
    ans = winrate(curr_node) + sqrt(2) * sqrt(log(curr_node.N + c + (10**-6)) / (curr_node.n + (10**-10)))
    return ans

def winrate(curr_node):
    if(curr_node.n == 0):
        return 1
    else:
        return curr_node.win / curr_node.n

def rollout(curr_node, first_roll, true_3gram):
    if(chess.Board.outcome(curr_node.state) != None):
        board = curr_node.state
        if(board.result()=='1-0'):
            return (1,curr_node)
        elif(board.result()=='0-1'):
            return (-1,curr_node)
        else:
            return (0.5,curr_node)
    
    all_moves = [curr_node.state.san(i) for i in list(curr_node.state.legal_moves)]
    epsgrd = random.randrange(10)
    if epsgrd > 3 and first_roll:
        if true_3gram:
            ngram_move = ngram_enhanced_3gram(curr_node)
        else:
            ngram_move = ngram_enhanced_2gram(curr_node)
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push(ngram_move)
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.children.add(child)
    else:
        for i in all_moves:
            tmp_state = chess.Board(curr_node.state.fen())
            tmp_state.push_san(i)
            child = node()
            child.state = tmp_state
            child.parent = curr_node
            curr_node.children.add(child)

    
    rnd_state = random.choice(list(curr_node.children))

    return rollout(rnd_state, False, False)

def ngram_enhanced_3gram(curr_node):
    '''
    현재 보드 상태에서 시작
    흑백흑 or 백흑백 1순2순3순의 모든 조합에 대해 is_capture() 값에 따라 가중치 부여 1순3순은 + 2순은 - 
    가중치가 최대인 조합일 때의 이동 반환
    '''
    base_board = chess.Board(curr_node.state.fen())
    base_score = 0
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


def ngram_enhanced_2gram(curr_node):
    base_board = chess.Board(curr_node.state.fen())
    base_score = 0
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
#이중시뮬
def extra_rollout(curr_node):
    sim_result = -inf
    next_child = None
    all_moves = [curr_node.state.san(i) for i in list(curr_node.state.legal_moves)]
    for i in all_moves:
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push_san(i)
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.children.add(child)
    ran_children = random.sample(list(curr_node.children), ceil(len(curr_node.children)/3))
    for child in ran_children:
        child.v += rollout(child, False, False)[0]
        if child.v >= sim_result:
            sim_result = child.v
            next_child = child
    if next_child == None:
        return rollout(curr_node, False, False)

    return (next_child.v, next_child)

def expand(curr_node,white):
    if(len(curr_node.children)==0):
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

        return(expand(sel_child,0))

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

        return expand(sel_child,1)

def rollback(curr_node,reward):
    while(curr_node.parent!=None):
        curr_node.n+=1
        curr_node.v+=reward
        curr_node.N+=1
        if (reward == 1):
            curr_node.win += 1
        curr_node = curr_node.parent
    return curr_node

def mcts_pred(curr_node,over,white,iterations=5):
    if(over != None):
        return -1
        
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
############ngram 온오프, 3그램true/2그램false 스위치################
            reward,state = rollout(ex_child, True, False)
            #reward,state = extra_rollout(ex_child)
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
############ngram 온오프, 3그램true/2그램false 스위치################
            #reward,state = rollout(ex_child, True, False)
            reward,state = extra_rollout(ex_child)
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

    

def mcts_pred_wo_ucb(curr_node,over,white,iterations=5):
    if(over != None):
        return -1
        
    while(iterations>0): 
        if(white):
            ex_child = expand(random.choice(list(curr_node.children)),0)
############ngram 온오프, 3그램true/2그램false 스위치################
            reward,state = rollout(ex_child, True, False)
            #reward,state = extra_rollout(ex_child)
            curr_node = rollback(state,reward)
            iterations-=1  
            
        else:
            ex_child = expand(random.choice(list(curr_node.children)),1)
############ngram 온오프, 3그램true/2그램false 스위치################
            reward,state = rollout(ex_child, False, False)
            #reward,state = extra_rollout(ex_child)
            curr_node = rollback(state,reward)
            iterations-=1
    if(white):  
        mx = -inf
        idx = -1
        selected_move = ''
        for child in (curr_node.children):
            tmp = child.v
            if(tmp>mx):
                mx = tmp
                selected_move = map_state_move[child]
        return selected_move
    else:
        mn = inf
        idx = -1
        selected_move = ''
        for child in (curr_node.children):
            tmp = child.v
            if(tmp<mn):
                mn = tmp
                selected_move = map_state_move[child]
        return selected_move


def evaluate_board(): 
    
    if board.is_checkmate():  
        if board.turn:
            return 9999  
        else:
            return -9999  
    if board.is_stalemate():  
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
    
    material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)  
    
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
        return -eval
    else:
        return eval  
    
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

def alphabeta( alpha, beta, depthleft ):  
    bestscore = -9999
    if( depthleft == 0 ): 
        return quiesce( alpha, beta )
    for move in board.legal_moves: 
        board.push(move)   
        score = -alphabeta( -beta, -alpha, depthleft - 1 )
        board.pop() 
        if( score >= beta ): 
            return score
        if( score > bestscore ):
            bestscore = score
        if( score > alpha ):
            alpha = score   
    return bestscore 

def quiesce( alpha, beta ):
    stand_pat = evaluate_board() 
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
    for move in board.legal_moves: 
        board.push(move) 
        boardValue = -alphabeta(-beta, -alpha, depth-1)
        if boardValue > bestValue:
            bestValue = boardValue;
            bestMove = move 
        if( boardValue > alpha ):
            alpha = boardValue 
        board.pop() 
    return bestMove

fp = open('result.txt','a')
white_avr_time = 0
black_avr_time = 0
count_turn = 0
for i in range(7):
    print("try count: ", i+1)
    board = chess.Board()
    while (chess.Board.outcome(board) is None):
        count_turn += 1
        if board.turn:    ####################################흑백바꾸는법: 이부분만 if not board.turn: 으로 변경
            time_white_begin = time.time()
            print('ucb, ngram=2')
            root = node()
            root.state = board
            all_moves = [root.state.san(i) for i in list(root.state.legal_moves)]
            map_state_move = dict()

            for i in all_moves:
                tmp_state = chess.Board(root.state.fen())
                tmp_state.push_san(i)
                child = node()
                child.state = tmp_state
                child.parent = root
                root.children.add(child)
                map_state_move[child] = i
#### UCB 여부에 따라 아래를 mcts_pred 또는 mcts_pred_wo_ucb 로 사용
            result = mcts_pred(root,chess.Board.outcome(board),board.turn, 5)
            board.push_san(result)
            time_white_end = time.time()
            time_white = time_white_end - time_white_begin
            white_avr_time += time_white
            
            print(result)
            print(board)
            print()
            print('this turn: ', time_white, '  avr time: ', white_avr_time / ceil(count_turn))
            print()
            
            
        else:
            time_black_begin = time.time()
            print('ucb, extra rollout')
            '''result = selectmove(3)
            board.push(result)'''
            root = node()
            root.state = board
            all_moves = [root.state.san(i) for i in list(root.state.legal_moves)]
            map_state_move = dict()

            for i in all_moves:
                tmp_state = chess.Board(root.state.fen())
                tmp_state.push_san(i)
                child = node()
                child.state = tmp_state
                child.parent = root
                root.children.add(child)
                map_state_move[child] = i
#### UCB 여부에 따라 아래를 mcts_pred 또는 mcts_pred_wo_ucb 로 사용
            result = mcts_pred(root,chess.Board.outcome(board),board.turn, 5)
            board.push_san(result)
            time_black_end = time.time()
            time_black = time_black_end - time_black_begin
            black_avr_time += time_black
            
            print(result)
            print(board)
            print()
            print('this turn: ', time_black, '  avr time: ', black_avr_time / ceil(count_turn/2))
            print()
            

    print(chess.Board.outcome(board))
    print('white avr: ', white_avr_time / ceil(count_turn/2), ' black avr: ', black_avr_time / ceil(count_turn/2))
    fp.write(str(chess.Board.outcome(board)))
    fp.write('\n')

fp.close()