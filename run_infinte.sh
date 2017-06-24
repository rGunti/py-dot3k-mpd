#!/bin/bash
SCRIPT_PATH=`realpath $0`
SCRIPT_DIR=`dirname $SCRIPT_PATH`

cd $SCRIPT_DIR
echo $SCRIPT_DIR

export DOT3K=1

while true; do
	python ./run.py
	sleep 1
done
