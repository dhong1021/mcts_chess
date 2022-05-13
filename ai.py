import board, pieces, numpy
from collections import defaultdict

class Heuristics:

    # The tables denote the points scored for the position of the chess pieces on the board.

    PAWN_TABLE = numpy.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    KNIGHT_TABLE = numpy.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  15,  20,  20,  15,   0, -30],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    BISHOP_TABLE = numpy.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

    ROOK_TABLE = numpy.array([
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    QUEEN_TABLE = numpy.array([
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,   0,   5,  0,  0,   0,   0, -10],
        [-10,   5,   5,  5,  5,   5,   0, -10],
        [  0,   0,   5,  5,  5,   5,   0,  -5],
        [ -5,   0,   5,  5,  5,   5,   0,  -5],
        [-10,   0,   5,  5,  5,   5,   0, -10],
        [-10,   0,   0,  0,  0,   0,   0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ])

    @staticmethod
    def evaluate(board):
        material = Heuristics.get_material_score(board)

        pawns = Heuristics.get_piece_position_score(board, pieces.Pawn.PIECE_TYPE, Heuristics.PAWN_TABLE)
        knights = Heuristics.get_piece_position_score(board, pieces.Knight.PIECE_TYPE, Heuristics.KNIGHT_TABLE)
        bishops = Heuristics.get_piece_position_score(board, pieces.Bishop.PIECE_TYPE, Heuristics.BISHOP_TABLE)
        rooks = Heuristics.get_piece_position_score(board, pieces.Rook.PIECE_TYPE, Heuristics.ROOK_TABLE)
        queens = Heuristics.get_piece_position_score(board, pieces.Queen.PIECE_TYPE, Heuristics.QUEEN_TABLE)

        return material + pawns + knights + bishops + rooks + queens

    # Returns the score for the position of the given type of piece.
    # A piece type can for example be: pieces.Pawn.PIECE_TYPE.
    # The table is the 2d numpy array used for the scoring. Example: Heuristics.PAWN_TABLE
    @staticmethod
    def get_piece_position_score(board, piece_type, table):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
                if (piece != 0):
                    if (piece.piece_type == piece_type):
                        if (piece.color == pieces.Piece.WHITE):
                            white += table[x][y]
                        else:
                            black += table[7 - x][y]

        return white - black

    @staticmethod
    def get_material_score(board):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
                if (piece != 0):
                    if (piece.color == pieces.Piece.WHITE):
                        white += piece.value
                    else:
                        black += piece.value

        return white - black


class AI:

    INFINITE = 10000000

    @staticmethod
    def is_invalid_move(move, invalid_moves):
        for invalid_move in invalid_moves:
            if (invalid_move.equals(move)):
                return True
        return False

class MonteCarloTreeSearchNode():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        self._untried_actions = self.state.get_possible_moves(pieces.Piece.BLACK)
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):	
        action = self._untried_actions.pop()
        next_state = self.state.perform_move(action)
        child_node = MonteCarloTreeSearchNode(
                    next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_check(pieces.Piece.BLACK)

    def rollout(self):
        current_rollout_state = self.state
    
        while not current_rollout_state.is_check(pieces.Piece.BLACK):
        
            possible_moves = current_rollout_state.get_possible_moves(pieces.Piece.BLACK)
        
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.perform_move(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
        
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100
	
        for i in range(simulation_no):
		
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
	
        return self.best_child(c_param=0.)

    def game_result(self):
        current_state = self.state

        if evaluate(current_state) >= 0:
            return -1
        else:
            return 1

    def main(self):
        root = MonteCarloTreeSearchNode(self)
        selected_node = root.best_action()
        return selected_node

class Move:

    def __init__(self, xfrom, yfrom, xto, yto, castling_move):
        self.xfrom = xfrom
        self.yfrom = yfrom
        self.xto = xto
        self.yto = yto
        self.castling_move = castling_move

    # Returns true iff (xfrom,yfrom) and (xto,yto) are the same.
    def equals(self, other_move):
        return self.xfrom == other_move.xfrom and self.yfrom == other_move.yfrom and self.xto == other_move.xto and self.yto == other_move.yto

    def to_string(self):
        return "(" + str(self.xfrom) + ", " + str(self.yfrom) + ") -> (" + str(self.xto) + ", " + str(self.yto) + ")"
