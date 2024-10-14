pawnPoint = [
    [900, 900, 900, 900, 900, 900, 900, 900],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

knightPoint = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

bishopPoint = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

rockPoint = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]
]

queenPoint = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]

kingMidPoint = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]
]

kingEndPoint = [
    [-50, -40, -30, -20, -20, -30, -40, -50],
    [-30, -20, -10, 0, 0, -10, -20, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -30, 0, 0, 0, 0, -30, -30],
    [-50, -30, -30, -30, -30, -30, -30, -50]
]
dict1 = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g':6, 'h':7,
    '1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0
}
import pandas as pd
import numpy as np
import chess
import random
hash_table = {}
data = pd.read_csv('./my_list.csv')
chess_opening = data.values.tolist()
chess_opening = [chess[0] for chess in chess_opening]
class AIEasy():
    def __init__(self, game):
        self.game = game
        self.depth = 3

    def evaluate_board(self, board):
        evaluation = 0
        for x in range(8):
            for y in range(8):
                piece = board[x][y]
                if np.sum(self.game.board == '') <=50:
                    piece_values = {
                        'bP': (100 + pawnPoint[7 - x][7 - y]),
                        'bR': (500 + rockPoint[7 - x][7 - y]),
                        'bH': (300 + knightPoint[7 - x][7 - y]),
                        'bB': (300 + bishopPoint[7 - x][7 - y]),
                        'bQ': (1000 + queenPoint[7 - x][7 - y]),
                        'bK': (10000 + kingMidPoint[7 - x][7 - y]),

                        'wP': (100 + pawnPoint[x][y]),
                        'wR': (500 + rockPoint[x][y]),
                        'wH': (300 + knightPoint[x][y]),
                        'wB': (300 + bishopPoint[x][y]),
                        'wQ': (1000 + queenPoint[x][y]),
                        'wK': (10000 + kingMidPoint[x][y]),
                    }
                else:
                    piece_values = {
                        'bP': (100 + pawnPoint[7 - x][7 - y]),
                        'bR': (500 + rockPoint[7 - x][7 - y]),
                        'bH': (300 + knightPoint[7 - x][7 - y]),
                        'bB': (300 + bishopPoint[7 - x][7 - y]),
                        'bQ': (1000 + queenPoint[7 - x][7 - y]),
                        'bK': (10000 + kingEndPoint[7 - x][7 - y]),

                        'wP': (100 + pawnPoint[x][y]),
                        'wR': (500 + rockPoint[x][y]),
                        'wH': (300 + knightPoint[x][y]),
                        'wB': (300 + bishopPoint[x][y]),
                        'wQ': (1000 + queenPoint[x][y]),
                        'wK': (10000 + kingEndPoint[x][y]),
                    }
                value = piece_values.get(piece, 0)
                if piece != '':
                    if piece[0] == 'b':
                        evaluation += value
                    else:
                        evaluation -= value
        return evaluation

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        if (tuple(map(tuple,self.game.board)), depth) in hash_table.keys():
            return hash_table[(tuple(map(tuple,self.game.board)), depth)], None
        if self.game.pyboard.is_game_over():
            if self.game.pyboard.turn == chess.WHITE:
                return 1000000, None
            else:
                return -1000000, None
        if depth == 0:
            return self.evaluate_board(self.game.board), None
        check_end = self.game.end_game(False)
        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for src, dest in self.get_all_moves('b'):
                temp_src = self.game.board[src[0]][src[1]]
                temp_dest = self.game.board[dest[0]][dest[1]]
                temp_ck = self.game.ck[src[0]][src[1]]
                if not self.check_transform(src, dest):
                    self.game.move(src, dest)
                else:
                    self.game.board[src[0]][src[1]] = ''
                    self.game.board[dest[0]][dest[1]] = 'bQ'
                    self.game.pyboard.push(chess.Move.from_uci(self.game.move_to_fen(src, dest) + 'q'))
                eval = self.alpha_beta(depth - 1, alpha, beta, False)[0]
                hash_table[(tuple(map(tuple,self.game.board)), depth-1)] = eval
                self.game.board[dest[0]][dest[1]] = temp_dest
                self.game.board[src[0]][src[1]] = temp_src
                if temp_src == 'bK' and src == (0, 4) and dest == (0, 2):
                    self.game.board[0][3] = ''
                    self.game.board[0][0] = 'bR'
                elif temp_src == 'bK' and src == (0, 4) and dest == (0, 6):
                    self.game.board[0][5] = ''
                    self.game.board[0][7] = 'bR'
                self.game.pyboard.pop()
                self.game.ck[src[0]][src[1]] = temp_ck

                if eval > max_eval:
                    max_eval = eval
                    best_move = (src, dest)
                    if max_eval > 100000:
                        return max_eval, best_move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move
        else:
            min_eval = float('inf')
            for src, dest in self.get_all_moves('w'):
                temp_src = self.game.board[src[0]][src[1]]
                temp_dest = self.game.board[dest[0]][dest[1]]
                temp_ck = self.game.ck[src[0]][src[1]]
                if not self.check_transform(src, dest):
                    self.game.move(src, dest)

                else:
                    self.game.board[src[0]][src[1]] = ''
                    self.game.board[dest[0]][dest[1]] = 'wQ'
                    self.game.pyboard.push(chess.Move.from_uci(self.game.move_to_fen(src, dest) + 'q'))
                eval = self.alpha_beta(depth - 1, alpha, beta, True)[0]
                hash_table[(tuple(map(tuple,self.game.board)), depth-1)] = eval
                self.game.board[dest[0]][dest[1]] = temp_dest
                self.game.board[src[0]][src[1]] = temp_src
                if temp_src == 'wK' and src == (7, 4) and dest == (7, 6):
                    self.game.board[7][5] = ''
                    self.game.board[7][7] = 'wR'
                elif temp_src == 'wK' and src == (7, 4) and dest == (7, 2):
                    self.game.board[7][3] = ''
                    self.game.board[7][0] = 'wR'
                self.game.pyboard.pop()
                self.game.ck[src[0]][src[1]] = temp_ck
                if eval < min_eval:
                    min_eval = eval
                    best_move = (src, dest)
                    if min_eval < -100000:
                        return min_eval, best_move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_all_moves(self, player):
        all_moves = []
        for x in range(8):
            for y in range(8):
                piece = self.game.board[x][y]
                if piece != '' and piece[0] == player:
                    for row in range(8):
                        for col in range(8):
                            if not self.game.restrict((x, y), (row, col)) and not self.game.move_leads_to_check((x, y),
                                                                                                                (row,
                                                                                                                 col)):
                                all_moves.append(((x, y), (row, col)))
        return all_moves

    def select_best_move(self):
        legal_string = []
        check = False
        for string in chess_opening:
            if string.startswith(self.game.string):
                check = True
                temp = string
                temp = temp.replace(self.game.string, '', 1).strip()
                temp = temp[:4]
                legal_string.append(temp)
        if check:
            rand_string = random.choice(legal_string)
            if len(rand_string) > 0:
                return self.game.fen_to_move(rand_string)
        _, best_move = self.alpha_beta(self.depth, float('-inf'), float('inf'), True)
        return best_move

    def check_transform(self, src, dest):
        piece = self.game.board[src[0]][src[1]]
        if piece == 'wP' and dest[0] == 0:
            return True
        if piece == 'bP' and dest[0] == 7:
            return True
        return False

