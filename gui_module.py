import pygame
from pygame.locals import *
from math import sqrt
from os_module import MyOS
import os

pygame.init()
pygame.font.init()

HIGHLIGHT_OFFSET = 2
FILE_TEXT_OFFSET_X = 35
FILE_TEXT_OFFSET_Y = 7.5

BORDER_THICKNESS = 2

TEXT_TO_RECT_WIDTH_RATIO = 10
TEXT_TO_RECT_HEIGHT_RATIO = 5

NAV_BUTTON_SIZE = 40
BUTTON_RADIUS = 15

FONT = "Courier"

FONT_SIZE = 20

PATH_WIDTH = 140
PATH_HEIGHT = 40

ICON_WIDTH = 30
ICON_HEIGHT = 30

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

WHITE = (255, 255, 255)
YELLOW = (255, 153, 0)
BLACK = (0, 0, 0)
RED = (204, 51, 0)
BLUE = (50, 143, 168)

CHANGE_BACK = 1
CHANGE_FRONT = 2
CHANGE_PARENT = 3
CHANGE_CHILD = 4
CHANGE_DIR = 5

FILE_X_START = 15
FILE_Y_START = 100

class GameObject:
    def __init__(self, game, position):
        self.game = game
        self.position = position

    def input(self, events):
        pass

    def update(self):   
        pass

    def draw(self):
        pass

class CloseButton(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)
        self.text = self.game.font.render("X", False, BLACK, 1)

    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = list(pygame.mouse.get_pos())
                dist = sqrt((pos[0] - self.position[0])**2 + (pos[1] - self.position[1])**2)

                if dist < BUTTON_RADIUS :
                    self.game.running = False

    def draw(self):
        pygame.draw.circle(self.game.window, YELLOW, (int(self.position[0]), int(self.position[1])), BUTTON_RADIUS)
        pygame.draw.circle(self.game.window, BLACK, (int(self.position[0]), int(self.position[1])), BUTTON_RADIUS, BORDER_THICKNESS)
        self.game.window.blit(self.text, (self.position[0] - 5, self.position[1] - 10))

class File(GameObject):
    def __init__(self, game, position, name):
        super().__init__(game, position)
        self.name = name
        self.icon = pygame.image.load(self.game.initial_dir + "/file_icon.png")
        self.icon = pygame.transform.scale(self.icon, (ICON_WIDTH, ICON_HEIGHT))
        self.text = self.game.font.render(self.name, False, BLACK)

    def draw(self):
        self.game.window.blit(self.icon, self.position)
        self.game.window.blit(self.text, (self.position[0] + FILE_TEXT_OFFSET_X, self.position[1] + FILE_TEXT_OFFSET_Y))
        
    def update(self):
        self.draw()
    
class Directory(GameObject):    
    def __init__(self, game, position, name):
        super().__init__(game, position)
        self.name = name
        self.icon = pygame.image.load(self.game.initial_dir + "/dir_icon.png")
        self.icon = pygame.transform.scale(self.icon, (ICON_WIDTH, ICON_HEIGHT))
        self.text = self.game.font.render(self.name, False, BLACK)

    def draw(self):
        self.game.window.blit(self.icon, self.position)
        self.game.window.blit(self.text, (self.position[0] + FILE_TEXT_OFFSET_X, self.position[1] + FILE_TEXT_OFFSET_Y))

    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = list(pygame.mouse.get_pos())
                dist_x = pos[0] - self.position[0]
                dist_y = pos[1] - self.position[1]

                if (dist_x > 0 and dist_y > 0) and (dist_x < ICON_WIDTH and dist_y < ICON_HEIGHT):
                    self.game.code = CHANGE_CHILD
                    self.game.explorer.change_dir_child(self.name)

    def update(self):
        self.draw()

class Filepath(GameObject):
    def __init__(self, game, position, curr_dir):
        super().__init__(game, position)
        self.curr_dir = curr_dir

    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = list(pygame.mouse.get_pos())
                dist_x = pos[0] - self.position[0]
                dist_y = pos[1] - self.position[1]

                if (dist_x > 0 and dist_y > 0) and (dist_x < PATH_WIDTH and dist_y < PATH_HEIGHT):
                    self.game.code = CHANGE_DIR
                    # self.game.explorer.change_dir(self.curr_dir)
                    print(self.curr_dir)

    def draw(self):
        text = self.game.font.render(self.curr_dir, False, BLACK)

        pygame.draw.rect(self.game.window, YELLOW, (self.position[0], self.position[1], PATH_WIDTH, PATH_HEIGHT), 0)
        pygame.draw.rect(self.game.window, BLACK, (self.position[0], self.position[1], PATH_WIDTH, PATH_HEIGHT), BORDER_THICKNESS)
        self.game.window.blit(text, (self.position[0] + PATH_WIDTH // TEXT_TO_RECT_WIDTH_RATIO, self.position[1] + PATH_HEIGHT // TEXT_TO_RECT_HEIGHT_RATIO))

    def update(self):
        self.draw()

class FrontButton(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)
        self.text = self.game.font.render(">", False, BLACK, 1)

    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = list(pygame.mouse.get_pos())
                dist_x = pos[0] - self.position[0]
                dist_y = pos[1] - self.position[1]

                if (dist_x > 0 and dist_y > 0) and (dist_x < NAV_BUTTON_SIZE and dist_y < NAV_BUTTON_SIZE):
                    self.game.code = CHANGE_FRONT
                    self.game.explorer.change_dir_next()

    def draw(self):
        pygame.draw.rect(self.game.window, YELLOW, (self.position[0], self.position[1], NAV_BUTTON_SIZE, NAV_BUTTON_SIZE), 0)
        pygame.draw.rect(self.game.window, BLACK, (self.position[0], self.position[1], NAV_BUTTON_SIZE, NAV_BUTTON_SIZE), BORDER_THICKNESS)
        self.game.window.blit(self.text, (self.position[0] + NAV_BUTTON_SIZE // 3, self.position[1] + NAV_BUTTON_SIZE // 3))

class BackButton(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)
        self.text = self.game.font.render("<", False, BLACK, 1)

    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = list(pygame.mouse.get_pos())
                dist_x = pos[0] - self.position[0]
                dist_y = pos[1] - self.position[1]

                if (dist_x > 0 and dist_y > 0) and (dist_x < NAV_BUTTON_SIZE and dist_y < NAV_BUTTON_SIZE):
                    self.game.code = CHANGE_BACK
                    self.game.explorer.change_dir_previous()

    def draw(self):
        pygame.draw.rect(self.game.window, YELLOW, (self.position[0], self.position[1], NAV_BUTTON_SIZE, NAV_BUTTON_SIZE), 0)
        pygame.draw.rect(self.game.window, BLACK, (self.position[0], self.position[1], NAV_BUTTON_SIZE, NAV_BUTTON_SIZE), BORDER_THICKNESS)
        self.game.window.blit(self.text, (self.position[0] + NAV_BUTTON_SIZE // 3, self.position[1] + NAV_BUTTON_SIZE // 3))

class Game:
    def __init__(self, curr_dir, code):
        self.code = code
        self.initial_dir = curr_dir
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        pygame.display.set_caption('PyExplorer')
        pygame.time.Clock().tick(60)
        
        self.running = True
        self.font = pygame.font.SysFont(FONT, FONT_SIZE)
        
        # Explorer
        self.explorer = MyOS(curr_dir)
        
        # Dynamic objects
        self.dir_objects = [Directory(self, [FILE_X_START, FILE_Y_START + (i * 30)], name) for i, name in enumerate(self.explorer.get_dir_list())]
        curr_counter = len(self.dir_objects)
        self.file_objects = [File(self, [FILE_X_START, FILE_Y_START + ((i + curr_counter) * 30)], name) for i, name in enumerate(self.explorer.get_file_list())]
        self.filepath = [Filepath(self, (2 * NAV_BUTTON_SIZE + i * PATH_WIDTH, 0), dir) for i, dir in enumerate(self.explorer.get_path_list())]
        # self.highlighter = [Highlighter(self, (2 * NAV_BUTTON_SIZE, 0), self.explorer.get_path_list(), self.explorer.get_dir().split("/")[-1])]
        self.temp_objects = self.dir_objects + self.file_objects + self.filepath # update_files

        # Constant objects
        self.front_butt = FrontButton(self, (NAV_BUTTON_SIZE,0))
        self.back_butt = BackButton(self, (0, 0))
        self.close_butt = CloseButton(self, [SCREEN_WIDTH - BUTTON_RADIUS, BUTTON_RADIUS])
        self.const_objects = [self.back_butt, self.close_butt, self.front_butt]

    def run(self):
        while self.running == True:
            # Game logic happens here
            self.input()
            self.update()
            self.draw()

    def input(self):
        events = pygame.event.get()
        for gameObject in self.const_objects:
            gameObject.input(events)
        for gameObject in self.temp_objects:
            gameObject.input(events)
    
    def update(self):
        self.explorer.update()

        self.dir_objects = [Directory(self, [FILE_X_START, FILE_Y_START + (i * 30)], name) for i, name in enumerate(self.explorer.get_dir_list())]
        curr_counter = len(self.dir_objects)
        self.file_objects = [File(self, [FILE_X_START, FILE_Y_START + ((i + curr_counter) * 30)], name) for i, name in enumerate(self.explorer.get_file_list())]
        self.filepath = [Filepath(self, (2 * NAV_BUTTON_SIZE + i * PATH_WIDTH, 0), dir) for i, dir in enumerate(self.explorer.get_path_list())]
        # self.highlighter = [Highlighter(self, (2 * NAV_BUTTON_SIZE, 0), self.explorer.get_path_list(), self.explorer.get_dir().split("/")[-1])]
        self.temp_objects = self.dir_objects + self.file_objects + self.filepath # update_files

        for gameObject in self.const_objects:
            gameObject.update()
        for gameObject in self.temp_objects:
            gameObject.update()

    def draw(self):
        self.window.fill(WHITE)

        for gameObject in self.const_objects:
            gameObject.draw()
        for gameObject in self.temp_objects:
            gameObject.draw()

        pygame.display.update()


def main():
    # Run game
    game = Game(os.getcwd(), 0)
    game.run()
    pygame.quit()

if __name__ == '__main__':
    main()

    #TODO: Front button
        # -> Cand dau back, imi taie din filepath => nu pot sa mai dau front inapoi
    #TODO: Highlighter
        # -> Sa arate directoru in care sunt
    #TODO: Clicking on a certain directory from filepath
        # -> explorer.change_dir() nu stie sa mearga decat in fata/spate => eu vreau undeva la mijlocul filepath-ului

'''
    DRAWING THE HIGHLIGHTER:

    pygame.draw.rect(self.game.window, BLUE, (self.position[0] + HIGHLIGHT_OFFSET, self.position[1] + HIGHLIGHT_OFFSET, PATH_WIDTH - 2 * HIGHLIGHT_OFFSET, PATH_HEIGHT - 2 *HIGHLIGHT_OFFSET))
    self.game.window.blit(self.text, (self.position[0] + PATH_WIDTH // TEXT_TO_RECT_WIDTH_RATIO, self.position[1] + PATH_HEIGHT // TEXT_TO_RECT_HEIGHT_RATIO))
'''
