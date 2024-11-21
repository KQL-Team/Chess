import pygame

from modes import AIEasy, AIHard
import pygame as p
import random
import math
import config as cg
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

p.init()

AnKing = p.transform.rotate(p.transform.scale(p.image.load("Images/king.png"), (75, 75)), 40)
AnQueen = p.transform.rotate(p.transform.scale(p.image.load("Images/queen.png"), (75, 75)), 40)
AnPawn = p.transform.rotate(p.transform.scale(p.image.load("Images/pawn.png"), (65, 65)), 40)
AnKnight = p.transform.rotate(p.transform.scale(p.image.load("Images/knight.png"), (75, 75)), 40)
clock = p.time.Clock()

font = p.font.SysFont("Georgia", 23)
font2 = p.font.SysFont("Georgia", 19)
brown = p.Color(138,50,36)
black = p.color.THECOLORS["black"]
white = p.color.THECOLORS["seashell1"]
gray = p.color.THECOLORS["grey44"]

game_state = cg.GAME_STATE
game_run = cg.game_run
choice = cg.choice
width = cg.width
height = cg.height
dim = cg.dim
p_size = width // dim
FPS = cg.p_size
screen = cg.screen
image = p.transform.smoothscale(p.image.load("Images/background.png"), (720, 720))
def draw_menu():
    global game_state
    screen.blit(image, (0, 0))

    title_text = font.render("Chess Game", True, white)
    title_rect = title_text.get_rect(center=(width // 2, 50))
    screen.blit(title_text, title_rect)

    subtitle_text = font2.render("by KQL AI Company", True, white)
    subtitle_rect = subtitle_text.get_rect(center=(width // 2, 80))
    screen.blit(subtitle_text, subtitle_rect)

    button_width = 200
    button_height = 65
    button_x = (width - button_width) // 2
    button_y = 280
    button_spacing = 20

    buttons = [
        {"text": "PvP", "rect": p.Rect(button_x, button_y, button_width, button_height)},
        {"text": "AIEasy",
         "rect": p.Rect(button_x, button_y + button_height + button_spacing, button_width, button_height)},
        {"text": "AIHard",
         "rect": p.Rect(button_x, button_y + 2 * button_height + 2 * button_spacing, button_width, button_height)}
    ]

    for button in buttons:
        p.draw.rect(screen, brown, button["rect"], border_radius=20)
        button_text = font.render(button["text"], True, white)
        button_text_rect = button_text.get_rect(center=button["rect"].center)
        screen.blit(button_text, button_text_rect)

    mouse = p.mouse.get_pos()
    mouse_click = p.mouse.get_pressed()
    for i, button in enumerate(buttons):
        if button["rect"].collidepoint(mouse):
            if mouse_click[0]:
                if i == 0:
                    game_state = 1
                elif i == 1:
                    game_state = 2
                elif i == 2:
                    game_state = 3
    return game_state

def random_pieces():
    pieces = [AnKing, AnQueen, AnPawn, AnKnight]
    if random.random() < 0.5:
        x = random.randint(0, 150)
    else:
        x = random.randint(460, width-80)
    y = -50
    random_piece = random.choices(pieces)[0]
    falling_pieces = (random_piece, [x, y])
    return falling_pieces


falling_piece = random_pieces()
falling_piece2 = random_pieces()

count = 0

def run():
    import main
    speed = 1.5
    global count, falling_piece, falling_piece2, game_state, game_run
    falling_piece[1][1] += speed
    clock.tick(FPS)
    for event in p.event.get():
        if event.type == p.QUIT:
            game_run = False
    screen.fill(p.color.THECOLORS["chartreuse4"])
    game_state = draw_menu()
    screen.blit(falling_piece[0], falling_piece[1])

    if falling_piece[1][1] > height/2:
        count = 1
    if count == 1:
        falling_piece2[1][1] += speed
        screen.blit(falling_piece2[0], falling_piece2[1])
    if falling_piece[1][1] > height:
        falling_piece = random_pieces()
    if falling_piece2[1][1] > height:
        falling_piece2 = random_pieces()

    if game_state != 0:
        main.set_game_state(game_state)

    p.display.flip()
    return game_run, game_state
def reset():
    global game_state
    game_state = 0
