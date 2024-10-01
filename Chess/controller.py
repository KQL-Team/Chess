import main
import menu
import config as cg
game_state = cg.GAME_STATE
game_run = cg.game_run
while game_run:
    if game_state == 0:
        game_run, game_state = menu.run()
    if game_state == 1:
        game_run = main.main()

