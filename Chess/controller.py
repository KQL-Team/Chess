import main
import menu
import config as cg
game_state = cg.GAME_STATE
game_run = cg.game_run
check = True
while game_run:
    if game_state == 0:
        if  not check:
            menu.reset()
        check = True
        game_run, game_state = menu.run()
    else:
        if check:
            main.reset_board()
            main.reset()
            check = False
        game_run, game_state = main.main()

