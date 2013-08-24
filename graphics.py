import pygame
import time
from pygame.sprite import Sprite
import settings
from utils import send_event, calculate_dot_positions

pygame.font.init()

class ProgressBar(Sprite):
    def __init__(self, length=1, artist='', title=''):
        Sprite.__init__(self)
        self.track_start = time.time()
        self.track_end = time.time() + length
        self.track_length = length
        self.track_progress = 0
        self.image = pygame.Surface((settings.RESOLUTION[0], settings.NOW_PLAYING_HEIGHT))
        self.rect = self.image.get_rect()
        self.metadata = pygame.font.Font(
            settings.PROGRESS_FONT,
            settings.PROGRESS_FONT_SIZE
            ).render('%s - %s' % (artist, title), True, pygame.Color('white'))
        self.rect.bottom = settings.RESOLUTION[1]
        self.update()

    def update(self):
        # background
        pygame.draw.rect(self.image, (30, 0, 100),
                         pygame.Rect(0, 0, settings.RESOLUTION[0], settings.NOW_PLAYING_HEIGHT))

        # progress bar
        self.progress = (time.time() - self.track_start) / float(self.track_length)
        if self.progress < 1:
            pygame.draw.rect(self.image, (100, 0, 255),
                             pygame.Rect(0, 0, settings.RESOLUTION[0]*self.progress, settings.NOW_PLAYING_HEIGHT))
        else:
            self.kill()
            send_event(event='song_finished')

        # track info
        self.image.blit(self.metadata, (settings.PADDING,
                                        settings.NOW_PLAYING_HEIGHT - self.metadata.get_height() - settings.PADDING))

        # remaining time
        r = self.track_end - time.time()
        m, s = divmod(r, 60)
        remaining = pygame.font.Font(
            settings.PROGRESS_FONT,
            settings.PROGRESS_FONT_SIZE
            ).render('%d:%02d' % (m, s), True, pygame.Color('white'))
        self.image.blit(remaining, (settings.RESOLUTION[0]-remaining.get_width()*1.2,
                                    settings.NOW_PLAYING_HEIGHT - remaining.get_height() - settings.PADDING))

    def get_font(self):
        return pygame.font.Font(settings.PROGRESS_FONT, settings.PROGRESS_FONT_SIZE)


class Announcement(Sprite):
    def __init__(self, value='', color='white', textcolor='black'):
        Sprite.__init__(self)
        self.image = pygame.Surface((settings.RESOLUTION[0], settings.NOW_PLAYING_HEIGHT))
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect()
        self.text = pygame.font.Font(
            settings.PROGRESS_FONT,
            settings.PROGRESS_FONT_SIZE
            ).render('%s' % (value), True, pygame.Color(textcolor))
        self.image.blit(self.text, (settings.RESOLUTION[0]/2 - self.text.get_width()/2,
                                        settings.NOW_PLAYING_HEIGHT - self.text.get_height() - settings.PADDING))
        self.rect.bottom = settings.RESOLUTION[1]
        send_event(event='position', now_playing=True)

    def kill(self):
        Sprite.kill(self)


class Dots(Sprite):
    def __init__(self, value='', color='white', textcolor='black'):
        Sprite.__init__(self)
        self.image = pygame.Surface(settings.RESOLUTION)
        self.markers = calculate_dot_positions(outer=True)
        self.pos = calculate_dot_positions()
        self.rect = self.image.get_rect()
        self.blank()

    def blank(self):
        self.image.fill(pygame.Color('black'))
        for x in xrange(12):
            pygame.draw.circle(self.image, (200,0,0), self.markers[x], 6)

    def update(self):
        s = self.get_seconds()
        if s == 0:
            self.blank()
        #for x in xrange(self.get_seconds()+1):
        pygame.draw.circle(self.image, (255,0,0), self.pos[s], 6)

    def get_seconds(self):
        return time.localtime()[5]
