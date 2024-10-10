import numpy as np
from keras.models import load_model
import tensorflow as tf
import h5py
pieces = ['bR', 'bH', 'bB', 'bQ', 'bK', 'bP', 'wR', 'wH', 'wB', 'wQ', 'wK', 'wP', '']
tf.get_logger().setLevel('ERROR')
chess_model = load_model('chess_model.h5')
class AIHard():
    def __init__(self, game):
        self.game = game
        self.depth = 3
    def one_hot_encode_piece(self, piece):
        global pieces
        arr = np.zeros(len(pieces), dtype=np.uint8)
        piece_to_index = {p: i for i, p in enumerate(pieces)}
        index = piece_to_index[piece]
        arr[index] = 1
        return arr
    def encode_board(self, board):
        board_list = []
        for row in board:
            row_list = []
            for piece in row:
                row_list.append(self.one_hot_encode_piece(piece))
            board_list.append(row_list)
        return np.array(board_list)


    def evaluate_board(self, board):
        encoded_board = self.encode_board(board).reshape(1,8,8,13)
        prediction = chess_model.predict(encoded_board)
        return prediction
    def alpha_beta(self, depth, alpha, beta, maximizing_player):
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
            return min_eval, best_move

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
        return all_moves
