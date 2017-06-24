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

""" Test Script do check if my idea works

Created by rapha on the 23.06.2017 at 21:44
"""

from os import environ
from apps.utils import get_env
from time import sleep
from mpd import MPDClient
from dot3k.menu import Menu
from apps.mpd_player import MPDPlayer


USE_DOT3K = (get_env('DOT3K', '0') == "1")
USE_DOTHAT = not USE_DOT3K

if USE_DOT3K:
    import dot3k.backlight as backlight
    import dot3k.lcd as lcd
    import dot3k.joystick as nav
else:
    import dothat.backlight as backlight
    import dothat.lcd as lcd
    import dothat.touch as nav

__author__ = "Raphael \"rGunti\" Guntersweiler"
__copyright__ = "Copyright 2017 rGunti"
__credits__ = []

__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raphael \"rGunti\" Guntersweiler"
__email__ = "raphael@rgunti.ch"
__status__ = "Development"


"""
:param String s
"""

if __name__ == '__main__':  # code to execute if called from command-line
    menu = Menu(
        structure={
            'Player': MPDPlayer()
        },
        lcd=lcd
    )
    menu.select()

    if USE_DOTHAT:
        nav.enable_repeat(True)
        nav.bind_defaults(menu)
    else:
        @nav.on(nav.UP)
        def handle_up(pin):
            menu.up()


        @nav.on(nav.DOWN)
        def handle_down(pin):
            menu.down()


        @nav.on(nav.LEFT)
        def handle_left(pin):
            menu.left()


        @nav.on(nav.RIGHT)
        def handle_right(pin):
            menu.right()


        @nav.on(nav.BUTTON)
        def handle_button(pin):
            menu.select()

    backlight.set_graph(0)
    backlight.rgb(128, 128, 128)
    lcd.set_contrast(50)

    while True:
        # status = mpd_client.status()
        #
        # lcd.set_cursor_position(0, 0)
        # if status['state'] == 'play' or status['state'] == 'pause':
        #     current_song = mpd_client.currentsong()
        #
        #     lcd.write(get_trimmed_string(current_song['title']).center(16))
        #     lcd.write(' '.center(16))
        #     lcd.write(' '.center(16))
        # else:
        #     lcd.write(' '.center(16))
        #     lcd.write('Ready'.center(16))
        #     lcd.write(' '.center(16))
        menu.redraw()
        sleep(0.1)
