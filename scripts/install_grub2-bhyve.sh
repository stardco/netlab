#!/bin/sh
GBHYVE=$(pkg info grub2-bhyve | grep Name | wc -l)
if [ $GBHYVE -eq 0 ]; then
	pkg install grub2-bhyve
fi