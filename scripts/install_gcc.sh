#!/bin/sh
GCC=$(pkg info gcc | grep Name |wc -l)
if [ $GCC -eq 0 ]; then
	pkg install gcc
fi
