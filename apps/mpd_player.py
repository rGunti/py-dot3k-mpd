#!/usr/bin/env python
""" Copyright 2017 Raphael "rGunti" Guntersweiler

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

""" TODO: Explain what mpd_player does

Maybe a longer description here?

Created by rapha on the 23.06.2017 at 22:40
"""

__author__ = "Raphael \"rGunti\" Guntersweiler"
__copyright__ = "Copyright 2017 rGunti"
__credits__ = []

__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raphael \"rGunti\" Guntersweiler"
__email__ = "raphael@rgunti.ch"
__status__ = "Development"

if __name__ == '__main__':  # code to execute if called from command-line
    print("""
    !!! DO NOT RUN THIS SCRIPT !!!
    
    This script is intended to be included by another script and is not executable
    on its own. Please do not try to run this.
    
    The script will now terminate.
    """)
    exit(1)
else:
    from dot3k.menu import Menu, MenuIcon, MenuOption
    # from dothat.backlight import set_graph, set
    from apps.utils import get_env
    from mpd import MPDClient, ProtocolError, ConnectionError
    from datetime import datetime
    from time import time


    class MPDPlayer(MenuOption):
        def __init__(self):
            MenuOption.__init__(self)
            self._setup = False
            self._icons = {
                'ICON_PLAY': {
                    'index': 1,
                    'bmp': [0b10000, 0b11000, 0b11100, 0b11110, 0b11100, 0b11000, 0b10000, 0b00000]
                },
                'ICON_PAUSE': {
                    'index': 2,
                    'bmp': [0b00000, 0b11011, 0b11011, 0b11011, 0b11011, 0b11011, 0b11011, 0b00000]
                },
                'ICON_STOP': {
                    'index': 3,
                    'bmp': [0b00000, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b00000]
                }
            }
            self._animations = {
                'ANIM_PAUSE': {
                    'index': 7,
                    'frames': [self._icons['ICON_PAUSE']['bmp'], [0, 0, 0, 0, 0, 0, 0, 0]],
                    'fps': 2
                }
            }

            self.mpd = None
            self.mpd_status = None

            self.volume = 100
            self.volume_pressed = time() - 5

            self._reconnect()

        def _reconnect(self):
            if self.mpd is not None:
                self.mpd.disconnect()

            self.mpd = MPDClient()
            self.mpd.timeout = 5
            self.mpd.idletimeout = None

            self.mpd.connect(get_env('MPD_HOST', '127.0.0.1'), int(get_env('MPD_PORT', 6600)))

            self.mpd_status = None

        def _setup_icons(self, lcd):
            for key, value in self._icons.iteritems():
                lcd.create_char(value['index'], value['bmp'])

            for key, value in self._animations.iteritems():
                lcd.create_animation(value['index'], value['frames'], value['fps'])

        @staticmethod
        def print_row(menu, row, text):
            menu.write_option(
                row=row,
                text=text,
                scroll_padding='  ',
                scroll=(len(text) > 16)
            )

        @staticmethod
        def format_time(sec, no_hours=False):
            m, s = divmod(sec, 60)
            h, m = divmod(m, 60)
            if h >= 1:
                if no_hours:
                    return "%02d:%02d" % ((h * 60) + m, s)
                else:
                    return "%d:%02d:%02d" % (h, m, s)
            else:
                return "%02d:%02d" % (m, s)

        @staticmethod
        def format_mpd_status_time(v, both=False):
            arr_v = v.split(':')

            time_current = MPDPlayer.format_time(int(arr_v[0]), True)
            if both:
                time_total = MPDPlayer.format_time(int(arr_v[1]), True)
                return time_current + '/' + time_total
            else:
                return time_current

        @staticmethod
        def get_safe(d, k, default=''):
            if k in d:
                return d[k]
            else:
                return default

        def left(self):
            # Sometimes a protocol error is raised when executing next
            # (don't know why) and the app freaks out.
            # We just try to throw away our current MPD session and
            # create a new one
            try:
                self.volume_pressed -= 5
                self.mpd.previous()
            except ConnectionError:
                pass
            except:
                self._reconnect()

            return True

        def right(self):
            # Sometimes a protocol error is raised when executing next
            # (don't know why) and the app freaks out.
            # We just try to throw away our current MPD session and
            # create a new one
            try:
                self.volume_pressed -= 5
                self.mpd.next()
            except ConnectionError:
                pass
            except:
                self._reconnect()

            return True

        def up(self):
            try:
                self.volume_pressed = time()
                self.mpd.setvol(min(self.volume + 5, 100))
            except ConnectionError:
                pass
            except:
                self._reconnect()
            return True

        def down(self):
            try:
                self.volume_pressed = time()
                self.mpd.setvol(max(self.volume - 5, 0))
            except ConnectionError:
                pass
            except:
                self._reconnect()
            return True

        def select(self):
            # Sometimes a protocol error is raised when executing next
            # (don't know why) and the app freaks out.
            # We just try to throw away our current MPD session and
            # create a new one
            try:
                if self.mpd_status is not None:
                    state = self.mpd_status['state']
                    if state == 'play' or state == 'pause':
                        self.mpd.pause(1 if state == 'play' else 0)
                    else:
                        self.mpd.play()
            except ConnectionError:
                pass
            except:
                self._reconnect()

            return False

        def cancel(self):
            return False

        def redraw(self, menu):
            if not self._setup:
                self._setup_icons(menu.lcd)

            try:
                self.mpd_status = self.mpd.status()
            except ConnectionError:
                return
            status = self.mpd_status

            self.volume = int(MPDPlayer.get_safe(status, 'volume', '100'))

            player_icon = 0
            title_line = ''
            artist_line = ''
            player_time = '--:--'

            if len(status) == 0 or 'state' not in status:
                pass
            elif status['state'] == 'play' or status['state'] == 'pause':
                current_song = self.mpd.currentsong()
                title_line = MPDPlayer.get_safe(current_song, 'title', '-')
                artist_line = MPDPlayer.get_safe(current_song, 'artist', '-')

                player_time = MPDPlayer.format_mpd_status_time(MPDPlayer.get_safe(status, 'time', '0'), True)

                if status['state'] == 'play':
                    player_icon = 1
                else:
                    player_icon = 2
            elif status['state'] == 'stop':
                player_icon = 3

            dif = time() - self.volume_pressed
            if dif < 3:
                title_line = ('VOLUME ' + str(self.volume).rjust(3) + ' %').center(16)
                artist_line = ''
                for i in range(0, (self.volume / 10)):
                    artist_line += '-'
                artist_line = ('[ ' + artist_line.ljust(10) + ' ]').center(16)
                # set_graph(float(self.volume) / 100)
            else:
                # set_graph(0)
                pass

            MPDPlayer.print_row(menu, 0, title_line)
            MPDPlayer.print_row(menu, 1, artist_line)
            MPDPlayer.print_row(menu, 2, chr(player_icon) + player_time.rjust(15))

            menu.lcd.update_animations()
