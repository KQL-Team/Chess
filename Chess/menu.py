from modes import AIEasy, AIHard, pvp
import pygame as p
import random
import math
import config as cg
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

p.init()

AnKing = p.transform.rotate(p.transform.scale(p.image.load("Images/king.png"), (75, 75)), 40)
AnQueen = p.transform.rotate(p.transform.scale(p.image.load("Images/queen.png"), (75, 75)), 40)
AnPawn = p.transform.rotate(p.transform.scale(p.image.load("Images/pawn.png"), (75, 75)), 40)
AnKnight = p.transform.rotate(p.transform.scale(p.image.load("Images/knight.png"), (75, 75)), 40)
clock = p.time.Clock()

font = p.font.Font(None, 36)
brown = p.color.THECOLORS["brown"]
black = p.color.THECOLORS["black"]
white = p.color.THECOLORS["seashell1"]
gray = p.color.THECOLORS["grey44"]

game_run = cg.game_run
choice = cg.choice
width = cg.width
height = cg.height
dim = cg.dim
p_size = width // dim
FPS = cg.p_size
screen = cg.screen


def draw_menu(choice, menu_run):
    screen.fill(p.Color(134, 165, 91))

    title_text = font.render("Racism's Chess", True, white)
    title_rect = title_text.get_rect(center=(width // 2, 50))
    screen.blit(title_text, title_rect)

    subtitle_text = font.render("by KQL AI Company", True, white)
    subtitle_rect = subtitle_text.get_rect(center=(width // 2, 80))
    screen.blit(subtitle_text, subtitle_rect)

    button_width = 200
    button_height = 50
    button_x = (width - button_width) // 2
    button_y = 200
    button_spacing = 20

    buttons = [
        {"text": "pvp", "rect": p.Rect(button_x, button_y, button_width, button_height)},
        {"text": "AIEasy",
         "rect": p.Rect(button_x, button_y + button_height + button_spacing, button_width, button_height)},
        {"text": "AIHard",
         "rect": p.Rect(button_x, button_y + 2 * button_height + 2 * button_spacing, button_width, button_height)}
    ]

    for button in buttons:
        p.draw.rect(screen, brown, button["rect"], border_radius=10)
        button_text = font.render(button["text"], True, black)
        button_text_rect = button_text.get_rect(center=button["rect"].center)
        screen.blit(button_text, button_text_rect)

    mouse = p.mouse.get_pos()
    mouse_click = p.mouse.get_pressed()
    for i, button in enumerate(buttons):
        if button["rect"].collidepoint(mouse):
            if mouse_click[0]:
                if i == 0:
                    choice = 1
                    menu_run = True
                elif i == 1:
                    p.quit()
                    # Thêm mã để gọi file chế độ AIEasy
                elif i == 2:
                    p.quit()
                    # Thêm mã để gọi file chế độ AIHard
    return choice, menu_run


def random_pieces():
    pieces = [AnKing, AnQueen, AnPawn, AnKnight]
    x = random.randint(0, width - 20)
    y = -50
    random_piece = random.choices(pieces)[0]
    falling_pieces = (random_piece, [x, y])
    return falling_pieces


falling_piece = random_pieces()
falling_piece2 = random_pieces()


def run(game_run):
    global falling_piece
    # global falling_piece2
    falling_piece[1][1] += 1
    count = 0
    clock.tick(FPS)
    for event in p.event.get():
        if event.type == p.QUIT:
            game_run = True
    screen.fill(p.color.THECOLORS["chartreuse4"])
    choice, game_run = draw_menu(0, game_run)
    screen.blit(falling_piece[0], falling_piece[1])

    if falling_piece[1][1] > height/2:
        count = 1
    if count == 1:
        falling_piece2[1][1] += 1
        screen.blit(falling_piece2[0], falling_piece2[1])
    if falling_piece[1][1] > height:
        falling_piece = random_pieces()
    if falling_piece2[1][1] > height:
        falling_piece = random_pieces()

    p.display.flip()
    return game_run, choice
