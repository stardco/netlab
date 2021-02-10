#!/bin/sh
PYTHON=$(pkg info python37 | grep Name)
if [ $PYTHON -eq 0 ]; then
	pkg install python37
fi
