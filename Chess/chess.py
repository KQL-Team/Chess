import tkinter as tk
from tkinter import messagebox
import numpy as np
from prompt_toolkit.key_binding.bindings.named_commands import self_insert


class Game():
    def __init__(self):
        self.board = np.array([
            ['bR', 'bH', 'bB', 'bQ', 'bK', 'bB', 'bH', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wH', 'wB', 'wQ', 'wK', 'wB', 'wH', 'wR']
        ])
        self.ck = np.zeros((10, 10), dtype=int)
        self.white_check = False
        self.black_check = False

    def move(self, src, dest):
        if self.restrict(src, dest):
            return
        if self.move_leads_to_check(src, dest):
            return
        if self.castling(src, dest):
            return
        self.ck[src[0]][src[1]] = 1
        if not self.remove_piece(src, dest):
            temp = self.board[src[0]][src[1]]
            self.board[src[0]][src[1]] = self.board[dest[0]][dest[1]]
            self.board[dest[0]][dest[1]] = temp
        else:
            self.board[dest[0]][dest[1]] = self.board[src[0]][src[1]]
            self.board[src[0]][src[1]] = ''
        self.transform_pawn(src, dest)

    def move_leads_to_check(self, src, dest):
        temp_board = self.board.copy()
        temp_board[dest[0]][dest[1]] = temp_board[src[0]][src[1]]
        temp_board[src[0]][src[1]] = ''

        if self.board[src[0]][src[1]][0] == 'w':
            temp_game = Game()
            temp_game.board = temp_board
            return temp_game.check_white()
        elif self.board[src[0]][src[1]][0] == 'b':
            temp_game = Game()
            temp_game.board = temp_board
            return temp_game.check_black()
        return False

    def restrict(self, src, dest):
        first_char = self.board[src[0]][src[1]][1]
        if self.board[src[0]][src[1]] != '' and self.board[dest[0]][dest[1]] != '':
            if self.board[src[0]][src[1]][0] == self.board[dest[0]][dest[1]][0]:
                return True
        if first_char == 'H' and not self.h_move(src, dest):
            return True
        elif first_char == 'R' and not self.r_move(src, dest):
            return True
        elif first_char == 'B' and not self.b_move(src, dest):
            return True
        elif first_char == 'Q' and not self.queen_move(src, dest):
            return True
        elif first_char == 'K' and not self.king_move(src, dest):
            return True
        elif first_char == 'P' and not self.pawn_move(src, dest):
            return True
        return False

    def remove_piece(self, src, dest):
        if self.board[dest[0]][dest[1]] != '':
            if self.board[src[0]][src[1]][0] != self.board[dest[0]][dest[1]][0]:
                return True
        return False

    def h_move(self, src, dest):
        row_diff = abs(src[0] - dest[0])
        col_diff = abs(src[1] - dest[1])
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    def r_move(self, src, dest):
        if src[0] != dest[0] and src[1] != dest[1]:
            return False
        if src[0] == dest[0]:
            step = 1 if dest[1] > src[1] else -1
            for col in range(src[1] + step, dest[1], step):
                if self.board[src[0]][col] != '':
                    return False
        else:
            step = 1 if dest[0] > src[0] else -1
            for row in range(src[0] + step, dest[0], step):
                if self.board[row][src[1]] != '':
                    return False
        return True

    def b_move(self, src, dest):
        if abs(src[0] - dest[0]) != abs(src[1] - dest[1]):
            return False
        row_step = 1 if dest[0] > src[0] else -1
        col_step = 1 if dest[1] > src[1] else -1
        for i in range(1, abs(dest[0] - src[0])):
            if self.board[src[0] + i * row_step][src[1] + i * col_step] != '':
                return False
        return True

    def queen_move(self, src, dest):
        return self.r_move(src, dest) or self.b_move(src, dest)

    def king_move(self, src, dest):
        piece = self.board[src[0]][src[1]]
        row_diff = abs(src[0] - dest[0])
        col_diff = abs(src[1] - dest[1])
        if piece[0] == 'w' and piece[1] == 'K' and self.ck[7][4] == 0 and not self.white_check:
            if dest == (7, 1) and self.ck[7][0] == 0:
                if self.board[7][1] == '' and self.board[7][2] == '' and self.board[7][3] == '':
                    return True
            if dest == (7, 6) and self.ck[7][7] == 0:
                if self.board[7][5] == '' and self.board[7][6] == '':
                    return True

        if piece[0] == 'b' and piece[1] == 'K' and self.ck[0][4] == 0 and not self.black_check:
            if dest == (0, 1) and self.ck[0][0] == 0:
                if self.board[0][1] == '' and self.board[0][2] == '' and self.board[0][3] == '':
                    return True
            if dest == (0, 6) and self.ck[0][7] == 0:
                if self.board[0][5] == '' and self.board[0][6] == '':
                    return True

        if row_diff <= 1 and col_diff <= 1:
            return True

        return False

    def pawn_move(self, src, dest):
        piece = self.board[src[0]][src[1]]
        temp = abs(src[0] - dest[0])
        if piece[0] == 'b':
            if not self.pawn_remove(src, dest):
                if self.board[dest[0]][dest[1]] == '':
                    if src[0] == 1:
                        if dest[0] <= src[0] + 2 and dest[1] == src[1] and dest[0] >= src[0]:
                            for i in range(1, temp):
                                if self.board[src[0] + i][src[1]] != '':
                                    return False
                            return True
                    else:
                        if dest[0] <= src[0] + 1 and dest[1] == src[1] and dest[0] >= src[0]:
                            return True
            else:
                if abs(dest[1] - src[1]) <= 1:
                    return True
        else:
            if not self.pawn_remove(src, dest):
                if self.board[dest[0]][dest[1]] == '':
                    if src[0] == 6:
                        if dest[0] >= src[0] - 2 and dest[1] == src[1] and dest[0] <= src[0]:
                            for i in range(1, temp):
                                if self.board[src[0] - i][src[1]] != '':
                                    return False
                            return True
                    else:
                        if dest[0] >= src[0] - 1 and dest[1] == src[1] and dest[0] <= src[0]:
                            return True
            else:
                if abs(dest[1] - src[1]) <= 1:
                    return True
        return False

    def pawn_remove(self, src, dest):
        piece = self.board[src[0]][src[1]]
        if piece[0] == 'b':
            if self.board[dest[0]][dest[1]] != '' and self.board[dest[0]][dest[1]][0] != self.board[src[0]][src[1]][0]:
                return src[0] + 1 == dest[0] and (src[1] + 1 == dest[1] or src[1] - 1 == dest[1])
        else:
            if self.board[dest[0]][dest[1]] != '' and self.board[dest[0]][dest[1]][0] != self.board[src[0]][src[1]][0]:
                return src[0] - 1 == dest[0] and (src[1] + 1 == dest[1] or src[1] - 1 == dest[1])

    def prompt_for_promotion_piece(self):
        window = tk.Tk()
        window.title("Pawn Promotion")
        window.geometry("250x250")

        selected_piece = tk.StringVar(value='Q')

        def select_piece(piece):
            selected_piece.set(piece)
            window.destroy()

        pieces = {'Q': 'Queen', 'R': 'Rook', 'B': 'Bishop', 'N': 'Horse'}
        for piece, name in pieces.items():
            button = tk.Button(window, text=name, command=lambda p=piece: select_piece(p))
            button.pack(pady=10)

        window.mainloop()
        return selected_piece.get()

    def transform_pawn(self, src, dest):
        piece = self.board[dest[0]][dest[1]]
        if piece[0] == 'b' and piece[1] == 'P':
            if dest[0] == 7:
                promotion_piece = self.prompt_for_promotion_piece()
                self.board[dest[0]][dest[1]] = 'b' + promotion_piece
        if piece[0] == 'w' and piece[1] == 'P':
            if dest[0] == 0:
                promotion_piece = self.prompt_for_promotion_piece()
                self.board[dest[0]][dest[1]] = 'w' + promotion_piece

    def check_white(self):
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != '' and self.board[x][y][0] == 'b':
                    temp = np.where(self.board == 'wK')
                    if temp[0].size > 0 and not self.restrict((x, y), (temp[0][0], temp[1][0])):
                        self.white_check = True
                        return True
        self.white_check = False
        return False

    def check_black(self):
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != '' and self.board[x][y][0] == 'w':
                    temp = np.where(self.board == 'bK')
                    if temp[0].size > 0 and not self.restrict((x, y), (temp[0][0], temp[1][0])):
                        self.black_check = True
                        return True
        self.black_check = False
        return False

    def castling(self, src, dest):
        piece = self.board[src[0]][src[1]]
        if piece[0] == 'w' and piece[1] == 'K' and src == (7, 4):
            if dest == (7, 1):
                self.board[7][4] = ''
                self.board[7][1] = 'wK'

                self.board[7][0] = ''
                self.board[7][2] = 'wR'
                self.ck[7][4] = 1
                return True
            elif dest == (7, 6):
                self.board[7][6] = 'wK'
                self.board[7][4] = ''

                self.board[7][7] = ''
                self.board[7][5] = 'wR'
                self.ck[7][4] = 1
                return True
        if piece[0] == 'b' and piece[1] == 'K' and src == (0, 4):
            if dest == (0, 1):
                self.board[0][1] = 'bK'
                self.board[0][4] = ''

                self.board[0][0] = ''
                self.board[0][2] = 'bR'
                self.ck[0][4] = 1
                return True
            elif dest == (0, 6):
                self.board[0][6] = 'bK'
                self.board[0][4] = ''

                self.board[0][7] = ''
                self.board[0][5] = 'bR'
                self.ck[0][4] = 1
                return True
        return False

    def end_game(self):
        if self.check_white():
            for x in range(8):
                for y in range(8):
                    if self.board[x][y] != '' and self.board[x][y][0] == "w":
                        for col in range(8):
                            for row in range(8):
                                if not self.restrict((x, y), (col, row)) and not self.move_leads_to_check((x, y), (col, row)):
                                    return False, "white_check"
            return True, "lose"
        if self.check_black():
            for x in range(8):
                for y in range(8):
                    if self.board[x][y] != '' and self.board[x][y][0] == "b":
                        for col in range(8):
                            for row in range(8):
                                if not self.restrict((x, y), (col, row)) and not self.move_leads_to_check((x, y), (col, row)):
                                    return False, "black_check"
            return True, "win"
        drawW = 0
        drawB = 0
        if not (self.check_white() or self.check_black()):
            for x in range(8):
                for y in range(8):
                    if self.board[x][y] != '' and self.board[x][y][0] == "b":
                        for col in range(8):
                            for row in range(8):
                                if not self.restrict((x, y), (col, row)) and not self.move_leads_to_check((x, y), (col, row)):
                                    drawB =1
                    if self.board[x][y] != '' and self.board[x][y][0] == "w":
                        for col in range(8):
                            for row in range(8):
                                if not self.restrict((x, y), (col, row)) and not self.move_leads_to_check((x, y), (col, row)):
                                    drawW =1
            if drawB == 0 or drawW == 0:
                return True, "draw"
            else:
                return False, "cont"
        return False, "cont2"
