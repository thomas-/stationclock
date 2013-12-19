import pygame
import time
from math import pi, radians, cos, sin

import settings
from constants import *

def send_event(**kwargs):
    pygame.event.post(
        pygame.event.Event(
            pygame.USEREVENT,
            **kwargs
        )
    )

def make_readable_time():
    h, m = time.localtime()[3:5]
    p = " %s " % PAST
    if m > 30:
        m = 60 - m
        h = h + 1
        p = " %s " % TO
    time_string = ""
    if m == 0:
        if h%24 == 0: time_string = HOURS[h]
        else: time_string = HOURS[h] + " %s" % OCLOCK
    else:
        time_string = MINUTES[m] + p + HOURS[h]
    return time_string

def make_backtimer_time():
    m, s = time.localtime()[4:6]
    m = settings.BACKTIMER_COUNT - 1 - (m % settings.BACKTIMER_COUNT)
    s = 60 - s
    backtimer_string = '-%02d:%02d' % (m, s)
    return backtimer_string

def calculate_dot_positions(outer=False):
    x, y = settings.RESOLUTION[0]/2, settings.RESOLUTION[1]/2
    if outer:
        r = settings.RESOLUTION[1]/2.5
    else:
        r = settings.RESOLUTION[1]/2.75
    dots = []
    if outer: gap = 5
    else: gap = 1
    for i in xrange(0,60,gap):
        deg = 6*i - 90
        rad = radians(deg)
        dots.append((int(x + r * cos(rad)),
                int(y + r * sin(rad))))
    return dots
