
int2tap: 
	gcc src/int2tap.c -o src/int2tap

depends:
	sh scripts/install_ser2net.sh
	
install: int2tap depends
	install -d /usr/local/etc/netlab/repo
	install -d /usr/local/etc/netlab/templates
	install -d /var/run/netlab
	touch /var/run/netlab/ser2net_session
	install -m 0755 -o root -g wheel src/int2tap /usr/local/sbin/
	install -m 0750 -o root -g wheel files/netlab-area /usr/local/sbin/
	install -m 0750 -o root -g wheel files/netlab-machine /usr/local/sbin/
	install -m 0750 -o root -g wheel files/netlab-interco /usr/local/sbin/
	if [ -f /usr/local/etc/netlab/machines.conf ]; then
		cp /usr/local/etc/netlab/machines.conf /usr/local/etc/netlab/machines.conf.old
	fi
	install -m 0640 -o root -g wheel -b confs/machines.conf /usr/local/etc/netlab/
	if [ -f /usr/local/etc/netlab/areas.conf ]; then
		cp /usr/local/etc/netlab/areas.conf /usr/local/etc/netlab/areas.conf.old
	fi
	install -m 0640 -o root -g wheel -b confs/areas.conf /usr/local/etc/netlab/
	if [ -f /usr/local/etc/netlab/templates.conf ]; then
		cp /usr/local/etc/netlab/templates.conf /usr/local/etc/netlab/templates.conf.old
	fi
	install -m 0640 -o root -g wheel -b confs/templates.conf /usr/local/etc/netlab/
	if [ -f /usr/local/etc/netlab/interco.conf ]; then
		cp /usr/local/etc/netlab/interco.conf /usr/local/etc/netlab/interco.conf.old
	fi
	install -m 0640 -o root -g wheel -b confs/interco.conf /usr/local/etc/netlab/

deinstall:
	rm /usr/local/sbin/int2tap
	rm /usr/local/sbin/netlab-area
	rm /usr/local/sbin/netlab-machine
	rm /usr/local/sbin/netlab-interco
	rm -r /var/run/netlab
	echo "ser2net not deinstalled. do pkg remove ser2net to delete it"
	echo "Configuration file in /usr/local/etc/netlab not removed" 

reinstall: stop deinstall int2tap depends
	install -d /usr/local/etc/netlab/repo
	install -d /usr/local/etc/netlab/templates
	install -d /var/run/netlab
	touch /var/run/netlab/ser2net_session
	install -m 0755 -o root -g wheel src/int2tap /usr/local/sbin/
	install -m 0750 -o root -g wheel files/netlab-area /usr/local/sbin/
	install -m 0750 -o root -g wheel files/netlab-machine /usr/local/sbin/
	install -m 0750 -o root -g wheel files/netlab-interco /usr/local/sbin/

stop:
	netlab-area unload
