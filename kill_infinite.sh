#!/usr/bin/env bash

echo "This script will shut down all processes of the run_infinite.sh script"
echo "to enable Development and Debugging."
echo ""
echo "The Python Firmware will be started, after the next reboot."
echo "You can keep the Firmware disabled by placing an empty file with the "
echo "following name in the boot drive:"
echo ""
echo "   /boot/no_mpd_display"
echo ""
echo "As long as this file is placed there the Firmware will not start and the"
echo "run_infinite.sh script will not work. To re-enable the Firmware on boot"
echo "remove this file from the boot drive."
echo ""

PID_WATCHDOG=$(ps aux | grep '[/]bin/bash /home/pi/py-dot3k-mpd/run_infinite.sh' | awk '{print $2}')
PID_PYTHON=$(ps aux | grep '[p]ython ./run.py' | awk '{print $2}')

echo "The following processes will be killed:"
echo " - Firmware Watchdog => $PID_WATCHDOG"
echo " - Python Firmware   => $PID_PYTHON"
echo ""

read -r -p "Do you want to continue? [y/n] " response
case "$response" in
    [yY][eE][sS]|[yY])
        echo ""

        echo "Killing Watchdog (PID: $PID_WATCHDOG)"...
        sudo kill $PID_WATCHDOG

        echo "Killing Python Process (PID: $PID_PYTHON)"...
        sudo kill $PID_PYTHON
        ;;
    *)
        echo ""
        ;;
esac

echo " ==== Script finished ==== "
