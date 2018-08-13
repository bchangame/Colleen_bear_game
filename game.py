import sys
from pygame.locals import *
from game_objects import *
from game_globals import *


class GAME(object):
    def __init__(self):
        self.surface = pygame.display.set_mode((W, H))
        pygame.init()
        self.CLOCK = pygame.time.Clock()
        pygame.display.set_caption("")

        self.background = Background(0, GROUND, "images/background.png")
        self.character = Character(500, GROUND)
        self.inventory = Inventory(0, 0, "images/inventory.png")

        self.cave = Item(2060, GROUND, "images/cave.png", "cave")
        self.cave_entry = Item(2060, GROUND, "images/cave_entry.png", "cave entry")
        self.cave_front = Item(2060, GROUND, "images/frontcave.png", "cave front")
        self.sheep = Item(720, GROUND, "images/sheep.png", "sheep")
        self.sheep_heart = Item(720, GROUND, "images/sheep_heart.png", "sheep heart")
        self.knife = Item(500, 700, "images/knife.png", "knife")
        self.tree = Item(100, GROUND, "images/tree.png", "tree")
        self.nest = Item(0, GROUND + 1200, "images/nest.png", "nest")
        self.feather = Item(20, GROUND + 1220, "images/feather.png", "feather")
        self.knife = Item(200, GROUND, "images/knife.png", "knife")

        self.sprites_back = pygame.sprite.Group(self.sheep, self.cave_entry)
        self.sprites_mid = pygame.sprite.Group(self.tree, self.cave)
        self.sprites_front = pygame.sprite.Group(self.cave_front, self.knife)
        self.sprites_character = pygame.sprite.Group(self.character)

        self.sprites_scroll = pygame.sprite.Group(self.background, self.tree, self.knife, self.nest, self.feather,
                                                  self.sheep, self.sheep_heart, self.cave, self.cave_front, self.cave_entry)
        self.sprites_gettable = pygame.sprite.Group(self.sheep_heart, self.feather, self.knife)

        self.inventory_sprite = pygame.sprite.OrderedUpdates()
        self.item_sprites = pygame.sprite.Group(self.sheep_heart, self.knife)

        self.title_screen_scroll = 0
        self.play_button = Item(W/2 - 170, H/2, "images/play_button.png", "play button")
        self.title_background1 = InfiniteBackground(0, GROUND, "images/background.png")
        self.title_background2 = InfiniteBackground(self.title_background1.rect.width, GROUND, "images/background.png")
        self.title_screen_sprites = pygame.sprite.LayeredUpdates(self.title_background1, self.title_background2, self.play_button)

        self.pause = False
        self.on_surface = True

        self.title_screen()

    def scroll(self, direction):
        if direction == "LEFT" and not self.background.at_edge_left:
            for sprite in self.sprites_scroll:
                sprite.scroll_left()

        elif direction == "RIGHT" and not self.background.at_edge_right:
            for sprite in self.sprites_scroll:
                sprite.scroll_right()

        elif direction == "UP" and not self.background.at_edge_top:
            for sprite in self.sprites_scroll:
                sprite.scroll_up()

        elif direction == "DOWN" and not self.background.at_edge_bottom:
            for sprite in self.sprites_scroll:
                sprite.scroll_down(self.character.climbing)

    def display_game(self):
        self.surface.blit(self.background.image, (self.background.x, self.background.y))
        self.sprites_back.draw(self.surface)
        self.sprites_mid.draw(self.surface)
        self.sprites_character.draw(self.surface)
        self.sprites_front.draw(self.surface)
        for x in range(-GROUND, W+GROUND, GROUND):
            self.surface.blit(pygame.image.load("images/tile.png"), ((self.background.x % 200) + x,
                                                              self.background.rect.bottom - 50))

        self.inventory_sprite.draw(self.surface)
        pygame.display.update()

    def display_inventory(self):
        self.inventory_sprite.add(self.inventory)
        for item in self.inventory.dictionary.keys():
            # figure out how many of the item we have
            # display item in open square
            # display a transparent box with number of items in it
            print("%s: %d" % (item.name, self.inventory.dictionary[item]))
            print(self.inventory.i)
            if self.inventory.i <= 3:
                item.inventory_sprite.rect.y = 200
            else:
                print("more items")
                item.inventory_sprite.rect.y = 350

            item.inventory_sprite.rect.x = 900 + (150 * (self.inventory.i % 4))
            self.inventory_sprite.add(item.inventory_sprite)
            self.inventory.matrix.append((item, 100, 900 + (200 * self.inventory.i)))
            self.inventory.i += 1
        self.pause = True

    def dont_display_inventory(self):
        self.inventory_sprite.remove(self.inventory)
        for item in self.inventory.dictionary.keys():
            self.inventory_sprite.remove(item.inventory_sprite)
        self.pause = False
        self.inventory.i = 0

    def get_item(self, item):
        if item in self.inventory.dictionary.keys():
            self.inventory.dictionary[item] += 1
        else:
            self.inventory.dictionary[item] = 1

    def check_inventory(self, item):
        if item in self.inventory.dictionary.keys():
            return True
        else:
            return False

    def set_state(self):
        # Is the character on a surface (i.e. ground)
        if self.character.rect.bottom == self.background.rect.bottom or \
                (self.character.rect.bottom == (H-GROUND-640) and self.character.could_climb):
            self.on_surface = True
            self.character.falling = False
            self.character.jumping = False
            self.character.climbing = False

        else:
            self.on_surface = False
            self.character.falling = True

        # Is the character colliding with a climbable object
        if self.tree.rect.left + (self.tree.rect.width/3) < \
                self.character.rect.centerx < self.tree.rect.right - (self.tree.rect.width/3) or pygame.sprite.collide_mask(self.character, self.cave):
            self.character.could_climb = True
            if self.character.climbing:
                self.sprites_front.remove(self.cave_front)
        else:
            self.character.could_climb = False
            self.character.climbing = False
            self.sprites_front.add(self.cave_front)

    def title_screen(self):
        while True:
            self.surface.fill(WHITE)

            for event in pygame.event.get():
                # click on X in corner
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.play_button.rect.collidepoint(pos):
                        self.loops()

            self.title_background1.scroll_right()
            self.title_background2.scroll_right()

            self.title_screen_sprites.draw(self.surface)

            for x in range(-GROUND, W+GROUND, GROUND):
                self.surface.blit(pygame.image.load("images/tile.png"), ((self.title_background1.x % 200) + x,
                                                                         self.background.rect.bottom - 50))

            pygame.display.update()

    def loops(self):
        # Outer game loop, includes paused game and inventory
        while True:
            # Inner game loop, while not paused
            while not self.pause:
                self.surface.fill(WHITE)

                self.set_state()

                # Events to evaluate once, not continual input
                for event in pygame.event.get():
                    # click on X in corner
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit(0)

                    # Key events to evaluate once
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            self.display_inventory()
                        if event.key == pygame.K_p:
                            self.pause = True

                        if self.character.crouching_right or self.character.crouching_left and event.key == pygame.K_UP:
                            self.character.stand()

                        if not self.character.could_climb and event.key == pygame.K_DOWN:
                            self.character.crouch()

                        # Jumping
                        if event.key == pygame.K_SPACE and not self.character.climbing and self.on_surface:
                            self.character.jumping = True
                            self.character.falling = True
                            self.character.v = JUMP_VELOCITY

                        # Hiding behind things
                        if event.key == pygame.K_h and not self.character.climbing:
                            if self.sprites_character.has(self.character):
                                self.sprites_character.remove(self.character)
                                self.sprites_back.add(self.character)
                            else:
                                self.sprites_character.add(self.character)
                                self.sprites_back.remove(self.character)

                    # Clicking on things
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if self.sheep_heart.rect.collidepoint(pos) and self.sheep_heart.alive() and \
                                self.character.rect.colliderect(self.sheep_heart.rect):
                            self.get_item(self.sheep_heart)
                            self.sheep_heart.kill()

                        if self.knife.rect.collidepoint(pos) and self.knife.alive() and self.character.rect.colliderect \
                                (self.knife.rect):
                            self.get_item(self.knife)
                            self.knife.kill()

                        if self.sheep.rect.collidepoint(pos) and self.check_inventory(self.knife) and self.sheep.alive() and \
                                self.character.rect.colliderect(self.sheep.rect):
                            self.sheep.kill()
                            self.sprites_front.add(self.sheep_heart)

                # Keys that we want to continually evaluate
                keys = pygame.key.get_pressed()
                # When character stops moving, don't animate
                if not (keys[K_LEFT] or keys[K_RIGHT] or keys[K_UP] or keys[K_DOWN]):
                    self.character.animate = False

                if keys[K_LEFT] or keys[K_a]:
                    self.character.animate = True
                    self.character.walking_right = False
                    self.character.walking_left = True
                    if not self.background.at_edge_left and self.character.rect.centerx <= (W/2):
                        self.scroll("LEFT")
                    else:
                        self.character.move_left()

                if keys[K_RIGHT] or keys[K_d]:
                    self.character.animate = True
                    self.character.walking_left = False
                    self.character.walking_right = True
                    if not self.background.at_edge_right and self.character.rect.centerx >= (W/2):
                        self.scroll("RIGHT")
                    else:
                        self.character.move_right()

                if keys[K_UP]:
                    if self.character.could_climb:
                        self.character.animate = True
                        self.character.climbing = True
                        self.character.v = 0

                        # define scrolling behavior
                        if not self.background.at_edge_top and self.character.rect.centery <= (H/2):
                            self.scroll("UP")
                        else:
                            self.character.climb_up()

                if keys[K_DOWN]:
                    if self.character.climbing and self.character.could_climb:
                        self.character.animate = True
                        # Has the ground been reached
                        if not self.background.at_edge_bottom:
                            self.scroll("DOWN")
                        else:
                            self.character.climb_down(self.on_surface)

                if not self.background.at_edge_bottom and not self.character.climbing:
                    self.scroll("DOWN")
                    self.character.v = self.background.v
                    self.character.falling = False

                elif not self.character.falling:
                    self.background.v = 0
                    self.character.falling = True

                self.character.update(self.background.rect.bottom)
                self.display_game()
                self.CLOCK.tick(FPS)

            # Pause Loop
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p and not self.inventory.alive():
                        self.pause = False
                    if event.key == pygame.K_e:
                        self.dont_display_inventory()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)


GAME()
