import pygame
from pygame.locals import *

WIDTH = 1280
HEIGHT = 720

YELLOW = (255, 153, 0)
BLACK = (0, 0, 0)
RED = (204, 51, 0)


MOVESPEED = 1

class GameObject:
    def __init__(self, game, position):
        self.game = game
        self.position = position
        self.velocity = [0, 0]

    def input(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass

class Smiley(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)

    def input(self, events):
        
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_d:
                    self.velocity[0] = MOVESPEED
                if event.key == K_a:
                    self.velocity[0] = -MOVESPEED
                if event.key == K_w:
                    self.velocity[1] = -MOVESPEED
                if event.key == K_s:
                    self.velocity[1] = MOVESPEED
            if event.type == KEYUP:
                if event.key == K_d:
                    self.velocity[0] = 0
                if event.key == K_a:
                    self.velocity[0] = 0
                if event.key == K_w:
                    self.velocity[1] = 0
                if event.key == K_s:
                    self.velocity[1] = 0
                    

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def draw(self):
        pygame.draw.circle(self.game.window, YELLOW, (int(self.position[0]), int(self.position[1])), 200)
        pygame.draw.circle(self.game.window, BLACK, (int(self.position[0]) - 100, int(self.position[1]) - 100), 50)
        pygame.draw.circle(self.game.window, BLACK, (int(self.position[0]) + 100, int(self.position[1]) - 100), 50)
        pygame.draw.ellipse(self.game.window, BLACK, (int(self.position[0]) - 150, int(self.position[1]) + 100, 300, 50))
        pygame.draw.rect(self.game.window, RED, (int(self.position[0]) - 30, int(self.position[1]) + 110, 60, 30))

class Game:

    def __init__(self):
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('Demo')
        pygame.time.Clock().tick(60)
        self.smiley = Smiley(self, [WIDTH // 2, HEIGHT // 2])
        self.gameObjects = [self.smiley]

    def run(self):
        while True:
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
        self.window.fill(BLACK)

        for gameObject in self.gameObjects:
            gameObject.draw()

        pygame.display.update()


def main():
    # Run game
    game = Game()
    game.run()

if __name__ == '__main__':
    main()