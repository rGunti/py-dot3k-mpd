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

""" TODO: Explain what wifi_app does

Maybe a longer description here?

Created by rapha on the 24.06.2017 at 11:52
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
    from dot3k.menu import MenuOption
    from apps.utils import get_env
    from ConfigParser import ConfigParser
    from StringIO import StringIO
    from os import SEEK_SET, listdir, stat
    from time import time, sleep
    from subprocess import check_output, Popen, PIPE
    from re import sub, split, MULTILINE, match, IGNORECASE
    import humanize as pp
    from threading import Thread, current_thread

    class WiFiDataFetcher(object):
        def __init__(self, interval=1):
            self.interval = interval
            self.connected_clients = 0

            self.parent_thread = current_thread()

            self.settings = {
                'HOSTAPD_CONTROL_PATH': '/var/run/hostapd',
                'HOSTAPD_CLI_PATH': '/usr/sbin/hostapd_cli',
                'IFCONFIG_PATH': '/sbin/ifconfig',
                'ARP_PATH': '/usr/sbin/arp',
                'ARP_FLAGS': '-an'
            }

            self._interfaces = []
            self._hostapd_stats = dict()
            self._clients = dict()
            self._arp_table = dict()

            thread = Thread(target=self.run, args=())
            thread.daemon = True
            thread.start()

        def get_client_count(self, iface):
            if iface in self._hostapd_stats:
                return self._hostapd_stats[iface][3]
            else:
                return 0

        def run(self):
            while True:
                self.parent_thread.join(self.interval)
                if not self.parent_thread.is_alive():
                    break
                self._interfaces = self._get_hostapd_interfaces()
                self._get_hostapd()
                self._get_arp_table()

        def _get_hostapd_interfaces(self):
            return listdir(self.settings['HOSTAPD_CONTROL_PATH'])

        def _get_hostapd(self):
            for interface in self._interfaces:
                hostapd_cli_cmd = [self.settings['HOSTAPD_CLI_PATH'], 'i', interface, 'all_sta']
                hostapd_uptime = time() - int(stat('%s/%s' % (self.settings['HOSTAPD_CONTROL_PATH'], interface))[9])

                all_sta_output = Popen(hostapd_cli_cmd, stdout=PIPE)\
                    .communicate()[0]
                hostapd_output = Popen([self.settings['HOSTAPD_CLI_PATH'], 'status'], stdout=PIPE)\
                    .communicate()[0]\
                    .split('\n')

                channel = sub('channel=', '', hostapd_output[16])
                bssid = sub('bssid\[0\]=', '', hostapd_output[24])
                ssid = sub('ssid\[0\]=', '', hostapd_output[25])
                clientcount = int(sub('num_sta\[0\]=', '', hostapd_output[26]))

                self._hostapd_stats[interface] = [ssid, bssid, channel, clientcount]

                macreg = r'^(' + r'[:-]'.join([r'[0-9a-fA-F]{2}'] * 6) + r')$'
                stas = split(macreg, all_sta_output, flags=MULTILINE)

                mac = rx = tx = ctime = ''
                for sta_output in stas:

                    for line in sta_output.split('\n'):
                        if match(macreg, line):
                            mac = line
                        if match('rx_packets', line):
                            rx = sub('rx_packets=', '', line)
                        if match('tx_packets', line):
                            tx = sub('tx_packets=', '', line)
                        if match('connected_time=', line):
                            ctime = sub('connected_time=', '', line)

                    if mac and rx and tx and ctime:
                        self._clients[mac] = [ctime, rx, tx]

        def _get_arp_table(self):
            arp_output = Popen([self.settings['ARP_PATH'], self.settings['ARP_FLAGS']], stdout=PIPE)\
                .communicate()[0]\
                .split('\n')

            for line in xrange(len(arp_output)):
                l = arp_output[line].split(' ')
                try:
                    iface = l[6]
                    if iface in self._interfaces:
                        ip = l[1]
                        mac = l[3]

                        if match('[A-Z0-9][A-Z0-9]:', mac, IGNORECASE):
                            self._arp_table[mac] = [ip, iface]
                except:
                    pass


    class WiFiApp(MenuOption):
        def __init__(self):
            MenuOption.__init__(self)
            self._is_setup = False
            self._wifi_config = None
            self._icons = {
                'ICON_WIFI': {
                    'index': 0,
                    'bmp': [0b00000, 0b00000, 0b00000, 0b11100, 0b00010, 0b11001, 0b00101, 0b10101]
                },
                'ICON_KEY': {
                    'index': 1,
                    'bmp': [0b00110, 0b01001, 0b01001, 0b00110, 0b00010, 0b00110, 0b00010, 0b00110]
                },
                'ICON_DEVICES': {
                    'index': 2,
                    'bmp': [0b00000, 0b00000, 0b01111, 0b01000, 0b11011, 0b01000, 0b01111, 0b00000]
                }
            }
            self._animations = {}
            self._wifi_data_thread = WiFiDataFetcher()

        def _setup_icons(self, lcd):
            for key, value in self._icons.iteritems():
                lcd.create_char(value['index'], value['bmp'])

            for key, value in self._animations.iteritems():
                lcd.create_animation(value['index'], value['frames'], value['fps'])

            self._is_setup = True

        def cleanup(self):
            self._is_setup = False
            self._wifi_config = None

        def _read_wifi_config(self):
            cfg = StringIO()
            cfg.write('[hostapd]\n')
            cfg.write(open('/etc/hostapd/hostapd.conf').read())
            cfg.seek(0, SEEK_SET)

            self._wifi_config = ConfigParser()
            self._wifi_config.readfp(cfg)

        def _check_connected_devices(self):
            return self._wifi_data_thread.get_client_count('wlan0')

        def redraw(self, menu):
            if not self._is_setup:
                self._setup_icons(menu.lcd)
            if self._wifi_config is None:
                self._read_wifi_config()

            wifi_ssid = self._wifi_config.get('hostapd', 'ssid')
            wifi_psk = self._wifi_config.get('hostapd', 'wpa_passphrase')

            menu.write_option(
                row=0,
                text=wifi_ssid,
                icon=chr(0) + ' ',
                scroll=(len(wifi_ssid) > 14)
            )
            menu.write_option(
                row=1,
                text=wifi_psk,
                icon=chr(1) + ' ',
                scroll=(len(wifi_psk) > 14)
            )
            menu.write_option(
                row=2,
                text='Devices: ' + str(self._check_connected_devices()),
                icon=chr(2) + ' ',
                scroll=False
            )
