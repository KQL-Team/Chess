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

        # if piece[1] == 'H' and not self.h_move(src, dest):
        #     return
        # elif piece[1] == 'R' and not self.r_move(src, dest):
        #     return
        # elif piece[1] == 'B' and not self.b_move(src, dest):
        #     return
        # elif piece[1] == 'Q' and not self.queen_move(src, dest):
        #     return
        # elif piece[1] == 'K' and not self.king_move(src, dest):
        #     return
        # elif piece[1] == 'p' and not self.pawn_move(src, dest):
        #     return

        if not self.remove_piece(src, dest):
            temp = self.board[src[0]][src[1]]
            self.board[src[0]][src[1]] = self.board[dest[0]][dest[1]]
            self.board[dest[0]][dest[1]] = temp
        else:
            self.board[dest[0]][dest[1]] = self.board[src[0]][src[1]]
            self.board[src[0]][src[1]] = ''

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
        return False

    def remove_piece(self, src, dest):
        if self.board[src[0]][src[1]] != '' and self.board[dest[0]][dest[1]] != '':
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
        return
