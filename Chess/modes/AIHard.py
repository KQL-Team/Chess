import numpy as np
import time
import chess
import chess.engine
import pandas as pd
import random
data = pd.read_csv('./my_list.csv')
chess_opening = data.values.tolist()
chess_opening = [chess[0] for chess in chess_opening]
class AIHard():
    def __init__(self, game):
        self.game = game
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
        if self.game.pyboard.is_game_over():
            if self.game.pyboard.turn == chess.WHITE:
                return 1000000000
        #Use your own absolute path
        with chess.engine.SimpleEngine.popen_uci('C:/Users/Admin/OneDrive - vnu.edu.vn/PycharmProjects/Chess/Chess/model/model.exe') as sf:
            result = sf.analyse(board, chess.engine.Limit(depth=10))
            prediction = result['score'].black().score()
            if prediction != None:
                return prediction
            else:
                if str(result['score'])[1] == '+':
                    return -1000000
                else:
                    return 1000000
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
            return self.game.fen_to_move(rand_string)
        moves = self.get_all_moves('b')
        best_move = None
        max_eval = float('-inf')
        for src, dest in moves:
            if not self.check_transform(src, dest):
                self.game.pyboard.push(chess.Move.from_uci(self.game.move_to_fen(src, dest)))
            else:
                self.game.pyboard.push(chess.Move.from_uci(self.game.move_to_fen(src, dest) + 'q'))
            eval = self.evaluate_board(self.game.pyboard)
            print(eval)
            if eval >= max_eval:
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
