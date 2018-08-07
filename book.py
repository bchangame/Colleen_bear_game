import pygame


class Story(object):
    def __init__(self, surface):
        self.surface = surface
        self.images = dict()
        self.chap_num = 1
        self.page_num = 1

    def display(self, images):
        for image in images:
            self.images = (pygame.image.load(image))

    def chapter_one(self):
        self.images = ("Chapter1a.png": (0, 0))

        # :^'
        # 0, 