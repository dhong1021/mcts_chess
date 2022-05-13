import board, pieces, numpy
from montecarlotreesearch import MonteCarloTreeSearch

class MCTS:

    INFINITE = 10000000
    
    def partial_mcts(number_of_simulation, game_state):
        return MonteCarloTreeSearch.get_best_move(game_state, number_of_simulation)

    @staticmethod
    def get_MCTS_move(chessboard, invalid_moves):
        best_move = partial_mcts(100, board)
        best_score = MCTS.INFINITE
        for move in chessboard.get_possible_moves(pieces.Piece.WHITE):
            if (MCTS.is_invalid_move(move, invalid_moves)):
                continue

            copy = board.Board.clone(chessboard)
            copy.perform_move(move)

            score = MCTS.alphabeta(copy, 2, -MCTS.INFINITE, MCTS.INFINITE, True)
            if (score < best_score):
                best_score = score
                best_move = move

        # Checkmate.
        if (best_move == 0):
            return 0

        copy = board.Board.clone(chessboard)
        copy.perform_move(best_move)
        if (copy.is_check(pieces.Piece.WHITE)):
            invalid_moves.append(best_move)
            return MCTS.get_MCTS_move(chessboard, invalid_moves)

        return best_move
