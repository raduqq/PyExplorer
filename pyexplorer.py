from gui_module import Game
from os_module import MyOS
import pygame
import os

def main():
    # Run game
    game = Game(os.getcwd())
    game.run()
    pygame.quit()

if __name__ == '__main__':
    main()