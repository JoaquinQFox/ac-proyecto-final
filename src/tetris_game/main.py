import pygame, sys
from grid import Grid

dark_blue = (44, 44, 127)

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

game_grid = Grid()

game_grid.grid[19][0] = 1
game_grid.grid[1][0] = 4
game_grid.grid[0][1] = 7
game_grid.grid[2][3] = 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # DRAWING
    screen.fill(dark_blue)
    game_grid.draw(screen)
    pygame.display.update()
    clock.tick(60)
