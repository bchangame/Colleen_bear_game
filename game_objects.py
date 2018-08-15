import pygame
from game_globals import *
import random



class Ground(pygame.sprite.Sprite):
    x = 0
    y = 0

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(x=self.x, y=self.y)


class InfiniteBackground(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.image = pygame.image.load(image)
        self.y = H - y - self.image.get_rect().height
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def scroll_right(self):
        self.x -= SPEED
        if self.x == -self.rect.width:
            self.x = self.rect.width
        self.rect = self.image.get_rect(x=self.x, y=self.y)


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, image, name):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.image = pygame.image.load(image).convert_alpha()
        self.y = H - y - self.image.get_rect().height
        self.init_y = self.y
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
        if self.y - self.v >= self.init_y:
            self.y -= self.v
        else:
            self.v = 0
            self.y = self.init_y
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

    def place(self, x, y):
        self.x = x
        self.y = H - y - self.rect.height
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(x=self.x, y=self.y)


class Background(Item):
    def __init__(self, x, y):
        Item.__init__(self, x, y, "images/background.png", "background")

        self.at_edge_left = True
        self.at_edge_right = False
        self.at_edge_top = False
        self.at_edge_bottom = True

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


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        # Loading function
        self.image_right = pygame.image.load("images/bear_right.png").convert_alpha()
        self.image_left = pygame.image.load("images/bear.png").convert_alpha()
        self.image_crouch_left = pygame.image.load("images/bear_crouch_left.png").convert_alpha()
        self.image_crouch_right = pygame.image.load("images/bear_crouch_right.png").convert_alpha()
        self.image_climb = pygame.image.load("images/bear_climb.png").convert_alpha()

        self.image = self.image_right
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
        self.crouching_right = False
        self.crouching_left = False

        self.v = 0

        # for animation
        self.count = 0
        self.sprite_count = 0
        self.right = list()
        self.left = list()
        self.climb = list()

        for x in range(1, WALKING_FRAMES + 1):
            self.right.append(pygame.image.load("images/bear_right/"+str(x)+".png").convert_alpha())
            self.left.append(pygame.image.load("images/bear_left/"+str(x)+".png").convert_alpha())
            self.climb.append(pygame.image.load("images/bear_climb/"+str(x)+".png").convert_alpha())

    def move_left(self):
        self.crouching_right = False
        self.crouching_left = False
        if self.x >= SPEED:
            self.x -= SPEED
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def move_right(self):
        self.crouching_right = False
        self.crouching_left = False
        if self.x <= (W - self.rect.width):
            self.x += SPEED
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def climb_up(self):
        self.climbing = True
        self.y -= SPEED
        self.image = pygame.image.load("images/bear_climb.png").convert_alpha()
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def climb_down(self, on_ground):
        self.v = 0
        if not on_ground:
            self.y += SPEED
        else:
            self.climbing = False
            self.y = H - GROUND - self.rect.height
            self.image = self.image_right
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def crouch(self):
        self.animate = False
        self.y = H - GROUND - self.image_crouch_left.get_rect().height
        if self.walking_left:
            self.image = self.image_crouch_left
            self.walking_left = False
            self.crouching_left = True
        else:
            self.image = self.image_crouch_right
            self.walking_right = False
            self.crouching_right = True
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def stand(self):
        if self.crouching_left:
            self.image = self.image_left
            self.y = H - GROUND - self.image.get_rect().height
            self.crouching_left = False
        elif self.crouching_right:
            self.image = self.image_right
            self.y = H - GROUND - self.image.get_rect().height
            self.crouching_right = False
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def print_state(self):
        print("falling " + str(self.falling))
        print("climbing " + str(self.climbing))
        print("jumping " + str(self.jumping))
        print("Right " + str(self.walking_right))
        print("Left " + str(self.walking_left))
        print("ground " + str(ground))
        print("velocity " + str(self.v))

    def update(self, ground):
        # Animation
        if self.animate:
            self.count += 1
            if self.count > WALKING_FRAME_RATE:
                self.count = 0
                self.sprite_count = (self.sprite_count + 1) % WALKING_FRAMES

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



class Button(Item):
    def __init__(self, x, y, image, hover_image):
        Item.__init__(self, x, y, image, "button")
        self.hover_image = pygame.image.load(hover_image).convert_alpha()
        self.norm_image = self.image


class Sheep(Item):
    def __init__(self, x, y):
        Item.__init__(self, x, y, "images/sheep.png", "sheep")
        self.move = 0
        self.frame = 0
        self.image_right = self.image
        self.image_left = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.frame += 1
        if self.frame > 5:
            self.frame = 0
            if self.move >= 0:
                self.move = random.randint(-1, 5)
                if self.move >= 0:
                    self.move = 1
                else:
                    self.move = -1

            if self.move < 0:
                self.move = random.randint(-5, 1)
                if self.move > 0:
                    self.move = 1
                else:
                    self.move = -1

            if self.move < 0:
                self.image = self.image_left
            elif self.move > 0:
                self.image = self.image_right

            self.x += self.move * SPEED
            self.rect = self.image.get_rect(x=self.x, y=self.y)


class Knife(Item):
    def __init__(self, x, y):
        Item.__init__(self, x, y, "images/knife.png", "knife")


class SheepHeart(Item):
    def __init__(self, x, y):
        Item.__init__(self, x, y, "images/sheep_heart.png", "sheep heart")


class Tree(Item):
    def __init__(self, x, y):
        Item.__init__(self, x, y, "images/tree.png", "tree")


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


