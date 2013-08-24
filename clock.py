#from twisted.internet.task import LoopingCall
from twisted.internet import reactor

import pygame
from pygame.locals import QUIT, KEYUP, K_ESCAPE

from settings import RESOLUTION, PORT
import texts
import graphics
from api import root, ProtectedSite


class StationClock():
    def __init__(self, screen, res):
        self.res = res
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.bg = pygame.Surface(res)
        self.bg.fill(pygame.Color('black'))

        self.date = texts.Date()
        self.readable_time = texts.ReadableTime()
        self.digital_clock = texts.DigitalClock()
        self.backtimer = texts.Backtimer()
        self.dots = graphics.Dots()

        self.show = texts.Show()
        self.studio = texts.Studio()

        self.progress_bar = graphics.ProgressBar()
        self.announcement = graphics.Announcement()

        self.sprites = pygame.sprite.OrderedUpdates([
            self.dots,
            self.date,
            self.readable_time,
            self.digital_clock,
            self.backtimer,
            self.show,
            self.studio,
            #self.progress_bar,
            #self.announcement
        ])

        self.change_info_position(False)

        reactor.callLater(0.1, self.tick)

    def event_handler(self, events):
        for event in events:
            if (event.type == QUIT) or ((event.type == KEYUP) and (event.key == K_ESCAPE)):
                reactor.stop()
            if (event.type == pygame.USEREVENT):
                self.user_event_handler(event)

    def user_event_handler(self, e):
        if e.event == 'position':
            self.change_info_position(e.now_playing)
        if e.event == 'song_finished':
            self.change_info_position(False)
        if e.event == 'song':
            self.announcement.kill()
            self.progress_bar.kill()
            self.progress_bar = graphics.ProgressBar(e.length, e.artist, e.title)
            self.sprites.add(self.progress_bar)
            self.change_info_position(True)
        if e.event == 'announcement':
            self.progress_bar.kill()
            self.announcement.kill()
            if hasattr(e, 'color') and hasattr(e, 'textcolor'):
                self.announcement = graphics.Announcement(e.value, e.color, e.textcolor)
            else:
                self.announcement = graphics.Announcement(e.value)
            self.sprites.add(self.announcement)
        if e.event == 'stop':
            self.progress_bar.kill()
            self.announcement.kill()
            self.change_info_position(False)
        if e.event == 'info':
            if hasattr(e, 'show'):
                self.show.update(value=e.show)
            if hasattr(e, 'onair'):
                self.studio.update(value=e.onair)

    def tick(self):
        try:
            # self.dots.update()
            # self.show.update()
            # self.studio.update()
            # self.digital_clock.update()
            # self.backtimer.update()
            if self.progress_bar.alive(): self.progress_bar.update()
            self.sprites.update()
            self.sprites.draw(self.screen)
            pygame.display.flip()
            self.sprites.clear(self.screen, self.bg)
            self.event_handler(pygame.event.get())
        except Exception as e:
            print 'EXCEPTION:', e
        reactor.callLater(0.05, self.tick)

    def change_info_position(self, progress_bar):
        self.show.update(now_playing=progress_bar)
        self.studio.update(now_playing=progress_bar)


def main():
    res = RESOLUTION
    screen = pygame.display.set_mode(res)
    pygame.init()
    StationClock(screen, res)
    # tick = LoopingCall(stationclock.tick())
    # tick.start(0.1)
    reactor.listenTCP(PORT, ProtectedSite(root))
    reactor.run()

if __name__ == '__main__':
    main()
