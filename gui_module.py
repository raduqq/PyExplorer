import pygame
from pygame.locals import *
from math import sqrt

pygame.init()
pygame.font.init()

BUTTON_RADIUS = 15

FONT = "Courier"
FONT_SIZE = 25

PATH_WIDTH = 100
PATH_HEIGHT = 50

ICON_WIDTH = 30
ICON_HEIGHT = 30

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

WHITE = (255, 255, 255)
YELLOW = (255, 153, 0)
BLACK = (0, 0, 0)
RED = (204, 51, 0)

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
        self.text = self.game.font.render("X", False, BLACK)


    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = list(pygame.mouse.get_pos())
                dist = sqrt((pos[0] - self.position[0])**2 + (pos[1] - self.position[1])**2)

                if dist < BUTTON_RADIUS :
                    self.game.running = False

    def draw(self):
        pygame.draw.circle(self.game.window, YELLOW, (int(self.position[0]), int(self.position[1])), BUTTON_RADIUS)
        self.game.window.blit(self.text, (self.position[0] - 7, self.position[1] - 10))

class Highlighter(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)

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
        self.text = self.game.font.render(self.dir_list[-1], False, BLACK)

    def input(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_d:
                    # front
                    pass
                if event.key == K_a:
                    # back
                    pass
                if event.key == K_w:
                    # file up
                    pass
                if event.key == K_s:
                    # file down
                    pass
            # Sa se intample ceva daca ridici degetu de pe buton?
                    

    def update(self):
        # sa se draw-uiasca altfel nuj
        pass

    def draw(self):
        pygame.draw.rect(self.game.window, YELLOW, (self.position[0], self.position[1], self.position[0] + PATH_WIDTH, self.position[1] + PATH_HEIGHT), 5)
        self.game.window.blit(self.text, (self.position[0] + PATH_WIDTH // 6, self.position[1] + PATH_HEIGHT // 4))


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('PyExplorer')
        pygame.time.Clock().tick(60)
        self.running = True
        self.font = pygame.font.SysFont(FONT, FONT_SIZE)

        # Aici instantiez nebunii
        self.close_butt = CloseButton(self, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])
        self.file = File(self, [15, 100], "Testfile")
        self.directory = Directory(self, [15, 130], "Testdir")
        self.filepath = Filepath(self, (0, 0), ["Root", "Dir_1", "Dir_2"])
        self.gameObjects = [self.close_butt, self.file, self.directory, self.filepath]

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