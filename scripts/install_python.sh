#!/bin/sh
PYTHON=$(ls /usr/local/bin/python3.7)
if [ -z $PYTHON ]; then
	pkg install python37
fi
