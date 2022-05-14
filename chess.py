import chess
import math
import random
import sys
import time



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


def randomPiece():
    while True:
        random_alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        random_choice = []
        for _ in range(2):
            x = random.choice(random_alpha)
            y = random.randrange(1, 9, 1)
            random_choice.append(str(x) + str(y))

        enter_move = random_choice[0] + random_choice[1]
        
        if random_choice[0] == random_choice[1]:  #'d7d7'처럼 똑같은 경우 0000으로 입력해야 함
            continue
        else:
            pass
        if (chess.Move.from_uci(enter_move) in board.legal_moves) is False:   #이동할 수 없는 위치로 이동시킬 경우
            continue
        else:
            break
    return enter_move

def main():
    global board
    board = chess.Board()
    n = 0
    print(board)
    while n < 100:
        if n%2 == 0:
            print("Random Turn:")
            move = randomPiece()
            move = chess.Move.from_uci(str(move))
            board.push(move)
            time.sleep(1)
            print("\n")
        else:
            print("MMAB Turn:")
            move = minimaxRoot(3,board,True)
            move = chess.Move.from_uci(str(move))
            board.push(move)
            time.sleep(1)
            print("\n")
        print(board)
        n += 1

if __name__ == "__main__":
    main()
    
    
    
    
board.is_stalemate()  #교착 상태

board.is_insufficient_material()   #기물 부족(양 쪽의 킹만 남거나, 킹 + 비숍, 킹 + 나이트.)

board.outcome()   #결과
