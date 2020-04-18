from gui_module import Game
from os_module import MyOS
import pygame
import os

def main():
    # Run game
    #game = Game()
    #game.run()
    #pygame.quit()

    explorer = MyOS(os.getcwd())
    print(explorer.get_dir_list())
    print(explorer.get_file_list())
    print(explorer.get_path_list())


if __name__ == '__main__':
    main()
