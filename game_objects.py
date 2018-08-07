import pygame
from game_globals import *


class Ground(pygame.sprite.Sprite):
    x = 0
    y = 0

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(x=self.x, y=self.y)


class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.image = pygame.image.load(image)
        self.mask = pygame.mask.from_surface(self.image)
        self.y = H - y - self.image.get_rect().height
        self.rect = self.image.get_rect(x=self.x, y=self.y)

        self.at_edge_left = True
        self.at_edge_right = False
        self.at_edge_top = False
        self.at_edge_bottom = True
        self.v = 0

    def scroll_down(self, climbing):
        if climbing:
            self.v = SPEED
        else:
            self.v += GRAVITY
        if self.rect.bottom - self.v >= H - GROUND:
            self.y -= self.v
        else:
            self.y = H - GROUND - self.rect.height
            self.at_edge_bottom = True
        self.at_edge_top = False
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def scroll_up(self):
        self.y += SPEED
        if self.y == 0:
            self.at_edge_top = True
        self.at_edge_bottom = False
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def scroll_right(self):
        self.x -= SPEED
        if self.x == W - self.rect.width:
            self.at_edge_right = True
        self.at_edge_left = False
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def scroll_left(self):
        self.x += SPEED
        if self.x == 0:
            self.at_edge_left = True
        self.at_edge_right = False
        self.rect = self.image.get_rect(x=self.x, y=self.y)

# more classes


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        # Loading function
        self.image = pygame.image.load("bear_right/1.png").convert_alpha()
        self.image_right = pygame.image.load("bear_right.png").convert_alpha()
        self.image_left = pygame.image.load("bear.png").convert_alpha()
        self.image_climb = pygame.image.load("bear_climb.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.y = H - y - self.image.get_rect().height
        self.rect = self.image.get_rect(x=self.x, y=self.y)

        self.climbing = False
        self.jumping = False
        self.walking_left = False
        self.walking_right = False
        self.falling = False
        self.animate = False
        self.could_climb = False

        self.v = 0

        self.count = 0
        self.sprite_count = 0
        self.right = list()
        self.left = list()
        self.climb = list()

        for x in range(1, 4):
            self.right.append(pygame.image.load("bear_right/"+str(x)+".png").convert_alpha())
            self.left.append(pygame.image.load("bear_left/"+str(x)+".png").convert_alpha())
            self.climb.append(pygame.image.load("bear_climb/"+str(x)+".png").convert_alpha())

    def move_left(self):
        if self.x >= SPEED:
            self.x -= SPEED
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def move_right(self):
        if self.x <= (W - self.rect.width):
            self.x += SPEED
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def climb_up(self):
        self.climbing = True
        self.y -= SPEED
        self.image = pygame.image.load("bear_climb.png").convert_alpha()
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def climb_down(self, on_ground):
        self.v = 0
        if not on_ground:
            self.y += SPEED
            #self.image = self.image_climb
        else:
            self.climbing = False
            self.y = H - GROUND - self.rect.height
            self.image = self.image_right
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def update(self, ground):
        #print("falling " + str(self.falling))
        #print("climbing " + str(self.climbing))
        #print("jumping " + str(self.jumping))
        #print("Right " + str(self.walking_right))
        #print("Left " + str(self.walking_left))
        #print("ground " + str(ground))
        #print("velocity " + str(self.v))

        # Animation
        if self.animate:
            self.count += 1
            if self.count > 1:
                self.count = 0
                self.sprite_count = (self.sprite_count + 1) % 3
            if self.walking_left:
                self.image = self.left[self.sprite_count]
            if self.walking_right:
                self.image = self.right[self.sprite_count]
            if self.climbing:
                self.image = self.climb[self.sprite_count]
        else:
            if self.walking_right:
                self.image = self.image_right
            if self.walking_left:
                self.image = self.image_left
            if self.climbing:
                self.image = self.image_climb

        if not self.climbing and self.falling:
            self.v += GRAVITY
            if self.rect.bottom + self.v <= ground:
                self.y += self.v

            else:
                self.v = 0
                self.jumping = False
                self.falling = False
                self.y = ground - self.rect.height
        self.rect = self.image.get_rect(x=self.x, y=self.y)


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, image, name):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.image = pygame.image.load(image).convert_alpha()
        self.y = H - y - self.image.get_rect().height
        self.inity = self.y
        self.inventory_sprite = InventoryItem(0, 0, image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(x=self.x, y=self.y)
        self.name = name
        self.v = 0

    def scroll_down(self, climbing):
        if climbing:
            self.v = SPEED
        else:
            self.v += GRAVITY
        if self.y - self.v >= self.inity:
            self.y -= self.v
        else:
            self.v = 0
            self.y = self.inity
            #self.y = H - GROUND - self.rect.height
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def scroll_up(self):
        """This makes other interactable objects scroll with the screen"""
        self.y += SPEED
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def scroll_right(self):
        """This makes other interactable objects scroll with the screen"""
        self.x -= SPEED
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def scroll_left(self):
        """This makes other interactable objects scroll with the screen"""
        self.x += SPEED
        self.rect = self.image.get_rect(x=self.x, y=self.y)


class Inventory(Item):
    def __init__(self, x, y, image):
        Item.__init__(self, x, y, image, "inventory")
        self.dictionary = {}
        self.i = 0
        self.matrix = []


class InventoryItem(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.number = 0
        self.x = x
        self.y = y
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(x=self.x, y=self.y)


