stationclock
====

A clock/information screen primarily for use in a radio station.

Dependencies
====

[twisted](http://twistedmatrix.com/trac/)
[pygame](http://www.pygame.org)

Features
====

You get a clock, a backtimer, some dots showing seconds, a readable time format (handy for presenters quickly reading the time), the date, the currently onair show and the currently onair studio.

There is also a now playing/announcement bar at the bottom which remains hidden unless a song or announcement is active.

Information is updated via an API over HTTP so can be controlled by just about anything.

Usage
====

To run the clock:
    python clock.py

Screen can be updated using POST requests to the provided API

Update onair information to be The Morning Show from Studio 2:
    curl -d "show=The Morning Show&onair=2" http://localhost:7000/info

Trigger a progress bar for a now playing song (length in _seconds_):
    curl -d "artist=Icona Pop&title=I Love It&length=50" http://localhost:7000/play

Trigger an announcement:
    curl -d "value=BULLETINS" http://localhost:7000/announcement

Trigger an announcement with fancy colors:
    curl -d "value=BULLETINS&color=yellow&textcolor=black" http://localhost:7000/announcement

Kill the current progress bar/announcement
    curl http://localhost:7000/stop


Configuration
===

By default stationclock listens on port 7000 and only allows access from localhost.

Add allowed IP addresses to `ALLOWED_IPS` in `settings.py`, eg, the IP of your playout computer or whatever else will be triggering events.

The display is not very configurable at this stage, but some settings are available in `settings.py`

Thanks
===

Special thanks to @tepreece and @ofluff for making this possible.



