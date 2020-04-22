import os
import pygame
from gui_module import Game

def main():
    starting_dir = input()

    # Check if the input is valid
    if (not os.path.isdir(starting_dir)):
        starting_dir = os.getcwd()
        
    # Run the explorer from the specified file
    game = Game(starting_dir)
    game.run()
    pygame.quit()

if __name__ == '__main__':
    main()
