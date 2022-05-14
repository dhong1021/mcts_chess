import chess
import random


def random_moves(tokenlist):
    return tokenlist[random.randrange(0,len(tokenlist))]
    
def eval_moves(self, tokenlist):
    max_val = 0
    max_move = tokenlist[0]
    if tokenlist is None:
        return max_move
    for token in tokenlist:
        val = 0
        if token[-1] == '#':    #체크메이트는 항상 1순위
            return token
        
        curr_piece = token[0]
        move = chess.Board.parse_san(self, token)
        if self.is_capture(move):
            split_move = token.split('x')    #이동할 위치
            move_to = split_move[1][0:2]
            try:
                captured_piece = chess.piece_name(self.piece_type_at(chess.parse_square(move_to)))    #그 위치에 있는 기물
            except TypeError:
                break
            val += piece_value[captured_piece]    #잡을 기물 점수
        else:
            if curr_piece.isupper():    #KQBNR
                if token[-1] == '+':
                    move_to = token[-3:-1]
                else:
                    move_to = token[-2:]
            else:
                move_to = token[0:2]
        
        if self.turn:    #white
            if curr_piece == 'O':    #캐슬링
                val += 30
            else:
                sq_index = chess.parse_square(move_to)
                if curr_piece == 'K':
                    val += kingEvalWhite[sq_index]
                elif curr_piece == 'Q':
                    val += queenEval[sq_index]
                elif curr_piece == 'B':
                    val += bishopEvalWhite[sq_index]
                elif curr_piece == 'N':
                    val += knightEval[sq_index]
                elif curr_piece == 'R':
                    val += rookEvalWhite[sq_index]
                else:
                    val += pawnEvalWhite[sq_index]
        else:    #black
            if curr_piece == 'O':
                val += 30
            else:
                sq_index = chess.parse_square(move_to)
                if curr_piece == 'K':
                    val += kingEvalBlack[sq_index]
                elif curr_piece == 'Q':
                    val += queenEval[sq_index]
                elif curr_piece == 'B':
                    val += bishopEvalBlack[sq_index]
                elif curr_piece == 'N':
                    val += knightEval[sq_index]
                elif curr_piece == 'R':
                    val += rookEvalBlack[sq_index]
                else:
                    val += pawnEvalBlack[sq_index]
        
        if max_val <= val:
            max_val = val
            max_move = token
            
    return max_move
        
    
# 토큰리스트의 다음 무브가 몇 점을 얻는가?

#  흑인가 백인가? self.turn() --> true==white

#  기물을 잡는가(is_capture(board, move)==True)? 잡는다면 어떤?
#    capture한다면 chess.piece_name(board.piece_type_at(위치)) 가 'pawn' 'rook' 등으로 반환
#    K Q B N R + x + 도착위치 로 표기. 폰이 잡으면 기존 폰의 위치열에 따라. cxd3, Qxb7+

# 다음 무브에서 어떤 기물이 움직였는가? --> san의 첫글자가 대문자면 KQBNR, 소문자면 폰
#  위치는 어떻게 알아내는가? 특수한 상황 - 캐슬링, 앙파상, 승급?
#    일반: capture 여부에 따라 2~3번째 문자 또는 3~4번째 글자. 
#    캐슬링: o-o , o-o-o (위치 언급 없음. 알파벳 o)
#    앙파상: 별도 표기 없음. 일반적인 폰이 이동해 잡는 표기. axb6
#    승급: 위치 뒤에 =Q, =B, =N, =R (체크, 체크메이트와 동시 가능. h8=R, a1=Q+)
#    체크는 +, 체크메이트는 #


piece_value = {
    'pawn':100,
    'rook':500,
    'knight':320,
    'bishop':330,
    'queen':900,
    'king':20000
}

pawnEvalWhite = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]
pawnEvalBlack = list(reversed(pawnEvalWhite))

knightEval = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

bishopEvalWhite = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
bishopEvalBlack = list(reversed(bishopEvalWhite))

rookEvalWhite = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]
rookEvalBlack = list(reversed(rookEvalWhite))

queenEval = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

kingEvalWhite = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]
kingEvalBlack = list(reversed(kingEvalWhite))

kingEvalEndGameWhite = [
    50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30,  0,  0,  0,  0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10,  0,  0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]
kingEvalEndGameBlack = list(reversed(kingEvalEndGameWhite))
