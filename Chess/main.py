import sys
import pygame
import pygame as p
from PIL import Image
import config as cg
import game
import pygame.gfxdraw
import numpy as np
from game import Game
from Chess.menu import game_state
from modes.AIEasy import AIEasy
from modes.AIHard import AIHard
from modes import AIHard as AH
chess_img = {}
end_game_image = []
game_run = cg.game_run
game_state = 1
choice = cg.choice
width = cg.width 
height = cg.height
dim = cg.dim
p_size = width // dim
FPS = cg.p_size
screen = cg.screen
pygame.display.set_caption('Chess')
p.init()
clock = p.time.Clock()
game = game.Game()
ai = AIEasy(game)
ai2 = AIHard(game)
square_select = ()
player_move = []
cur_src = None
cur_dest = None
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

def set_game_state(new_game_state):
    global game_state
    game_state = new_game_state

def main():
    global game_run, white_turn, game_state, cur_src, cur_dest

    screen.fill(p.Color('white'))
    #print(game_state)
    for event in p.event.get():
        if event.type == p.QUIT:
            game_run = False
        elif event.type == p.MOUSEBUTTONDOWN :
            if game_state == 1:
                white_turn = check_mouse(p, game)
            elif game_state == 2 or game_state == 3:
                if white_turn:
                    white_turn = check_mouse(p, game)
    # if game_state == 2:
    #     if white_turn:
    #         white_turn = check_mouse(p, game)
    #     else:
    #         ai_move = ai.select_best_move()
    #         game.move(ai_move[0], ai_move[1])
    #         white_turn = not white_turn

    draw_game(screen, game, player_move, cur_src, cur_dest)
    game_over(screen)

    clock.tick(FPS)

    p.display.flip()
    if game_state == 2 and not white_turn:
        ai_move = ai.select_best_move()
        if ai_move:
            game.move(ai_move[0], ai_move[1])
            cur_src = ai_move[0]
            cur_dest = ai_move[1]
            white_turn = not white_turn
    if game_state == 3 and not white_turn:
        ai_move = ai2.select_best_move()
        if ai_move:
            game.move(ai_move[0], ai_move[1])
            cur_src = ai_move[0]
            cur_dest = ai_move[1]
            white_turn = not white_turn
    draw_game(screen, game, player_move, cur_src, cur_dest)
    game_over(screen)

    clock.tick(FPS)

    p.display.flip()
    return game_run, game_state
def draw_game(screen, game, player_move, cur_src, cur_dest):
    if len(player_move) == 1:
        draw_temp_board(screen, game, player_move, cur_src, cur_dest)

    else:
        draw_board(screen, cur_src, cur_dest)
    if game.check_white():
        white_king(game)
    if game.check_black():
        black_king(game)
    draw_pieces(screen, game.board)


def draw_board(screen, cur_src, cur_dest):
    colors = [p.Color(235, 236, 208), p.Color("#9A784F"), p.Color('#F5F682')]
    for y in range(8):
        for x in range(8):
            color = colors[(x + y) % 2]
            p.draw.rect(screen, color, p.Rect(x * p_size, y * p_size, p_size, p_size))
            if (y, x)  == cur_src or (y, x) == cur_dest:
                p.draw.rect(screen, colors[2], p.Rect(x * p_size, y * p_size, p_size, p_size))


def draw_pieces(screen, board):
    for x in range(8):
        for y in range(8):
            piece = board[y][x]
            if piece != '':
                screen.blit(chess_img[piece], p.Rect(x * p_size, y * p_size, p_size, p_size))


def draw_temp_board(screen, game, player_move, cur_src, cur_dest):
    colors = [p.Color(235, 236, 208), p.Color("#9A784F"), p.Color('#795C34'), p.Color('#F5F682'), p.Color('#FFBF00')]
    for y in range(8):
        for x in range(8):
            color = colors[(x + y) % 2]
            p.draw.rect(screen, color, p.Rect(x * p_size, y * p_size, p_size, p_size))
            if (y, x) == cur_src or (y, x) == cur_dest:
                p.draw.rect(screen, colors[3], p.Rect(x * p_size, y * p_size, p_size, p_size))
            if not game.restrict(player_move[0], (y, x)) and not game.move_leads_to_check(player_move[0], (y, x)):
                pygame.gfxdraw.aacircle(screen, int((x+0.5) * p_size), int((y+0.5) * p_size), p_size//10, colors[2])
                pygame.gfxdraw.filled_circle(screen, int((x+0.5) * p_size), int((y+0.5)* p_size), p_size//10, colors[2])
                if game.remove_piece(player_move[0], (y, x)):
                    p.draw.rect(screen, colors[4], p.Rect(x * p_size, y * p_size, p_size, p_size))



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
    global square_select, white_turn, cur_src, cur_dest
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
        if not game.restrict(player_move[0], player_move[1]) and not game.move_leads_to_check(player_move[0],
                                                                                              player_move[1]):
            game.move(player_move[0], player_move[1])
            white_turn = not white_turn
            cur_src = player_move[0]
            cur_dest = player_move[1]
        player_move.clear()
        square_select = ()
    return white_turn


def game_over(screen):
    global game_run, game_state, white_turn
    result = game.end_game(white_turn)

    if result[0]:
        if result[1] == "win":
            screen.blit(end_game_image[0], p.Rect(0.5 * p_size, 3 * p_size, 7 * p_size, 2 * p_size))
        elif result[1] == "lose":
            screen.blit(end_game_image[1], p.Rect(0.5 * p_size, 3 * p_size, 7 * p_size, 2 * p_size))
        elif result[1] == "draw":
            screen.blit(end_game_image[2], p.Rect(0.5 * p_size, 3 * p_size, 7 * p_size, 2 * p_size))

        # Hiển thị nút Reset
        menu_rect = p.Rect(0, 0, p_size * 2, p_size // 2)
        menu_rect.center = (width // 2, height // 2 + p_size * 2)
        p.draw.rect(screen, p.Color('grey'), menu_rect)
        font = p.font.SysFont("Georgia", 30)
        text_surface = font.render("Menu", True, p.Color('black'))
        text_rect = text_surface.get_rect(center=menu_rect.center)
        screen.blit(text_surface, text_rect)

        # Kiểm tra nếu nhấn vào nút Menu thì trở lại menu chính
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if menu_rect.collidepoint(mouse_pos):
                    game_state = 0

def reset_board():
    global game
    game.board = np.array([
            ['bR', 'bH', 'bB', 'bQ', 'bK', 'bB', 'bH', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wH', 'wB', 'wQ', 'wK', 'wB', 'wH', 'wR']
        ])
def reset():
    global white_turn
    white_turn = True