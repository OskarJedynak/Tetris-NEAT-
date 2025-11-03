import sys, pygame
from grid import Grid
from blocks import *

pygame.init()
backg_color = (22, 22, 22)

screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

game_grid = Grid()

block = IBlock()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(backg_color)
    game_grid.draw(screen)
    block.draw(screen)

    pygame.display.update()
    clock.tick(60)
