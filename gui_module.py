import pygame
from pygame.locals import *
from math import sqrt
from os_module import MyOS
import os

pygame.init()
pygame.font.init()

HIGHLIGHT_OFFSET = 2

BORDER_THICKNESS = 2

TEXT_TO_RECT_WIDTH_RATIO = 10
TEXT_TO_RECT_HEIGHT_RATIO = 5

NAV_BUTTON_SIZE = 40
BUTTON_RADIUS = 15

FONT = "Courier"

FONT_SIZE = 20

PATH_WIDTH = 90
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
        self.icon = pygame.image.load("file_icon.png")
        self.icon = pygame.transform.scale(self.icon, (ICON_WIDTH, ICON_HEIGHT))
        self.text = self.game.font.render(self.name, False, BLACK)

    def draw(self):
        self.game.window.blit(self.icon, self.position)
        self.game.window.blit(self.text, (self.position[0] + 35, self.position[1] + 7.5))

    def update(self):
        pass
        
class Directory(GameObject):    
    def __init__(self, game, position, name):
        super().__init__(game, position)
        self.name = name
        self.icon = pygame.image.load("dir_icon.png")
        self.icon = pygame.transform.scale(self.icon, (ICON_WIDTH, ICON_HEIGHT))
        self.text = self.game.font.render(self.name, False, BLACK)

    def draw(self):
        self.game.window.blit(self.icon, self.position)
        self.game.window.blit(self.text, (self.position[0] + 35, self.position[1] + 7.5))

class Filepath(GameObject):
    def __init__(self, game, position, dir_list):
        super().__init__(game, position)
        self.dir_list = dir_list

    def input(self, events):
        pass

    def draw(self):
        cnt = 0
        for dir in self.dir_list:   
            text = self.game.font.render(dir, False, BLACK)
            pygame.draw.rect(self.game.window, YELLOW, (self.position[0] + PATH_WIDTH * cnt , self.position[1], PATH_WIDTH, PATH_HEIGHT), 0)
            pygame.draw.rect(self.game.window, BLACK, (self.position[0] + PATH_WIDTH * cnt, self.position[1], PATH_WIDTH, PATH_HEIGHT), BORDER_THICKNESS)
            self.game.window.blit(text, (self.position[0] + PATH_WIDTH * cnt + PATH_WIDTH // TEXT_TO_RECT_WIDTH_RATIO, self.position[1] + PATH_HEIGHT // TEXT_TO_RECT_HEIGHT_RATIO))
            cnt += 1

    def update(self):
        self.draw()
        pass

class Highlighter(Filepath):
    def __init__(self, game, position, dir_list, curr_dir):
        super().__init__(game, position, dir_list)
        self.curr_dir = curr_dir
        self.text = self.game.font.render(self.curr_dir, False, BLACK)

    def draw(self):
        cnt = 0
        for dir in self.dir_list:
            if self.curr_dir == dir:
                break
            cnt += 1

        pygame.draw.rect(self.game.window, BLUE, (self.position[0] + PATH_WIDTH * (cnt - 1) + HIGHLIGHT_OFFSET, self.position[1] + HIGHLIGHT_OFFSET, PATH_WIDTH - 2 * HIGHLIGHT_OFFSET, PATH_HEIGHT - 2 *HIGHLIGHT_OFFSET))
        self.game.window.blit(self.text, (self.position[0] + PATH_WIDTH * (cnt - 1) + PATH_WIDTH // TEXT_TO_RECT_WIDTH_RATIO, self.position[1] + PATH_HEIGHT // TEXT_TO_RECT_HEIGHT_RATIO))

    def update(self):
        # go deeper into filetree: self.position[0] + PATH_WIDTH ; else subtract
        pass    


class FrontButton(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)
        self.text = self.game.font.render(">", False, BLACK, 1)

    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                # TODO
                pass

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
                # TODO
                pass

    def draw(self):
        pygame.draw.rect(self.game.window, YELLOW, (self.position[0], self.position[1], NAV_BUTTON_SIZE, NAV_BUTTON_SIZE), 0)
        pygame.draw.rect(self.game.window, BLACK, (self.position[0], self.position[1], NAV_BUTTON_SIZE, NAV_BUTTON_SIZE), BORDER_THICKNESS)
        self.game.window.blit(self.text, (self.position[0] + NAV_BUTTON_SIZE // 3, self.position[1] + NAV_BUTTON_SIZE // 3))

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('PyExplorer')
        pygame.time.Clock().tick(60)
        self.running = True
        self.font = pygame.font.SysFont(FONT, FONT_SIZE)

        # "Static" buttons
        self.close_butt = CloseButton(self, [SCREEN_WIDTH - BUTTON_RADIUS, BUTTON_RADIUS])
        self.front_butt = FrontButton(self, (NAV_BUTTON_SIZE,0))
        self.back_butt = BackButton(self, (0, 0))

        # Get your initial path, file list, dir list
        os_module = MyOS(os.getcwd()) # Initializaza os_module la un director anume
        print(os_module.get_dir())


        # "Dynamic" stuff
        self.file = File(self, [15, 100], "Testfile")
        self.directory = Directory(self, [15, 130], "Testdir")
        self.filepath = Filepath(self, (2 * NAV_BUTTON_SIZE, 0), ["Root", "Dir_1", "Dir_2"])
        self.highlighter = Highlighter(self, (2 * NAV_BUTTON_SIZE, 0), ["Root", "Dir_1", "Dir_2"])
        
        self.gameObjects = [self.back_butt, self.close_butt, self.file, self.directory, self.filepath, self.highlighter, self.front_butt]

    def run(self):
        while self.running == True:
            # Game logic happens here
            self.input()
            self.update()
            self.draw()

    def input(self):
        events = pygame.event.get()
        for gameObject in self.gameObjects:
            gameObject.input(events)

    def update(self):
        for gameObject in self.gameObjects:
            gameObject.update()


    def draw(self):
        self.window.fill(WHITE)

        for gameObject in self.gameObjects:
            gameObject.draw()

        pygame.display.update()


def main():
    # Run game
    game = Game()
    game.run()
    pygame.quit()

if __name__ == '__main__':
    main()

    #TODO: ls, click directoare
    #TODO: Functionalitate click buton back/front
    #TODO: Update file path
    #TODO: Update highlighter
    #TODO: Modul draw_border