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
# for x in range(8):
#     for y in range(8):
#         piece_values = {
#             'P': 10 + pawnPoint[7-x][7-y],
#             'R': 50 + rockPoint[7-x][7-y],
#             'H': 30 + knightPoint[7-x][7-y],
#             'B': 30 + bishopPoint[7-x][7-y],
#             'Q': 100 + queenPoint[7-x][7-y],
#             'K': 1000 + kingMidPoint[7-x][7-y],
#         }


class AIEasy():
    def __init__(self, game):
        self.game = game
        self.depth = 3

    def evaluate_board(self, board):
        evaluation = 0
        for x in range(8):
            for y in range(8):

                piece = board[x][y]
                if piece != '':
                    if piece[0] == 'b':
                        piece_values = {
                            'P': (10 + pawnPoint[7 - x][7 - y]),
                            'R': (50 + rockPoint[7 - x][7 - y]),
                            'H': (30 + knightPoint[7 - x][7 - y]),
                            'B': (30 + bishopPoint[7 - x][7 - y]),
                            'Q': (100 + queenPoint[7 - x][7 - y]),
                            'K': (1000 + kingMidPoint[7 - x][7 - y]),
                        }
                        value = piece_values.get(piece[1], 0)
                        evaluation += value
                    else:
                        piece_values = {
                            'P': (10 + pawnPoint[x][y]),
                            'R': (50 + rockPoint[x][y]),
                            'H': (30 + knightPoint[x][y]),
                            'B': (30 + bishopPoint[x][y]),
                            'Q': (100 + queenPoint[x][y]),
                            'K': (1000 + kingMidPoint[x][y]),
                        }
                        value = piece_values.get(piece[1], 0)
                        evaluation -= value
        print("Evaluation:", evaluation)
        return evaluation

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        temp_tuple = tuple(tuple(row) for row in self.game.board)
        if depth == 0:
            return self.evaluate_board(self.game.board), None
        if self.game.end_game(False) == (True, 'lose'):
            return self.evaluate_board(self.game.board) + 1000000, None
        if self.game.end_game(False) == (True, 'win'):
            return self.evaluate_board(self.game.board) - 1000000, None
        if self.game.end_game(False) == (True, 'draw'):
            return self.evaluate_board(self.game.board) - 500, None
        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for src, dest in self.get_all_moves('b'):
                temp_src = self.game.board[src[0]][src[1]]
                temp_dest = self.game.board[dest[0]][dest[1]]
                if not self.check_transform(src, dest):
                    self.game.move(src, dest)
                else:
                    self.game.board[src[0]][src[1]] = ''
                    self.game.board[dest[0]][dest[1]] = 'bQ'
                eval = self.alpha_beta(depth - 1, alpha, beta, False)[0]
                self.game.board[dest[0]][dest[1]] = temp_dest
                self.game.board[src[0]][src[1]] = temp_src
                if temp_src == 'bK' and src == (0, 4) and dest == (0, 1):
                    self.game.board[0][2] = ''
                    self.game.board[0][0] = 'bR'
                elif temp_src == 'bK' and src == (0, 4) and dest == (0, 6):
                    self.game.board[0][5] = ''
                    self.game.board[0][7] = 'bR'
                self.game.ck[src[0]][src[1]] = 0
                if eval > max_eval:
                    max_eval = eval
                    best_move = (src, dest)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for src, dest in self.get_all_moves('w'):
                temp_src = self.game.board[src[0]][src[1]]
                temp_dest = self.game.board[dest[0]][dest[1]]
                if not self.check_transform(src, dest):
                    self.game.move(src, dest)
                else:
                    self.game.board[src[0]][src[1]] = ''
                    self.game.board[dest[0]][dest[1]] = 'wQ'
                eval = self.alpha_beta(depth - 1, alpha, beta, True)[0]
                self.game.board[dest[0]][dest[1]] = temp_dest
                self.game.board[src[0]][src[1]] = temp_src
                if temp_src == 'wK' and src == (7, 4) and dest == (7, 6):
                    self.game.board[7][5] = ''
                    self.game.board[7][7] = 'wR'
                elif temp_src == 'wK' and src == (7, 4) and dest == (7, 1):
                    self.game.board[7][2] = ''
                    self.game.board[7][0] = 'wR'
                self.game.ck[src[0]][src[1]] = 0
                if eval < min_eval:
                    min_eval = eval
                    best_move = (src, dest)
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
        _, best_move = self.alpha_beta(self.depth, float('-inf'), float('inf'), True)
        return best_move

    def check_transform(self, src, dest):
        piece = self.game.board[src[0]][src[1]]
        if piece == 'wP' and dest[0] == 0:
            return True
        if piece == 'bP' and dest[0] == 7:
            return True
        return False
