import tkinter as tk
from tkinter import messagebox

class Game():
    def __init__(self):
        self.board = [
            ['bR', 'bH', 'bB', 'bQ', 'bK', 'bB', 'bH', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wH', 'wB', 'wQ', 'wK', 'wB', 'wH', 'wR']
        ]

    def move(self, src, dest):
        if self.restrict(src, dest):
            return
        piece = self.board[src[0]][src[1]]

        if not self.remove_piece(src, dest):
            temp = self.board[src[0]][src[1]]
            self.board[src[0]][src[1]] = self.board[dest[0]][dest[1]]
            self.board[dest[0]][dest[1]] = temp
        else:
            self.board[dest[0]][dest[1]] = self.board[src[0]][src[1]]
            self.board[src[0]][src[1]] = ''
        self.transform_pawn(src, dest)

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
        row_diff = abs(src[0] - dest[0])
        col_diff = abs(src[1] - dest[1])
        return row_diff <= 1 and col_diff <= 1
    def pawn_move(self, src, dest):
        piece = self.board[src[0]][src[1]]
        if piece[0] == 'b':
            if not self.pawn_remove(src, dest) :
                if self.board[dest[0]][dest[1]] == '':
                    if src[0] == 1:
                        if dest[0] <= src[0] + 2 and dest[1] == src[1]:
                            return True
                    else:
                        if dest[0] <= src[0] + 1 and dest[1] == src[1]:
                            return True
            else:
                if src[0] == 1:
                    if dest[0] <= src[0]+2 and abs(dest[1]- src[1])<=1:
                        return True
                    else:
                        if dest[0] <= src[0] + 1 and abs(dest[1]- src[1])<=1:
                            return True
        else:
            if not self.pawn_remove(src, dest) :
                if self.board[dest[0]][dest[1]] == '':
                    if src[0] == 6:
                        if dest[0] >= src[0] - 2 and dest[1] == src[1]:
                            return True
                    else:
                        if dest[0] >= src[0] - 1 and dest[1] == src[1]:
                            return True
            else:
                if abs(dest[1]- src[1])<=1:
                    return True
        return False
    def pawn_remove(self, src, dest):
        piece = self.board[src[0]][src[1]]
        if piece[0] == 'b':
            if self.board[dest[0]][dest[1]] != '' and self.board[dest[0]][dest[1]][0] != self.board[src[0]][src[1]][0]:
                return (src[0]+1 == dest[0] and (src[1]+1 == dest[1] or src[1]-1 == dest[1]))
        else:
            if self.board[dest[0]][dest[1]] != '' and self.board[dest[0]][dest[1]][0] != self.board[src[0]][src[1]][0]:
                return (src[0] -1  == dest[0] and (src[1] + 1 == dest[1] or src[1] - 1 == dest[1]))
    def prompt_for_promotion_piece(self):
        window = tk.Tk()
        window.title("Phong Quân")
        window.geometry("250x250")

        selected_piece = tk.StringVar(value='Q')

        def select_piece(piece):
            selected_piece.set(piece)
            window.destroy()

        pieces = {'Q': 'Hậu', 'R': 'Xe', 'B': 'Tượng', 'N': 'Mã'}
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