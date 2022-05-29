import chess
import random
import mmab_chess
import time

board = chess.Board()

class node():
    def __init__(self):
        self.state = board  # state = 보드의 상태
        self.action = ''
        self.children = set()
        self.parent = None
        self.N = 0  # Number of times parent node has been visited
        self.n = 0  # number of times child node has been visited
        self.v = 0  # winning score of current node

################################################################################################################

def rollout(curr_node):
    if(curr_node.state.is_game_over() or curr_node.state.can_claim_draw()): # 현재 노드에서 게임이 끝나면 (leaf 노드에 도달)
        ro_board = curr_node.state
        if(ro_board.result()=='1-0'): # chess library result: 이기면 '1-0' 지면 '0-1' 비기면 '1/2-1/2'를 return
            run_rollback = rollback(curr_node, 1)
            return (1,curr_node) # 이겼으면 +1
        elif(ro_board.result()=='0-1'):
            run_rollback = rollback(curr_node, -1)
            return (-1,curr_node) # 졌으면 -1
        else:
            run_rollback = rollback(curr_node, 0.5)
            return (0.5,curr_node) # 비겼으면 +0.5
    
    all_moves = [move for move in list(curr_node.state.legal_moves)] # 이동 가능한 모든 이동의 리스트
    temp_fen = curr_node.state.fen()
    for i in all_moves:
        tmp_state = chess.Board(temp_fen)
        tmp_state.push(i) # 현재 보드에서 가능한 이동을 하나씩 해봄
        child = node() # 자식 노드를 하나 만들고
        child.state = tmp_state
        child.parent = curr_node # 현재 노드가 부모가 됨
        curr_node.children.add(child) # 현재 노드에 모든 이동들이 자식 노드로 추가됨
    temp_kid = random.choice(list(curr_node.children)) # 자식들 중 랜덤 선택
    
    rollout_states = [kid for kid in list(curr_node.children)] # 현재 노드의 자식들
    
    
    for i in rollout_states:
        continue
        
        
        
    return rollout(temp_kid)


################################################################################################################

def expand(curr_node,white): # white = 1
    if(len(curr_node.children)==0): # 자식 없음 = leaf 노드에 도달
        return curr_node
    temp_reward = 0
    max_child = None
    for i in list(curr_node.children):
        if temp_reward <= i.v:
            temp_reward = i.v
            max_child = i
    if max_child is None:
        max_child = random.choice(list(curr_node.children))
    if(white):
        #return expand(random.choice(list(curr_node.children)),0) # white턴에는 max_ucb를 가진 자식을 다음 노드로 선택하고 expand
        return expand(max_child, 0)
    else:
        #return expand(random.choice(list(curr_node.children)),1) # black턴에는 min_ucb를 가진 자식을 다음 노드로 선택하고 expand
        return expand(max_child, 1)

################################################################################################################

def rollback(curr_node,reward):
    curr_node.n+=1  # 노드의 방문수 1 증가
    curr_node.v+=reward  # 노드의 승점을 reward만큼 증가 (이기면 +1, 지면 -1, 비기면 +0.5)
    while(curr_node.parent != None): # 부모가 있으면 (root 노드에 갈 때 까지)
        curr_node.N+=1 # 부모 노드의 방문수 1증가
        curr_node = curr_node.parent # 현재 노드를 부모 노드로 바꾸면서 한단계씩 윗노드로 올라감
        curr_node.v += reward
    return curr_node

################################################################################################################

def mcts_pred(curr_node,over,white,iterations=3): # 반복횟수 설정 iterations
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
    reward_prev = float('-inf')
    while(iterations>0):
        if(white):
            ex_child = expand(random.choice(list(curr_node.children)),0)
            reward,state = rollout(ex_child)
            if (reward_prev <= reward):
                reward_prev = reward
                curr_node = rollback(state,reward)
            iterations-=1  # expand -> rollout -> rollback -> iteration -= 1  
        else:
            ex_child = expand(random.choice(list(curr_node.children)),1)
            reward,state = rollout(ex_child)
            if (reward_prev <= reward):
                reward_prev = reward
                curr_node = rollback(state,reward)
            iterations-=1
    temp_reward = 0
    max_child = None
    for i in list(curr_node.children):
        if temp_reward <= i.v:
            temp_reward = i.v
            max_child = i
    if max_child is None:
        selected_move = map_state_move[random.choice(list(curr_node.children))]
    else:
        selected_move = map_state_move[max_child]
    print(temp_reward)
    return selected_move

################################################################################################################

#board = chess.Board()
start_time = time.time()
while (not board.is_checkmate() and not board.is_stalemate() and not board.is_insufficient_material() and not board.is_seventyfive_moves() and not board.is_fivefold_repetition() and not board.is_fifty_moves()):
    if(board.turn):
        print("turn: MCTS")
        root = node()
        condition = board.is_game_over() or board.can_claim_draw()
        mov = mcts_pred(root, condition, board.turn)
        board.push(mov)

    else:
        print("turn: MMAB")
        mov = mmab_chess.selectmove(board, 2)
        '''print("turn: MCTS black")
        root = node()
        condition = board.is_game_over() or board.can_claim_draw()
        mov = mcts_pred(root, condition, board.turn)'''
        board.push(mov)
    print(board)
    print()

print(chess.Board.outcome(board))
if board.is_fifty_moves():
    print("fifty moves")
end_time = time.time()
print(end_time - start_time, ' sec')