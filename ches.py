import chess
import random
import select_move

def token_moves(self):
    legal_moves_str = str(self.legal_moves)
    legal_moves_str = legal_moves_str[legal_moves_str.find('(')+1:-2]
    legal_moves_tokens = legal_moves_str.split(', ')
    return legal_moves_tokens


board = chess.Board()

game_play = 10
winner = ['winner : black', 'winner : white']

for i in range(game_play):
    board.clear()
    board.reset()
    k = 0
    while (not board.is_checkmate() and not board.is_stalemate() and not board.is_insufficient_material() and not board.is_seventyfive_moves() and not board.is_fivefold_repetition() and not board.is_fifty_moves()):
        if k%2 == 0:
            temp = select_move.random_moves(token_moves(board))
            board.push_san(temp)
        else:
            temp = select_move.eval_moves(board, token_moves(board))
            board.push_san(temp)
        k += 1
    print(board)
    print(chess.Board.outcome(board))
    if board.is_fifty_moves():
        print("fifty moves")