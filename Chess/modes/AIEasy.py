piece_values = {
    'P': 10,
    'R': 50,
    'H': 40,
    'B': 30,
    'Q': 90,
    'K': 1000
}

class AIEasy():
    def __init__(self, game):
        self.game = game
        self.depth = 2
        self.transposition_table = {}

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

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        board_hash = hash(tuple(tuple(row) for row in self.game.board))
        if board_hash in self.transposition_table and self.transposition_table[board_hash]['depth'] >= depth:
            return self.transposition_table[board_hash]['value'], None
        if depth == 0:
            return self.evaluate_board(self.game.board), None
        if self.game.end_game() == (True, 'lose'):
            return self.evaluate_board(self.game.board) + 1000000, None
        if self.game.end_game() == (True, 'win'):
            return self.evaluate_board(self.game.board) - 1000000, None
        if self.game.end_game() == (True, 'draw'):
            return self.evaluate_board(self.game.board) - 500, None
        if self.game.check_black():
            return self.evaluate_board(self.game.board) - 10, None
        if self.game.check_white():
            return self.evaluate_board(self.game.board) + 10, None
        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for src, dest in self.get_all_moves('b'):
                temp_src = self.game.board[src[0]][src[1]]
                temp_dest = self.game.board[dest[0]][dest[1]]
                self.game.move(src, dest)
                eval = self.alpha_beta(depth - 1, alpha, beta, False)[0]
                self.game.board[dest[0]][dest[1]] = temp_dest
                self.game.board[src[0]][src[1]] = temp_src
                if temp_src == 'bK' and src == (0,4) and dest == (0,1):
                    self.game.board[0][2] = ''
                    self.game.board[0][0] = 'bR'
                elif temp_src == 'bK' and src == (0,4) and dest == (0,6):
                    self.game.board[0][5] = ''
                    self.game.board[0][7] = 'bR'
                self.game.ck[src[0]][src[1]] = 0
                if eval > max_eval:
                    max_eval = eval
                    best_move = (src, dest)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[board_hash] = {'value': max_eval, 'depth': depth}
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for src, dest in self.get_all_moves('w'):
                temp_src = self.game.board[src[0]][src[1]]
                temp_dest = self.game.board[dest[0]][dest[1]]
                self.game.move(src, dest)
                eval = self.alpha_beta(depth - 1, alpha, beta, True)[0]
                self.game.board[dest[0]][dest[1]] = temp_dest
                self.game.board[src[0]][src[1]] = temp_src
                if temp_src == 'wK' and src == (7,4) and dest == (7,6):
                    self.game.board[7][5] = ''
                    self.game.board[7][7] = 'wR'
                elif temp_src == 'wK' and src == (7,4) and dest == (7,1):
                    self.game.board[7][2] = ''
                    self.game.board[7][0] = 'wR'
                self.game.ck[src[0]][src[1]] = 0
                if eval < min_eval:
                    min_eval = eval
                    best_move = (src, dest)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[board_hash] = {'value': min_eval, 'depth': depth}
            return min_eval, best_move

    def order_moves(self, moves, player):
        def move_value(move):
            _, dest = move
            piece = self.game.board[dest[0]][dest[1]]
            return piece_values.get(piece[1], 0) if piece and piece[0] != player else 0
        return sorted(moves, key=move_value, reverse=True)

    def get_all_moves(self, player):
        all_moves = []
        for x in range(8):
            for y in range(8):
                piece = self.game.board[x][y]
                if piece != '' and piece[0] == player:
                    for row in range(8):
                        for col in range(8):
                            if not self.game.restrict((x, y), (row, col)) and not self.game.move_leads_to_check((x, y), (row, col)):
                                all_moves.append(((x, y), (row, col)))
        return self.order_moves(all_moves, player)

    def select_best_move(self):
        _, best_move = self.alpha_beta(self.depth, float('-inf'), float('inf'), True)
        return best_move
