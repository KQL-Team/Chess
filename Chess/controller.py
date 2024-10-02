import main
import menu
import config as cg
game_state = cg.GAME_STATE
game_run = cg.game_run
check = True
while game_run:
    if game_state == 0:
        game_run, game_state = menu.run()
        if  not check:
            menu.reset()
        check = True
    else:
        game_run, game_state = main.main()
        if check:
            main.reset()
            check = False
