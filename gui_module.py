import pygame
import os
import constants as Const
from pygame.locals import *
from math import sqrt
from os_module import MyOS

pygame.init()
pygame.font.init()

# General object class
class GameObject:
    def __init__(self, game, position):
        self.game = game
        self.position = position

    def input(self, events):
        pass

    def draw(self):
        pass


class CloseButton(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)
        self.text = self.game.font.render("X", False, Const.BLACK, 1)

    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                # Determining if the click was on the close button
                pos = list(pygame.mouse.get_pos())
                dist = sqrt((pos[0] - self.position[0])**2 +
                            (pos[1] - self.position[1])**2)

                if dist < Const.BUTTON_RADIUS:
                    self.game.running = False

    def draw(self):
        pygame.draw.circle(self.game.window, Const.YELLOW, (int(
            self.position[0]), int(self.position[1])), Const.BUTTON_RADIUS)
        pygame.draw.circle(self.game.window, Const.BLACK, (int(self.position[0]), int(
            self.position[1])), Const.BUTTON_RADIUS, Const.BORDER_THICKNESS)

        self.game.window.blit(
            self.text, (self.position[0] - Const.CLOSE_BUTTON_TEXT_OFFSET, self.position[1] - Const.CLOSE_BUTTON_TEXT_OFFSET * 2))


class File(GameObject):
    def __init__(self, game, position, name):
        super().__init__(game, position)
        self.name = name

        # Scaling image to standard size
        self.icon = pygame.image.load(self.game.initial_dir + "/file_icon.png")
        self.icon = pygame.transform.scale(
            self.icon, (Const.ICON_WIDTH, Const.ICON_HEIGHT))

        self.text = self.game.font.render(self.name, False, Const.BLACK)

    def draw(self):
        self.game.window.blit(self.icon, self.position)
        self.game.window.blit(
            self.text, (self.position[0] + Const.FILE_TEXT_OFFSET_X, self.position[1] + Const.FILE_TEXT_OFFSET_Y))


class Directory(GameObject):
    def __init__(self, game, position, name):
        super().__init__(game, position)
        self.name = name

        # Scaling image to standard size
        self.icon = pygame.image.load(self.game.initial_dir + "/dir_icon.png")
        self.icon = pygame.transform.scale(
            self.icon, (Const.ICON_WIDTH, Const.ICON_HEIGHT))

        self.text = self.game.font.render(self.name, False, Const.BLACK)

    def draw(self):
        self.game.window.blit(self.icon, self.position)
        self.game.window.blit(
            self.text, (self.position[0] + Const.FILE_TEXT_OFFSET_X, self.position[1] + Const.FILE_TEXT_OFFSET_Y))

    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = list(pygame.mouse.get_pos())
                dist_x = pos[0] - self.position[0]
                dist_y = pos[1] - self.position[1]

                # Determining if click was on directory icon
                if (dist_x > 0 and dist_y > 0) and (dist_x < Const.ICON_WIDTH and dist_y < Const.ICON_HEIGHT) and self.game.code == Const.NO_CHANGE:
                    self.game.code = Const.CHANGE_CHILD
                    self.game.filename = self.name


class Highlighter(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)

    def draw(self):
        # Determining position of highlighter in filepath
        counter = self.game.explorer.get_counter()
        my_text = self.game.explorer.get_path_list()[counter]
        text = self.game.font.render(my_text, False, Const.BLACK)

        pygame.draw.rect(self.game.window, Const.BLUE, (
            self.position[0] + counter * Const.PATH_WIDTH + 2, self.position[1] + 2, Const.PATH_WIDTH - 4, Const.PATH_HEIGHT - 4))
        self.game.window.blit(text, (self.position[0] + Const.PATH_WIDTH // Const.TEXT_TO_RECT_WIDTH_RATIO +
                                     counter * Const.PATH_WIDTH, self.position[1] + Const.PATH_HEIGHT // Const.TEXT_TO_RECT_HEIGHT_RATIO))


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

                # Determining if click was on a certain directory from filepath
                if (dist_x > 0 and dist_y > 0) and (dist_x < Const.PATH_WIDTH and dist_y < Const.PATH_HEIGHT) and self.game.code == Const.NO_CHANGE:
                    self.game.code = Const.CHANGE_PATH
                    self.game.filename = self.curr_dir

    def draw(self):
        text = self.game.font.render(self.curr_dir, False, Const.BLACK)

        pygame.draw.rect(self.game.window, Const.YELLOW, (
            self.position[0], self.position[1], Const.PATH_WIDTH, Const.PATH_HEIGHT), 0)
        pygame.draw.rect(self.game.window, Const.BLACK, (
            self.position[0], self.position[1], Const.PATH_WIDTH, Const.PATH_HEIGHT), Const.BORDER_THICKNESS)
        self.game.window.blit(text, (self.position[0] + Const.PATH_WIDTH // Const.TEXT_TO_RECT_WIDTH_RATIO,
                                     self.position[1] + Const.PATH_HEIGHT // Const.TEXT_TO_RECT_HEIGHT_RATIO))


class FrontButton(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)
        self.text = self.game.font.render(">", False, Const.BLACK, 1)

    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = list(pygame.mouse.get_pos())
                dist_x = pos[0] - self.position[0]
                dist_y = pos[1] - self.position[1]

                # If front button was clicked
                if (dist_x > 0 and dist_y > 0) and (dist_x < Const.NAV_BUTTON_SIZE and dist_y < Const.NAV_BUTTON_SIZE) and self.game.code == Const.NO_CHANGE:
                    self.game.code = Const.CHANGE_FRONT

    def draw(self):
        pygame.draw.rect(self.game.window, Const.YELLOW, (
            self.position[0], self.position[1], Const.NAV_BUTTON_SIZE, Const.NAV_BUTTON_SIZE), 0)
        pygame.draw.rect(self.game.window, Const.BLACK, (
            self.position[0], self.position[1], Const.NAV_BUTTON_SIZE, Const.NAV_BUTTON_SIZE), Const.BORDER_THICKNESS)
        self.game.window.blit(
            self.text, (self.position[0] + Const.NAV_BUTTON_SIZE // 3, self.position[1] + Const.NAV_BUTTON_SIZE // 3))


class BackButton(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position)
        self.text = self.game.font.render("<", False, Const.BLACK, 1)

    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = list(pygame.mouse.get_pos())
                dist_x = pos[0] - self.position[0]
                dist_y = pos[1] - self.position[1]

                # If back button was clicked
                if (dist_x > 0 and dist_y > 0) and (dist_x < Const.NAV_BUTTON_SIZE and dist_y < Const.NAV_BUTTON_SIZE) and self.game.code == Const.NO_CHANGE:
                    self.game.code = Const.CHANGE_BACK

    def draw(self):
        pygame.draw.rect(self.game.window, Const.YELLOW, (
            self.position[0], self.position[1], Const.NAV_BUTTON_SIZE, Const.NAV_BUTTON_SIZE), 0)
        pygame.draw.rect(self.game.window, Const.BLACK, (
            self.position[0], self.position[1], Const.NAV_BUTTON_SIZE, Const.NAV_BUTTON_SIZE), Const.BORDER_THICKNESS)
        self.game.window.blit(
            self.text, (self.position[0] + Const.NAV_BUTTON_SIZE // 3, self.position[1] + Const.NAV_BUTTON_SIZE // 3))


class Game:
    def __init__(self, curr_dir):
        self.code = Const.NO_CHANGE
        self.filename = ""
        self.initial_dir = os.getcwd()
        self.window = pygame.display.set_mode([Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT])

        pygame.display.set_caption('PyExplorer')
        pygame.time.Clock().tick(60)

        self.running = True
        self.font = pygame.font.SysFont(Const.FONT, Const.FONT_SIZE)

        # Explorer
        self.explorer = MyOS(curr_dir)

        # Dynamic objects
        self.temp_objects = []
        self.update_files()

        # Constant objects
        front_butt = FrontButton(self, (Const.NAV_BUTTON_SIZE, 0))
        back_butt = BackButton(self, (0, 0))
        close_butt = CloseButton(
            self, [Const.SCREEN_WIDTH - Const.BUTTON_RADIUS, Const.BUTTON_RADIUS])
        self.const_objects = [back_butt, close_butt, front_butt]

    # Update the files in the OS Module
    def update_files(self):
        dir_objects = [Directory(self, [Const.FILE_X_START, Const.FILE_Y_START + (i * 30)], name)
                       for i, name in enumerate(self.explorer.get_dir_list())]
        curr_counter = len(dir_objects)
        file_objects = [File(self, [Const.FILE_X_START, Const.FILE_Y_START + ((i + curr_counter) * 30)], name)
                        for i, name in enumerate(self.explorer.get_file_list())]
        filepath = [Filepath(self, (2 * Const.NAV_BUTTON_SIZE + i * Const.PATH_WIDTH, 0), dir)
                    for i, dir in enumerate(self.explorer.get_path_list())]
        highlighter = [Highlighter(self, (2 * Const.NAV_BUTTON_SIZE, 0))]
        self.temp_objects = dir_objects + file_objects + filepath + highlighter

    def run(self):
        while self.running:
            # Game logic happens here
            self.input()
            self.update()
            self.draw()

    def input(self):
        events = pygame.event.get()
        self.code = Const.NO_CHANGE
        self.filename = ""

        for game_object in self.const_objects:
            game_object.input(events)
        for game_object in self.temp_objects:
            game_object.input(events)

    def update(self):
        # All updates happen through codes
        # Determined by user input
        if self.code == Const.CHANGE_BACK:
            self.explorer.change_dir_previous()
        elif self.code == Const.CHANGE_FRONT:
            self.explorer.change_dir_next()
        elif self.code == Const.CHANGE_CHILD:
            self.explorer.change_dir_child(self.filename)
        elif self.code == Const.CHANGE_PATH:
            self.explorer.change_dir_path(self.filename)
        self.update_files()

    def draw(self):
        self.window.fill(Const.WHITE)

        for game_object in self.const_objects:
            game_object.draw()
        for game_object in self.temp_objects:
            game_object.draw()

        pygame.display.update()
