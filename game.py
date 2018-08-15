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

        self.mouse = Item(0, 0, "images/pixel.png", "mouse")
        self.mouse_group = pygame.sprite.Group(self.mouse)

        self.background = Background(0, GROUND)
        self.character = Character(500, GROUND)
        self.inventory = Inventory(0, 0, "images/inventory.png")

        self.cave = Item(2060, GROUND, "images/cave.png", "cave")
        self.cave_entry = Item(2060, GROUND, "images/cave_entry.png", "cave entry")
        self.cave_front = Item(2060, GROUND, "images/frontcave.png", "cave front")

        self.knife = pygame.sprite.Group()
        self.tree = pygame.sprite.Group()
        self.sheep = pygame.sprite.Group()
        self.sheep_heart = pygame.sprite.Group()
        self.read_csv('level_one.csv')

        self.sprites_back = pygame.sprite.Group(self.sheep, self.cave_entry)
        self.sprites_mid = pygame.sprite.Group(self.tree, self.cave)
        self.sprites_character = pygame.sprite.Group(self.character)
        self.sprites_front = pygame.sprite.Group(self.cave_front, self.knife)

        self.sprites_scroll = pygame.sprite.Group(self.background, self.tree, self.knife,
                                                  self.sheep, self.sheep_heart, self.cave, self.cave_front, self.cave_entry)
        self.sprites_gettable = pygame.sprite.Group(self.sheep_heart, self.knife)

        self.inventory_sprite = pygame.sprite.OrderedUpdates()

        self.title_screen_scroll = 0
        self.title = Item(W/2 - 390, H/2 + 150, "images/title.png", "title")
        self.play_button = Button(W/2 - 170, H/2 + 50, "images/play_button.png", "images/play_button_hover.png")
        self.load_button = Button(W/2 - 170, H/2 - 50, "images/load_button.png", "images/load_button_hover.png")
        self.title_background1 = InfiniteBackground(0, GROUND, "images/background.png")
        self.title_background2 = InfiniteBackground(self.title_background1.rect.width, GROUND, "images/background.png")
        self.title_screen_sprites = pygame.sprite.LayeredUpdates(self.title_background1, self.title_background2,
                                                                 self.title, self.play_button, self.load_button)

        self.pause = False
        self.on_surface = True

        self.title_screen()

    def read_csv(self, file):
        with open(file) as f:
            for line in f:
                split = line.strip().split(',')
                print(split)
                if split[2] == 'GROUND':
                    self.add_item(split[0], int(split[1]), GROUND)
                else:
                    self.add_item(split[0], int(split[1]), int(split[1]))

    def add_item(self, name, x, y):
        if name == "sheep":
            self.sheep.add(Sheep(x, y))
        elif name == "knife":
            self.knife.add(Knife(x, y))
        elif name == "sheep_heart":
            self.sheep_heart.add(SheepHeart(x, y))
        elif name == "tree":
            self.tree.add(Tree(x, y))

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

        # FIX ME
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
            print("%s: %d" % (item, self.inventory.dictionary[item][1]))
            print(self.inventory.i)
            if self.inventory.i <= 3:
                self.inventory.dictionary[item][0].inventory_sprite.rect.y = 200
            else:
                print("more items")
                item.inventory_sprite.rect.y = 350

            self.inventory.dictionary[item][0].inventory_sprite.rect.x = 900 + (150 * (self.inventory.i % 4))
            self.inventory_sprite.add(self.inventory.dictionary[item][0].inventory_sprite)
            self.inventory.matrix.append((item, 100, 900 + (200 * self.inventory.i)))
            self.inventory.i += 1
        self.pause = True

    def hide_inventory(self):
        self.inventory_sprite.remove(self.inventory)
        for item in self.inventory.dictionary.keys():
            self.inventory_sprite.remove(self.inventory.dictionary[item][0].inventory_sprite)
        self.pause = False
        self.inventory.i = 0

    def get_item(self, item):
        if item.name in self.inventory.dictionary.keys():
            self.inventory.dictionary[item.name][1] += 1
        else:
            self.inventory.dictionary[item.name] = [item, 1]

    def check_inventory(self, name):
        if name in self.inventory.dictionary.keys():
            return True
        else:
            return False

    def set_state(self):
        # Is the character on a surface (i.e. ground)
        if self.character.rect.bottom == self.background.rect.bottom:
            self.on_surface = True
            self.character.falling = False
            self.character.jumping = False
            self.character.climbing = False

        else:
            self.on_surface = False
            self.character.falling = True

        # Is the character colliding with a climbable object
        for sprite in pygame.sprite.spritecollide(self.character, self.tree, False):
            print(self.character.mask.count())
            print(self.character.mask.overlap_area(sprite.mask, (sprite.x - self.character.x, sprite.y - self.character.y)))
            if self.character.mask.overlap_area(sprite.mask, (sprite.x - self.character.x, sprite.y - self.character.y))\
                    > 0.5 * self.character.mask.count():
                print("can climb")
                self.character.could_climb = True
            else:
                self.character.could_climb = False
                self.character.climbing = False
                self.sprites_front.add(self.cave_front)

    def title_screen(self):
        while True:
            self.surface.fill(WHITE)

            pos = pygame.mouse.get_pos()
            self.mouse.set_pos(pos[0], pos[1])

            if pygame.sprite.spritecollide(self.play_button, self.mouse_group, False):
                self.play_button.image = self.play_button.hover_image
            else:
                self.play_button.image = self.play_button.norm_image

            if pygame.sprite.spritecollide(self.load_button, self.mouse_group, False):
                self.load_button.image = self.load_button.hover_image
            else:
                self.load_button.image = self.load_button.norm_image

            for event in pygame.event.get():
                # click on X in corner
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.rect.collidepoint(pos):
                        self.loop()

            self.title_background1.scroll_right()
            self.title_background2.scroll_right()

            self.title_screen_sprites.draw(self.surface)

            for x in range(-GROUND, W+GROUND, GROUND):
                self.surface.blit(pygame.image.load("images/tile.png"), ((self.title_background1.x % 200) + x,
                                                                         self.background.rect.bottom - 50))

            pygame.display.update()

    def cave_loop(self):
        while True:
            while not self.pause:
                self.surface.fill(BLACK)
                self.set_state()

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit(0)

                self.sprites_character.draw(self.surface)

                # FIX ME
                for x in range(-GROUND, W+GROUND, GROUND):
                    self.surface.blit(pygame.image.load("images/tile.png"), ((self.background.x % 200) + x,
                                                                             self.background.rect.bottom - 50))

                self.inventory_sprite.draw(self.surface)
                pygame.display.update()
                self.CLOCK.tick(FPS)

            # Pause Loop
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p and not self.inventory.alive():
                        self.pause = False
                    if event.key == pygame.K_e:
                        self.hide_inventory()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)

    def loop(self):
        # Outer game loop, includes paused game and inventory
        while True:
            # Inner game loop, while not paused
            while not self.pause:
                self.surface.fill(WHITE)

                self.set_state()

                if self.character.rect.right == W:
                    self.cave_loop()

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
                        self.mouse.set_pos(pos[0], pos[1])
                        # get sheep_heart
                        if pygame.sprite.groupcollide(self.mouse_group, self.sheep_heart, False, False):
                            for sprite in pygame.sprite.spritecollide(self.character, self.sheep_heart, True):
                                self.get_item(sprite)
                                sprite.kill()
                                break

                        # collect knife
                        if pygame.sprite.groupcollide(self.mouse_group, self.knife, False, False):
                            for sprite in pygame.sprite.spritecollide(self.character, self.knife, True):
                                self.get_item(sprite)
                                sprite.kill()
                                break

                        # kill sheep, need knife
                        if pygame.sprite.groupcollide(self.mouse_group, self.sheep, False, False) and \
                                self.check_inventory('knife'):
                            for sprite in pygame.sprite.spritecollide(self.character, self.sheep, False):
                                sprite.kill()
                                self.sheep_heart.add(SheepHeart(sprite.x, GROUND))
                                self.sprites_front.add(self.sheep_heart)
                                self.sprites_scroll.add(self.sheep_heart)
                                break

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
                            print("climbing")

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
                for sprite in self.sheep:
                    sprite.update()
                self.display_game()
                self.CLOCK.tick(FPS)

            # Pause Loop
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p and not self.inventory.alive():
                        self.pause = False
                    if event.key == pygame.K_e:
                        self.hide_inventory()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)


GAME()
