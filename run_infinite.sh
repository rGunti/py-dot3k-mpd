#!/bin/bash
SCRIPT_PATH=`realpath $0`
SCRIPT_DIR=`dirname $SCRIPT_PATH`

DEBUG_FILE=/boot/no_mpd_display

cd $SCRIPT_DIR
echo $SCRIPT_DIR

if [ -f $DEBUG_FILE ]; then
  echo "DEBUG FILE $DEBUG_FILE detected, firmware will not start"
  exit
fi

export DOT3K=0

while true; do
	python ./run.py
	sleep 1
done
