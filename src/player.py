import pygame

from src import constants
from src import spritesheet

"""
defining the player class; platforming engine etc
"""


class Player(pygame.sprite.Sprite):

    # will contain a level class that we use to check for collision
    level = None

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.xv = 0
        self.yv = 0

        self.start_x = x
        self.start_y = y

        self.gravity = constants.PLAYER_GRAVITY
        self.friction = constants.PLAYER_FRICTION
        self.speed = constants.PLAYER_SPEED
        self.jump_height = constants.PLAYER_JUMP_HEIGHT

        sprite_sheet = spritesheet.SpriteSheet("src/resources/sprites/player.png")

        self.image = sprite_sheet.get_image(0, 0, 32, 64)

        self.rect = self.image.get_rect()
        self.direction = "R"
        self.touching_ground = False

        self.rect.x = self.start_x
        self.rect.y = self.start_y

    def update(self):

        self.yv += self.gravity

        # temporary collision with bottom of screen: will remove once tiles are made
        if self.rect.y >= constants.DISPLAY_HEIGHT - self.rect.height and self.yv >= 0:
            self.yv = 0
            self.rect.y = constants.DISPLAY_HEIGHT - self.rect.height

        self.xv *= self.friction

        if abs(self.xv) <= 0.1:  # this will make animating look a little nicer later
            self.xv = 0

        self.rect.x += self.xv

        # collision detection time
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platforms, False)
        for block in block_hit_list:
            if self.xv > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
            self.xv = 0

        self.rect.y += self.yv
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platforms, False)
        for block in block_hit_list:
            if self.yv > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
            self.yv = 0

        self.touching_ground = self.on_ground()

    def on_ground(self):

        self.rect.y += 2
        hit_list = pygame.sprite.spritecollide(self, self.level.platforms, False)
        self.rect.y -= 2

        return True if len(hit_list) or self.rect.bottom >= constants.DISPLAY_HEIGHT else False

    def walk_right(self):

        self.xv += self.speed
        self.direction = "R"

    def walk_left(self):

        self.xv -= self.speed
        self.direction = "L"

    def jump(self):

        if self.on_ground():
            self.yv = -self.jump_height

    def reset(self):

        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.xv = 0
        self.yv = 0
