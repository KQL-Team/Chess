import pygame
import pygame as p
from PIL import Image

import chess

chess_img = {}
width = height = 720
dim = 8
p_size = width // dim
FPS = 240

p.init()
screen = p.display.set_mode((width, height))
clock = p.time.Clock()
game = chess.Game()
square_select = ()
player_move = []
white_turn = True
def load_images():
    chess_pieces = ['bR', 'bH', 'bB', 'bQ', 'bK', 'bP', 'wR', 'wH', 'wB', 'wQ', 'wK', 'wP']
    for piece in chess_pieces:
        img = Image.open("Images/" + piece + ".png")
        img = img.resize((p_size, p_size), Image.LANCZOS)
        chess_img[piece] = p.image.fromstring(img.tobytes(), img.size, img.mode).convert_alpha()

load_images()

def main(game_run):
    global square_select
    global white_turn
    screen.fill(p.Color('white'))
    for event in p.event.get():
        if event.type == p.QUIT:
            game_run = False
        elif event.type == p.MOUSEBUTTONDOWN:
            pos = p.mouse.get_pos()
            x = pos[1] // p_size
            y = pos[0] // p_size
            if square_select == (x, y):
                square_select = ()
                player_move.clear()
            else:
                square_select = (x, y)
                player_move.append(square_select)
                check_turn(white_turn, player_move, game.board)
            if len(player_move) == 2:
                if not game.restrict(player_move[0], player_move[1]):
                    white_turn = not white_turn
                    game.move(player_move[0], player_move[1])
                    player_move.clear()
    draw_game(screen, game)
    clock.tick(FPS)
    p.display.flip()
    return game_run

def draw_game(screen, game):
    draw_board(screen)
    draw_pieces(screen, game.board)


def draw_board(screen):
    colors = [p.Color(235, 236, 208), p.Color(119, 148, 85)]
    for y in range(8):
        for x in range(8):
            color = colors[(x + y) % 2]
            p.draw.rect(screen, color, p.Rect(x * p_size, y * p_size, p_size, p_size))


def draw_pieces(screen, board):
    for x in range(8):
        for y in range(8):
            piece = board[y][x]
            if piece != '':
                screen.blit(chess_img[piece], p.Rect(x * p_size, y * p_size, p_size, p_size))


def check_turn(color_turn, player_move, board):
    if (color_turn):
        cur = player_move[0]
        if board[cur[0]][cur[1]] == '' or board[cur[0]][cur[1]][0] == 'b':
            player_move.clear()
    else:
        cur = player_move[0]
        if board[cur[0]][cur[1]] == '' or board[cur[0]][cur[1]][0] == 'w':
            player_move.clear()

