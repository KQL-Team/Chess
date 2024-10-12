import numpy as np
import time
import chess
import chess.engine
dict2 = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
dict3 = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
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
        with chess.engine.SimpleEngine.popen_uci('C:/Users/Admin/OneDrive - vnu.edu.vn/PycharmProjects/Chess/Chess/stockfish/model.exe') as sf:
            result = sf.analyse(board, chess.engine.Limit(depth=10))
            prediction = result['score'].black().score()
            return prediction
    def select_best_move(self):
         moves = self.get_all_moves('b')
         best_move = None
         max_eval = float('-inf')
         for src, dest in moves:
             self.game.pyboard.push(chess.Move.from_uci(self.move_to_fen(src, dest)))
             eval = self.evaluate_board(self.game.pyboard)
             if eval > max_eval:
                 max_eval = eval
                 best_move = (src, dest)
             self.game.pyboard.pop()
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
    def move_to_fen(self, src, dest):
        str = ''
        str += dict2[src[1]]
        str += dict3[src[0]]
        str += dict2[dest[1]]
        str += dict3[dest[0]]
        return str