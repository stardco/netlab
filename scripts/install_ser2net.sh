#!/bin/sh
SER2NET=$(pkg info ser2net | grep Name |wc -l)
if [ $SER2NET -eq 0 ]; then
	pkg install ser2net
fi
