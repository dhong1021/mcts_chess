import chess
import random
from math import e, inf, log, sqrt

board = chess.Board()


class node():
    def __init__(self):
        self.state = board
        self.action = ''
        self.children = set()
        self.parent = None
        self.t = 0
        self.n = 0
        self.v = 0


def ucb(cur_node):
    value = cur_node.v + 2 * (sqrt(log(cur_node.t + e + (10 ** -6)) / (cur_node.n + (10 ** -10))))
    return value


def rollout(cur_node):
    if (cur_node.state.is_game_over() or cur_node.state.can_claim_draw()):  # 현재 노드에서 게임이 끝나면 (leaf 노드에 도달)
        board = cur_node.state
        if (board.result() == '1-0'):  # chess library result: 이기면 '1-0' 지면 '0-1' 비기면 '1/2-1/2'를 return
            return (1, cur_node)  # 이겼으면 +1
        elif (board.result() == '0-1'):
            return (-1, cur_node)  # 졌으면 -1
        else:
            return (0.5, cur_node)  # 비겼으면 +0.5

    for i in list(cur_node.state.legal_moves):
        temp_state = chess.Board(cur_node.state.fen())
        temp_state.push(i)  # 현재 보드에서 가능한 이동을 하나씩 해봄
        child = node()  # 자식 노드를 하나 만들고
        child.state = temp_state
        child.parent = cur_node  # 현재 노드가 부모가 됨
        cur_node.children.add(child)  # 현재 노드에 모든 이동들이 자식 노드로 추가됨
    # random_state = random.choice(list(cur_node.children)) # 자식들 중 랜덤 선택
    # return rollout(random_state)

    win = -1
    temp_node = node()
    # print(cur_node.children)
    reward = 0
    for i in list(cur_node.children):
        if (i.state.is_game_over() or i.state.can_claim_draw()):  # 현재 노드에서 게임이 끝나면 (leaf 노드에 도달)
            ro_board = i.state
            if (ro_board.result() == '1-0'):  # chess library result: 이기면 '1-0' 지면 '0-1' 비기면 '1/2-1/2'를 return
                reward = 1  # 이겼으면 +1
            elif (ro_board.result() == '0-1'):
                reward = -1  # 졌으면 -1
            else:
                reward = 0.5  # 비겼으면 +0.5
        # i.n += 1  # 노드의 방문수 1 증가
        i.v += reward  # 노드의 승점을 reward만큼 증가 (이기면 +1, 지면 -1, 비기면 +0.5)
        if win < i.v:  # 최대 승점인 노드보다 현재 노드의 승점이 크면
            win = i.v  # 최대 노드의 승점 갱신
            temp_node = i
            i.v -= reward  # 임시로 증가시킨 노드의 승점을 다시 원래대로
    # print(temp_node)
    return rollout(temp_node)


def expand(cur_node, white):  # white = 1
    if (len(cur_node.children) == 0):  # 자식 없음 = leaf 노드에 도달
        return cur_node

    maxucb = -inf
    if (white):
        index = -1
        maxucb = -inf
        ucb_child = None
        for i in cur_node.children:
            temp = ucb(i)
            if (temp > maxucb):
                index = i
                maxucb = temp
                ucb_child = i
        return (expand(ucb_child, 0))  # white턴에는 max_ucb를 가진 자식을 다음 노드로 선택하고 expand

    else:
        index = -1
        minucb = inf
        ucb_child = None
        for i in cur_node.children:
            temp = ucb(i)
            if (temp < minucb):
                index = i
                minucb = temp
                ucb_child = i
        return expand(ucb_child, 1)  # black턴에는 min_ucb를 가진 자식을 다음 노드로 선택하고 expand


def rollback(cur_node, reward):
    cur_node.n += 1  # 노드의 방문수 1 증가
    cur_node.v += reward  # 노드의 승점을 reward만큼 증가 (이기면 +1, 지면 -1, 비기면 +0.5)
    while (cur_node.parent != None):  # 부모가 있으면 (root 노드에 갈 때 까지)
        cur_node.t += 1  # 부모 노드의 방문수 1증가
        cur_node = cur_node.parent  # 현재 노드를 부모 노드로 바꾸면서 한단계씩 윗노드로 올라감
    return cur_node


def mcts(cur_node, over, white, iterations=10):
    if (over):  # board.is_game_over()
        return -1

    state_moves = dict()

    for i in list(cur_node.state.legal_moves):
        temp_state = chess.Board(cur_node.state.fen())
        temp_state.push(i)
        child = node()
        child.state = temp_state
        child.parent = cur_node
        cur_node.children.add(child)
        state_moves[child] = i

    while (iterations > 0):
        if (white):
            index = -1
            maxucb = -inf
            ucb_child = None
            for i in cur_node.children:
                temp = ucb(i)
                if (temp > maxucb):
                    index = i
                    maxucb = temp
                    ucb_child = i
            ex_child = expand(ucb_child, 0)
            reward, state = rollout(ex_child)
            curr_node = rollback(state, reward)
            iterations -= 1  # expand -> rollout -> rollback -> iteration -= 1

        else:
            index = -1
            minucb = inf
            ucb_child = None
            for i in cur_node.children:
                temp = ucb(i)
                if (temp < minucb):
                    index = i
                    minucb = temp
                    ucb_child = i
            ex_child = expand(ucb_child, 1)
            reward, state = rollout(ex_child)
            curr_node = rollback(state, reward)
            iterations -= 1

    if (white):
        maxucb_2 = -inf
        index = -1
        selected_move = ''
        for i in (cur_node.children):
            temp = ucb(i)
            if (temp > maxucb_2):
                maxucb_2 = temp
                selected_move = state_moves[i]
        return selected_move

    else:
        minucb_2 = inf
        index = -1
        selected_move = ''
        for i in (cur_node.children):
            temp = ucb(i)
            if (temp < minucb_2):
                minucb_2 = temp
                selected_move = state_moves[i]
        return selected_move


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

    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (
                wq - bq)  # 각각의 가중치 x (white-black)개수

    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                           for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
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

    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval  # 내 턴엔 양의 점수를
    else:
        return -eval  # 상대 턴엔 음의


# 말의 위치에 따른 점수표

pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


def alphabeta(alpha, beta, depthleft):  # 알파, 베타, depth = 몇 번 실험해볼지
    bestscore = -9999
    if (depthleft == 0):
        return quiesce(alpha, beta)
    for move in board.legal_moves:  # 가능한 움직임들 중에서
        board.push(move)  # 하나의 움직임 실행
        score = -alphabeta(-beta, -alpha, depthleft - 1)  # depth 하나 줄이고 -알파베타가 score
        board.pop()  # 움직임 실행 전 상태로 복귀
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore  # 최고 score를 리턴


def quiesce(alpha, beta):
    stand_pat = evaluate_board()  # 현재 보드판의 점수
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha)
            board.pop()

            if (score >= beta):
                return beta
            if (score > alpha):
                alpha = score
    return alpha


import chess.polyglot


def selectmove(depth):
    bestMove = chess.Move.null()
    bestValue = -99999
    alpha = -100000
    beta = 100000
    for move in board.legal_moves:  # 가능한 움직임들중에
        board.push(move)  # 하나의 움직임을 택했을 때
        boardValue = -alphabeta(-beta, -alpha, depth - 1)  # depth를 하나 줄이고 -알파베타 값을 가져온다
        if boardValue > bestValue:
            bestValue = boardValue;
            bestMove = move  # 그 값이 가장 크면 그 움직임을 택한다
        if (boardValue > alpha):
            alpha = boardValue  # 매 반복마다 alpha값은 boardValue 값으로
        board.pop()  # 하나의 움직임을 하기 전의 상태로 다시 돌아가서 테스트
    movehistory.append(bestMove)
    return bestMove


while (
        not board.is_checkmate() and not board.is_stalemate() and not board.is_insufficient_material() and not board.is_seventyfive_moves() and not board.is_fivefold_repetition() and not board.is_fifty_moves()):
    if (board.turn):
        print("turn: MCTS with UCB")
        root = node()
        condition = board.is_game_over() or board.can_claim_draw()
        mov = mcts(root, condition, board.turn, 1)
        board.push(mov)

    else:
        print("turn: MMAB")
        movehistory = []
        mov = selectmove(3)
        board.push(mov)
    print(mov)
    print('a b c d e f g h')
    print('---------------')
    print(board)
    print()

print(chess.Board.outcome(board))
if board.is_fifty_moves():
    print("fifty moves")