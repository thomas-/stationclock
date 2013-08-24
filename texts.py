import pygame
import time
from pygame.sprite import Sprite
import settings
from utils import make_readable_time, make_backtimer_time

pygame.font.init()

class TextSprite(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.font = self.get_font()
        self.update()

    def render(self, string, color):
        return self.font.render(string, True, color)

    def update(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        string, color = self.get_details()
        self.image = self.render(string, color)
        self.rect = self.image.get_rect()
        self.set_position(self.rect)

    def get_font(self):
        return pygame.font.Font(settings.DATE_FONT, 32)

    def get_details(self, *args, **kwargs):
        return str('string'), (255, 255, 255)

    def set_position(self, rect):
        pass


class Date(TextSprite):
    def get_font(self):
        return pygame.font.Font(settings.DATE_FONT, settings.DATE_FONT_SIZE)

    def get_details(self):
        return time.strftime("%A %d %B"), (255, 255, 255)

    def set_position(self, rect):
        rect.top = 0 + settings.PADDING
        rect.right = settings.RESOLUTION[0] - settings.PADDING


class ReadableTime(TextSprite):
    def get_font(self):
        return pygame.font.Font(settings.DATE_FONT, settings.DATE_FONT_SIZE)

    def get_details(self):
        return make_readable_time(), (255, 255, 255)

    def set_position(self, rect):
        rect.top = 0 + settings.PADDING
        rect.left = 0 + settings.PADDING


class DigitalClock(TextSprite):
    def get_font(self):
        return pygame.font.Font(settings.CLOCK_FONT, settings.CLOCK_FONT_SIZE)

    def get_details(self):
        return time.strftime("%H:%M"), (255, 0, 0)

    def set_position(self, rect):
        rect.midbottom = (settings.RESOLUTION[0]/2, settings.RESOLUTION[1]/2 + 10)


class Backtimer(TextSprite):
    def get_font(self):
        return pygame.font.Font(settings.BACKTIMER_FONT, settings.BACKTIMER_FONT_SIZE)

    def get_details(self):
        return make_backtimer_time(), (0, 255, 0)

    def set_position(self, rect):
        rect.midtop = (settings.RESOLUTION[0]/2, settings.RESOLUTION[1]/2 + 10)


class Show(TextSprite):
    value = 'No Show'
    now_playing = False
    def get_font(self):
        return pygame.font.Font(settings.INFO_FONT, settings.INFO_FONT_SIZE)

    def get_details(self):
        return self.value, (41, 255, 211)

    def set_position(self, rect):
        if self.now_playing: extra = 50
        else: extra = 0
        rect.left = 0 + settings.PADDING
        rect.bottom = settings.RESOLUTION[1] - settings.PADDING - extra


class Studio(TextSprite):
    value = 0
    now_playing = False
    def get_font(self):
        return pygame.font.Font(settings.INFO_FONT, settings.INFO_FONT_SIZE)

    def get_details(self):
        return 'Live from Studio %s' % self.value, (150, 255, 211)

    def set_position(self, rect):
        if self.now_playing: extra = 50
        else: extra = 0
        rect.right = settings.RESOLUTION[0] - settings.PADDING
        rect.bottom = settings.RESOLUTION[1] - settings.PADDING - extra
