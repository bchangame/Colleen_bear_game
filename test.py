import pygame
import sys
# * means everything
# pygame.locals has global variables
from pygame.locals import *


# GLOBAL VARIABLES--EDIT
W = 1600
H = 900
horizontalSprites = 1
verticalSprites = 3
WHITE = (255, 255, 255)
SPEED = 15
WITCH_WIDTH = 200
GROUND = 200


# classes
class Background(object):
    def __init__(self, init_x, init_y, image):
        self.x = init_x
        self.y = init_y
        self.image = pygame.image.load(image)
        self.size = self.image.get_rect().size

    def scroll_right(self):
        """This scrolls the background right when the character moves left."""
        self.x -= SPEED

    def scroll_left(self):
        """This scrolls the background left when the character moves right."""
        self.x += SPEED

# more classes


class Inventory(object):
    def __init__(self):
        self.sheep_heart = 0
        self.knife = 0


class Character(object):
    def __init__(self, x, y, image):
        self.x = x
        # Loading function
        self.image = pygame.image.load(image)
        self.size = self.image.get_rect().size
        self.y = H - y - WITCH_WIDTH
        # spriteX and sprite Y are the positions for the character on the sprite sheet
        self.spriteX = 0
        self.spriteY = 0
        # defines a rectangle around something for collision
        self.rect = Rect(self.x, self.y, WITCH_WIDTH, WITCH_WIDTH)

    def move_left(self):
        """This makes the character go faster than the background which is weird"""
        if self.x >= SPEED:
            self.x -= SPEED
            # left facing sprite
            # animation
            self.spriteX = 0
            self.spriteY = 0
            self.rect = Rect(self.x, self.y, WITCH_WIDTH, WITCH_WIDTH)

    def move_right(self):
        """This makes the character go faster than the background which is weird"""
        if self.x <= (W - WITCH_WIDTH):
            self.x += SPEED
            # right facing sprite
            self.spriteX = 0
            self.spriteY = self.size[0]
            self.rect = Rect(self.x, self.y, WITCH_WIDTH, WITCH_WIDTH)

# def climb_up(self, height):
# if self.y <= height - SPEED:



''' Instructions for Object-Adding:
1. Make a new class as below
2. Next, instantiate an object of the class you made in game __init__
3. Add a scroll method to scroll
'''


class Item(object):
    def __init__(self, x, y, image):
        self.x = x
        self.image = pygame.image.load(image)
        self.y = H - y - self.image.get_rect().height
        self.rect = self.image.get_rect(x = self.x, y = self.y)

    def scroll_right(self):
        """This makes other interactable objects scroll with the screen"""
        self.x -= SPEED
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def scroll_left(self):
        """This makes other interactable objects scroll with the screen"""
        self.x += SPEED
        self.rect = self.image.get_rect(x=self.x, y=self.y)


class GAME(object):
    def __init__(self):
        self.surface = pygame.display.set_mode((W, H))
        pygame.init()
        pygame.display.set_caption("This is a game.")

        self.background = Background(0, 0, "test_background.png")
        self.character = Character(100, GROUND, "Sulba_spriteSheet.png")
        self.sheep = Item(720, GROUND, "Untitled.png")
        self.sheep_heart = Item(720, GROUND, "sheep_heart.png")
        self.knife = Item(500, GROUND, "Knife.png")
        self.tree = Item(2000, GROUND, "tree.png")
        self.character_size = self.character.size
        self.inventory = Inventory()
        self.items = {'sheep', 'knife'}
        self.loops()

    def scroll(self, direction):
        if direction == "LEFT" and self.background.x <= (0 - SPEED):
            self.background.scroll_left()
            self.sheep.scroll_left()
            self.knife.scroll_left()
            self.sheep_heart.scroll_left()
            self.tree.scroll_left()
        elif direction == "RIGHT" and self.background.x >= (W - self.background.size[0] + SPEED):
            self.background.scroll_right()
            self.sheep.scroll_right()
            self.knife.scroll_right()
            self.sheep_heart.scroll_right()
            self.tree.scroll_right()

    def display_game(self):
        self.surface.blit(self.background.image, (self.background.x, self.background.y))
        self.surface.blit(self.character.image, (self.character.x, self.character.y),
                          (self.character.spriteX, self.character.spriteY, 200 / horizontalSprites,
                           400 / verticalSprites))
        self.surface.blit(self.tree.image, (self.tree.x, self.tree.y))

        if "sheep" in self.items:
            self.surface.blit(self.sheep.image, (self.sheep.x, self.sheep.y))
        if "knife" in self.items:
            self.surface.blit(self.knife.image, (self.knife.x, self.knife.y))
        if "sheep heart" in self.items:
            self.surface.blit(self.sheep_heart.image, (self.sheep_heart.x, self.sheep_heart.y))

        pygame.display.update()

    def loops(self):
        while True:
            self.surface.fill(WHITE)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                self.character.move_left()
                self.scroll("LEFT")
            if keys[K_RIGHT]:
                self.character.move_right()
                self.scroll("RIGHT")
            if self.character.rect.colliderect(self.sheep_heart.rect) and "sheep heart" in self.items:
                self.inventory.sheep_heart += 1
                self.items.remove("sheep heart")
            if self.character.rect.colliderect(self.knife.rect) and "knife" in self.items:
                self.inventory.knife += 1
                self.items.remove("knife")
            if self.character.rect.colliderect(self.sheep.rect) and self.inventory.knife and "sheep" in self.items:
                self.items.remove("sheep")
                self.items.add("sheep heart")
            self.display_game()


GAME()