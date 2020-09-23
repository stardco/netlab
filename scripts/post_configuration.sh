#!/bin/sh
#set -x
TAP_NAME=net.link.tap.up_on_open
TAP_VALUE_PARAM=1

LIST_MODULE_NAME="if_tap if_bridge vmm nmdm"
for MODULE in $LIST_MODULE_NAME; do 
	LOADED_MODULE=$(kldstat | grep $MODULE)
	if [ -z "$LOADED_MODULE" ]; then
		kldload $MODULE
	fi
	STARTUP_MODULE=$(cat /boot/loader.conf | grep ${MODULE}_load | grep YES)
	if [ -z "$STARTUP_MODULE" ]; then
		sysrc -f /boot/loader.conf ${MODULE}_load=YES
	fi
done

sysctl net.link.tap.up_on_open=1
SYSCTL_TAP=$(cat /etc/sysctl.conf | grep net.link.tap.up_on_open | cut -f2 -d "=")
if [ -z "$SYSCTL_TAP" ]; then
	echo net.link.tap.up_on_open=$TAP_VALUE_PARAM >> /etc/sysctl.conf
else
	if [ $SYSCTL_TAP -ne $TAP_VALUE_PARAM ]; then
		sed -i -r 's/net\.link\.tap\.up\_on\_open..*/net\.link\.tap\.up\_on\_open=1/' /etc/sysctl.conf
	fi 
fi
