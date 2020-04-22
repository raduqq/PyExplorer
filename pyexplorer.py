import os
import pygame
from gui_module import Game

def main():
    game = Game(os.getcwd())
    game.run()
    pygame.quit()

if __name__ == '__main__':
    main()
