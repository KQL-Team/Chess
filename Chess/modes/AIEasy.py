import numpy as np
import copy

piece_values = {
    'P': 10,
    'R': 50,
    'H': 30,
    'B': 30,
    'Q': 90,
    'K': 1000
}

class AIEasy():
    def __init__(self, game, depth=3):
        self.game = game
        self.depth = depth

    def evaluate_board(self, board):
        evaluation = 0
        for x in range(8):
            for y in range(8):
                piece = board[x][y]
                if piece != '':
                    value = piece_values.get(piece[1], 0)
                    if piece[0] == 'b':
                        evaluation += value
                    else:
                        evaluation -= value
        return evaluation

    def alpha_beta(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.end_game()[0]:
            return self.evaluate_board(game.board), None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for src, dest in self.get_all_moves(game, 'b'):
                temp_game = copy.deepcopy(game)
                temp_game.move(src, dest)
                eval = self.alpha_beta(temp_game, depth - 1, alpha, beta, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (src, dest)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for src, dest in self.get_all_moves(game, 'w'):
                temp_game = copy.deepcopy(game)
                temp_game.move(src, dest)
                eval = self.alpha_beta(temp_game, depth - 1, alpha, beta, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (src, dest)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_all_moves(self, game, player):
        all_moves = []
        for x in range(8):
            for y in range(8):
                piece = game.board[x][y]
                if piece != '' and piece[0] == player:
                    for row in range(8):
                        for col in range(8):
                            if not game.restrict((x, y), (row, col)) and not game.move_leads_to_check((x, y), (row, col)):
                                all_moves.append(((x, y), (row, col)))
        return all_moves

    def select_best_move(self):
        _, best_move = self.alpha_beta(self.game, self.depth, float('-inf'), float('inf'), True)
        return best_move
