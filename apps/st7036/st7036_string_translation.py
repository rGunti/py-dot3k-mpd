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

""" TODO: Explain what st7036_string_translation does

Maybe a longer description here?

Created by rapha on the 25.06.2017 at 12:16
"""

__author__ = "Raphael \"rGunti\" Guntersweiler"
__copyright__ = "Copyright 2017 rGunti"
__credits__ = []

__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Raphael \"rGunti\" Guntersweiler"
__email__ = "raphael@rgunti.ch"
__status__ = "Development"


ST7036_CHAR_MAP = {
    183: 13,
    174: 14,
    169: 15,
    8482: 16,
    8224: 17,
    167: 18,
    182: 19,
    915: 20,
    916: 21,
    920: 22,
    923: 23,
    926: 24,
    960: 25,
    931: 26,
    934: 28,
    936: 29,
    937: 30,
    945: 31,
    165: 92,
    8594: 126,
    8592: 127,
    231: 128,
    252: 129,
    233: 130,
    226: 131,
    228: 132,
    224: 133,
    229: 134,
    234: 136,
    235: 137,
    232: 138,
    239: 139,
    238: 140,
    236: 141,
    196: 142,
    197: 143,
    198: 146,
    230: 145,
    201: 144,
    244: 147,
    246: 148,
    242: 149,
    251: 150,
    249: 151,
    255: 152,
    214: 153,
    220: 154,
    241: 155,
    209: 156,
    170: 157,
    186: 158,
    191: 159,
    176: 223,
    225: 224,
    237: 225,
    243: 226,
    250: 227,
    162: 228,
    163: 229,
    402: 232,
    195: 234,
    227: 235,
    213: 236,
    245: 237,
    216: 238,
    248: 239,
    168: 241,
    730: 242,
    180: 244,
    189: 245,
    188: 246,
    215: 247,
    247: 248,
    8804: 249,
    8805: 250,
    171: 251,
    187: 252,
    8800: 253,
    8730: 254,
    175: 255,
}
ST7036_EXCEPTIONAL_CHAR_MAP = {
    223: 'ss'  # "Scharfes S" not supported by Display, replacing it with double s is fairly common
}


def st7036_replace(s, debug=False):
    global ST7036_CHAR_MAP
    s = unicode(s, 'utf-8')
    l = list(s)
    for i in range(0, len(l)):
        char = ord(l[i])
        if debug:
            print(" - " + str(i) + ": CHAR '" + l[i] + "' " + str(char))
        if char in ST7036_CHAR_MAP:
            repl_char = ST7036_CHAR_MAP[char]
            l[i] = unichr(repl_char)
            if debug:
                print(" - " + str(i) + ": => '" + l[i] + "'" + str(repl_char))
        elif char in ST7036_EXCEPTIONAL_CHAR_MAP:
            l[i] = ST7036_EXCEPTIONAL_CHAR_MAP[char]
            if debug:
                print(" - " + str(i) + ": => Exc. '" + l[i] + "'")

    return ''.join(l)


if __name__ == '__main__':  # code to execute if called from command-line
    exit(0)
