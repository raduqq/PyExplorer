import pygame
from pygame.locals import *

WIDTH = 1280
HEIGHT = 720

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

    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.game.running = False
                # Close pygame
                pass            

    def draw(self):
        pygame.draw.circle(self.game.window, YELLOW, (int(self.position[0]), int(self.position[1])), 25)

class Highlighter(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)

class File(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)

class Directory(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)

class Filepath(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)

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
        # TODO 
        pass

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('PyExplorer')
        pygame.time.Clock().tick(60)
        self.running = True

        # Aici instantiez nebunii
        self.close_butt = CloseButton(self, [WIDTH // 2, HEIGHT // 2])
        self.gameObjects = [self.close_butt]

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