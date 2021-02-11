#!/bin/sh
PYTHON=$(pkg info python37 | grep Name | wc -l)
if [ $PYTHON -eq 0 ]; then
	pkg install python37
fi
