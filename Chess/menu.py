from modes import AIEasy, AIHard, pvp
import pygame as p
import random
import warnings
import math
warnings.simplefilter(action='ignore', category=FutureWarning)

p.init()

width = height = 512
screen = p.display.set_mode((width, height))
p.display.set_caption("King of Rap")
FPS = 120
AnKing = p.transform.rotate(p.transform.scale(p.image.load("Images/king.png"), (75, 75)),40)
AnQueen = p.transform.rotate(p.transform.scale(p.image.load("Images/queen.png"), (75, 75)),40)
AnPawn = p.transform.rotate(p.transform.scale(p.image.load("Images/pawn.png"), (75, 75)),40)
AnKnight = p.transform.rotate(p.transform.scale(p.image.load("Images/knight.png"), (75, 75)),40)

font = p.font.Font(None, 36)
brown = p.color.THECOLORS["brown"]
black = p.color.THECOLORS["black"]
white = p.color.THECOLORS["seashell1"]
gray = p.color.THECOLORS["grey44"]

def draw_menu():
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
        {"text": "AIEasy", "rect": p.Rect(button_x, button_y + button_height + button_spacing, button_width, button_height)},
        {"text": "AIHard", "rect": p.Rect(button_x, button_y + 2 * button_height + 2 * button_spacing, button_width, button_height)}
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
                    p.quit()
                elif i == 1:
                    p.quit()
                    # Thêm mã để gọi file chế độ AIEasy
                elif i == 2:
                    p.quit()
                    # Thêm mã để gọi file chế độ AIHard

def random_pieces():
    pieces = [AnKing, AnQueen, AnPawn, AnKnight]
    x = random.randint(0, width - 20)
    y = -50
    random_piece = random.choices(pieces)[0]
    falling_pieces = (random_piece, [x,y])
    return falling_pieces

running = True
clock = p.time.Clock()
falling_piece = random_pieces()
while running:
    falling_piece[1][1] += 1
    clock.tick(FPS)
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
    screen.fill(p.color.THECOLORS["chartreuse4"])  
    draw_menu()
    screen.blit(falling_piece[0], falling_piece[1])
    if(falling_piece[1][1]>height):
        falling_piece = random_pieces()
    p.display.flip()
p.quit()
