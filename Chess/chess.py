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
        if not self.remove_piece(src, dest):
            temp = self.board[src[0]][src[1]]
            self.board[src[0]][src[1]] = self.board[dest[0]][dest[1]]
            self.board[dest[0]][dest[1]] = temp
        else:
            self.board[dest[0]][dest[1]] = self.board[src[0]][src[1]]
            self.board[src[0]][src[1]] = ''
    def restrict(self, src, dest):
        if self.board[src[0]][src[1]] != '' and self.board[dest[0]][dest[1]] != '':
            if self.board[src[0]][src[1]][0] == self.board[dest[0]][dest[1]][0]:
                return True
        return False
    def remove_piece(self, src, dest):
        if self.board[src[0]][src[1]] != '' and self.board[dest[0]][dest[1]] != '':
            if self.board[src[0]][src[1]][0] != self.board[dest[0]][dest[1]][0]:
                return True
        return False