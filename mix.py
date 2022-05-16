import chess
import random
from math import log, sqrt, e, inf

import chess.svg
from IPython.display import SVG
import chess.polyglot


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
    ans = curr_node.v+2 * \
        (sqrt(log(curr_node.N+e+(10**-6))/(curr_node.n+(10**-10))))
    return ans


def rollout(curr_node):
    if(curr_node.state.is_game_over()):  # 현재 노드에서 게임이 끝나면 (leaf 노드에 도달)
        board = curr_node.state
        if(board.result() == '1-0'):  # chess library result: 이기면 '1-0' 지면 '0-1' 비기면 '1/2-1/2'를 return
            return (1, curr_node)  # 이겼으면 +1
        elif(board.result() == '0-1'):
            return (-1, curr_node)  # 졌으면 -1
        else:
            return (0.5, curr_node)  # 비겼으면 +0.5

    all_moves = [move for move in list(
        curr_node.state.legal_moves)]  # 이동 가능한 모든 이동의 리스트

    for i in all_moves:
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push(i)  # 현재 보드에서 가능한 이동을 하나씩 해봄
        child = node()  # 자식 노드를 하나 만들고
        child.state = tmp_state
        child.parent = curr_node  # 현재 노드가 부모가 됨
        curr_node.children.add(child)  # 현재 노드에 모든 이동들이 자식 노드로 추가됨
    rnd_state = random.choice(list(curr_node.children))  # 자식들 중 랜덤 선택

    return rollout(rnd_state)


def expand(curr_node, white):  # white = 1
    if(len(curr_node.children) == 0):  # 자식 없음 = leaf 노드에 도달
        return curr_node

    max_ucb = -inf
    if(white):
        idx = -1
        max_ucb = -inf
        sel_child = None
        for i in curr_node.children:
            tmp = ucb1(i)
            if(tmp > max_ucb):
                idx = i
                max_ucb = tmp
                sel_child = i
        # white턴에는 max_ucb를 가진 자식을 다음 노드로 선택하고 expand
        return(expand(sel_child, 0))

    else:
        idx = -1
        min_ucb = inf
        sel_child = None
        for i in curr_node.children:
            tmp = ucb1(i)
            if(tmp < min_ucb):
                idx = i
                min_ucb = tmp
                sel_child = i
        # black턴에는 min_ucb를 가진 자식을 다음 노드로 선택하고 expand
        return expand(sel_child, 1)


def rollback(curr_node, reward):
    curr_node.n += 1  # 노드의 방문수 1 증가
    curr_node.v += reward  # 노드의 승점을 reward만큼 증가 (이기면 +1, 지면 -1, 비기면 +0.5)
    while(curr_node.parent != None):  # 부모가 있으면 (root 노드에 갈 때 까지)
        curr_node.N += 1  # 부모 노드의 방문수 1증가
        curr_node = curr_node.parent  # 현재 노드를 부모 노드로 바꾸면서 한단계씩 윗노드로 올라감
    return curr_node


def mcts_pred(curr_node, over, white, iterations=10):  # 반복횟수 설정 iterations
    if(over):  # board.is_game_over()
        return -1

    all_moves = [move for move in list(
        curr_node.state.legal_moves)]  # 가능한 모든 이동 리스트
    map_state_move = dict()

    for i in all_moves:
        tmp_state = chess.Board(curr_node.state.fen())
        tmp_state.push(i)
        child = node()
        child.state = tmp_state
        child.parent = curr_node
        curr_node.children.add(child)
        map_state_move[child] = i

    while(iterations > 0):
        if(white):
            idx = -1
            max_ucb = -inf
            sel_child = None
            for i in curr_node.children:
                tmp = ucb1(i)
                if(tmp > max_ucb):
                    idx = i
                    max_ucb = tmp
                    sel_child = i
            ex_child = expand(sel_child, 0)
            reward, state = rollout(ex_child)
            curr_node = rollback(state, reward)
            iterations -= 1  # expand -> rollout -> rollback -> iteration -= 1

        else:
            idx = -1
            min_ucb = inf
            sel_child = None
            for i in curr_node.children:
                tmp = ucb1(i)
                if(tmp < min_ucb):
                    idx = i
                    min_ucb = tmp
                    sel_child = i
            ex_child = expand(sel_child, 1)
            reward, state = rollout(ex_child)
            curr_node = rollback(state, reward)
            iterations -= 1

    if(white):
        mx = -inf
        idx = -1
        selected_move = ''
        for i in (curr_node.children):
            tmp = ucb1(i)
            if(tmp > mx):
                mx = tmp
                selected_move = map_state_move[i]
        return selected_move

    else:
        mn = inf
        idx = -1
        selected_move = ''
        for i in (curr_node.children):
            tmp = ucb1(i)
            if(tmp < mn):
                mn = tmp
                selected_move = map_state_move[i]
        return selected_move

# MMAB 구간


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

    material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500 * \
        (wr-br)+900*(wq-bq)  # 각각의 가중치 x (white-black)개수

    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                          for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i]
                   for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i]
                   for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                              for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i]
                 for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i]
                  for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                             for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i]
                 for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.KING, chess.BLACK)])

    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval  # 내 턴엔 양의 점수를
    else:
        return -eval  # 상대 턴엔 음의 점수를

# 말의 위치에 따른 점수표


pawntable = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,  5,  5,  0, -20, -40,
    -30,  5, 10, 15, 15, 10,  5, -30,
    -30,  0, 15, 20, 20, 15,  0, -30,
    -30,  5, 15, 20, 20, 15,  5, -30,
    -30,  0, 10, 15, 15, 10,  0, -30,
    -40, -20,  0,  0,  0,  0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,  5,  0,  0,  0,  0,  5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10,  0, 10, 10, 10, 10,  0, -10,
    -10,  5,  5, 10, 10,  5,  5, -10,
    -10,  0,  5, 10, 10,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

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
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -10,  5,  5,  5,  5,  5,  0, -10,
    0,  0,  5,  5,  5,  5,  0, -5,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


def alphabeta(alpha, beta, depthleft):  # 알파, 베타, depth = 몇 번 실험해볼지
    bestscore = -9999
    if(depthleft == 0):
        return quiesce(alpha, beta)
    for move in board.legal_moves:  # 가능한 움직임들 중에서
        board.push(move)   # 하나의 움직임 실행
        # depth 하나 줄이고 -알파베타가 score
        score = -alphabeta(-beta, -alpha, depthleft - 1)
        board.pop()  # 움직임 실행 전 상태로 복귀
        if(score >= beta):
            return score
        if(score > bestscore):
            bestscore = score
        if(score > alpha):
            alpha = score
    return bestscore  # 최고 score를 리턴


def quiesce(alpha, beta):
    stand_pat = evaluate_board()  # 현재 보드판의 점수
    if(stand_pat >= beta):
        return beta
    if(alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha)
            board.pop()

            if(score >= beta):
                return beta
            if(score > alpha):
                alpha = score
    return alpha


def selectmove(depth):
    try:
        move = chess.polyglot.MemoryMappedReader(
            "bookfish.bin").weighted_choice(board).move()
        movehistory.append(move)
        return move
    except:
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:  # 가능한 움직임들중에
            board.push(move)  # 하나의 움직임을 택했을 때
            # depth를 하나 줄이고 -알파베타 값을 가져온다
            boardValue = -alphabeta(-beta, -alpha, depth-1)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move  # 그 값이 가장 크면 그 움직임을 택한다
            if(boardValue > alpha):
                alpha = boardValue  # 매 반복마다 alpha값은 boardValue 값으로
            board.pop()  # 하나의 움직임을 하기 전의 상태로 다시 돌아가서 테스트
        movehistory.append(bestMove)
        return bestMove


board = chess.Board()
SVG(chess.svg.board(board=board, size=400))

checkmate = 0
stalemate = 0
insufficient_material = 0
game_play = 1

for i in range(game_play):
    while (not board.is_checkmate() and not board.is_stalemate() and not board.is_insufficient_material()):
        root = node()
        white = 1
        mov = mcts_pred(root, board.is_game_over(), white)
        board.push(mov)
        SVG(chess.svg.board(board=board, size=400))

        movehistory = []
        mov2 = selectmove(3)
        board.push(mov2)
        SVG(chess.svg.board(board=board, size=400))

    if (board.is_checkmate()):
        checkmate += 1
    elif (board.is_stalemate()):
        stalemate += 1
    else:
        insufficient_material += 1

    board.reset_board()
    movehistory = []


print("c = ", checkmate, ", s = ", stalemate, ", i = ", insufficient_material)
