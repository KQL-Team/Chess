import sys

import pygame
import pygame as p
from PIL import Image
import config as cg
import chess
import pygame.gfxdraw
import numpy as np
chess_img = {}
end_game_image = []
game_run = cg.game_run
game_state = cg.GAME_STATE
choice = cg.choice
width = cg.width 
height = cg.height
dim = cg.dim
p_size = width // dim
FPS = cg.p_size
screen = cg.screen 
pygame.display.set_caption('Chess')

p.init()
temp = True, "win"
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
    imggs = ['white_won', 'black_won', 'draw']
    for i in range(3):
        img = Image.open("Images/"+ imggs[i] + ".png")
        img = img.resize((p_size*7, p_size*2))
        end_game_image.append(p.image.fromstring(img.tobytes(), img.size, img.mode).convert_alpha())


load_images()


def main():
    global game_run, temp
    screen.fill(p.Color('white'))
    for event in p.event.get():
        if event.type == p.QUIT:
            game_run = False
        elif event.type == p.MOUSEBUTTONDOWN:
            white_turn = check_mouse(p, game)
    draw_game(screen, game, player_move)
    if game.end_game() != temp:
        print(game.end_game())
    if game.end_game() == (True, "win"):
        screen.blit(end_game_image[0], p.Rect(0.5 * p_size, 3 * p_size, p_size, p_size))
        cg.game_run = False
    if game.end_game() == (True, "lose"):
        screen.blit(end_game_image[1], p.Rect(0.5 * p_size, 3 * p_size, p_size, p_size))

    temp = game.end_game()
    clock.tick(FPS)
    p.display.flip()
    return game_run


def draw_game(screen, game, player_move):
    if len(player_move) == 1:
        draw_temp_board(screen, game, player_move)

    else:
        draw_board(screen)
    if game.check_white():
        white_king(game)
    if game.check_black():
        black_king(game)
    draw_pieces(screen, game.board)


def draw_board(screen):
    colors = [p.Color(235, 236, 208), p.Color("#9A784F")]
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


def draw_temp_board(screen, game, player_move):
    colors = [p.Color(235, 236, 208), p.Color("#9A784F"), p.Color('#795C34'), p.Color('#F5F682')]
    for y in range(8):
        for x in range(8):
            color = colors[(x + y) % 2]
            p.draw.rect(screen, color, p.Rect(x * p_size, y * p_size, p_size, p_size))
            if not game.restrict(player_move[0], (y, x)) and not game.move_leads_to_check(player_move[0], (y, x)):
                pygame.gfxdraw.aacircle(screen, int((x+0.5) * p_size), int((y+0.5) * p_size), p_size//10, colors[2])
                pygame.gfxdraw.filled_circle(screen, int((x+0.5) * p_size), int((y+0.5)* p_size), p_size//10, colors[2])
                if game.remove_piece(player_move[0], (y, x)):
                    p.draw.rect(screen, colors[3], p.Rect(x * p_size, y * p_size, p_size, p_size))


def check_turn(color_turn, player_move, board):
    if (color_turn):
        cur = player_move[0]
        if board[cur[0]][cur[1]] == '' or board[cur[0]][cur[1]][0] == 'b':
            player_move.clear()
    else:
        cur = player_move[0]
        if board[cur[0]][cur[1]] == '' or board[cur[0]][cur[1]][0] == 'w':
            player_move.clear()


def white_king(game):
    temp = np.where(game.board == 'wK')
    x = temp[0][0]
    y = temp[1][0]
    p.draw.rect(screen, p.Color('red'), p.Rect(y * p_size, x * p_size, p_size, p_size))


def black_king(game):
    temp = np.where(game.board == 'bK')
    x = temp[0][0]
    y = temp[1][0]
    p.draw.rect(screen, p.Color('red'), p.Rect(y * p_size, x * p_size, p_size, p_size))


def check_mouse(p, game):
    global square_select
    global white_turn
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
        if not game.restrict(player_move[0], player_move[1]) and not game.move_leads_to_check(player_move[0], player_move[1]):
            white_turn = not white_turn
            game.move(player_move[0], player_move[1])
        player_move.clear()
        square_select = ()
    return white_turn