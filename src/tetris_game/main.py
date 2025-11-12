import pygame, sys
from game import Game


SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
dark_blue = (44, 44, 127)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: 
            if game.game_over == True:
                game.game_over = False
                game.reset()

            if event.key == pygame.K_a and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_d and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_s and game.game_over == False:
                game.move_down()
            if event.key == pygame.K_w and game.game_over == False:
                game.rotate()

        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()

    # DRAWING
    screen.fill(dark_blue)
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)
