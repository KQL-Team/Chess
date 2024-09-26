import pygame
import main
import menu
game_run = False
choice = 0
while not game_run:
    game_run, choice = menu.run(game_run)
while choice and game_run:
    game_run = main.main(game_run)

