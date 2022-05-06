import chess
import random

def token_moves(self):
    legal_moves_str = str(self.legal_moves)
    legal_moves_str = legal_moves_str[legal_moves_str.find('(')+1:-2]
    legal_moves_tokens = legal_moves_str.split(', ')
    return legal_moves_tokens

def select_moves(tokenlist):
    return tokenlist[random.randrange(0,len(tokenlist))]
    
    

board = chess.Board()

checkmate = 0
stalemate = 0
insufficient_material = 0
game_play = 3

for i in range(game_play):
    while (not board.is_checkmate() and not board.is_stalemate() and not board.is_insufficient_material()):
        temp = select_moves(token_moves(board))
        board.push_san(temp)

    if (board.is_checkmate()):
        checkmate += 1
    elif (board.is_stalemate()):
        stalemate += 1
    else:
        insufficient_material += 1
    board.reset_board()

print("c = ", checkmate, ", s = ", stalemate, ", i = ", insufficient_material)