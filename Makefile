depends:
	sh scripts/install_ser2net.sh
	sh scripts/install_python.sh
	sh scripts/install_grub2-bhyve.sh

post-config:
	sh scripts/post_configuration.sh
	
install: depends
	install -d /usr/local/etc/netlab/repo
	install -d /usr/local/etc/netlab/templates
	install -d /var/run/netlab
	touch /var/run/netlab/ser2net_session
	install -m 0750 -o root -g wheel src/netlab /usr/local/sbin/
	install -m 0750 -o root -g wheel src/classes/netlab_area.py /usr/local/lib/python3.7/
	install -m 0750 -o root -g wheel src/classes/netlab_console.py /usr/local/lib/python3.7/
	install -m 0750 -o root -g wheel src/classes/netlab_host.py /usr/local/lib/python3.7/
	install -m 0750 -o root -g wheel src/classes/netlab_machine.py /usr/local/lib/python3.7/
	install -m 0750 -o root -g wheel src/classes/netlab_port.py /usr/local/lib/python3.7/
	install -m 0750 -o root -g wheel src/classes/netlab_switch.py /usr/local/lib/python3.7/
	install -m 0750 -o root -g wheel src/classes/netlab_template.py /usr/local/lib/python3.7/

	if [ -f /usr/local/etc/netlab/machines.conf ]; then\
		$(cp /usr/local/etc/netlab/machines.conf /usr/local/etc/netlab/machines.conf.old)\
	fi 
	install -m 0640 -o root -g wheel -b confs/machines.conf /usr/local/etc/netlab/
	
	if [ -f /usr/local/etc/netlab/areas.conf ]; then\
		$(cp /usr/local/etc/netlab/areas.conf /usr/local/etc/netlab/areas.conf.old)\
	fi
	install -m 0640 -o root -g wheel -b confs/areas.conf /usr/local/etc/netlab/
	
	if [ -f /usr/local/etc/netlab/templates.conf ]; then\
		$(cp /usr/local/etc/netlab/templates.conf /usr/local/etc/netlab/templates.conf.old)\
	fi
	install -m 0640 -o root -g wheel -b confs/templates.conf /usr/local/etc/netlab/
	
	if [ -f /usr/local/etc/netlab/intercos.conf ]; then\
		$(cp /usr/local/etc/netlab/intercos.conf /usr/local/etc/netlab/intercos.conf.old)\
	fi
	install -m 0640 -o root -g wheel -b confs/intercos.conf /usr/local/etc/netlab/

	if [ -f /usr/local/etc/netlab/switches.conf ]; then\
		$(cp /usr/local/etc/netlab/switches.conf /usr/local/etc/netlab/switches.conf.old)\
	fi
	install -m 0640 -o root -g wheel -b confs/switches.conf /usr/local/etc/netlab/
	
	make post-config

deinstall:
	rm /usr/local/sbin/netlab
	rm -r /var/run/netlab
	rm /usr/local/lib/python3.7/netlab_area.py
	rm /usr/local/lib/python3.7/netlab_console.py
	rm /usr/local/lib/python3.7/netlab_host.py
	rm /usr/local/lib/python3.7/netlab_machine.py
	rm /usr/local/lib/python3.7/netlab_port.py
	rm /usr/local/lib/python3.7/netlab_switch.py
	rm /usr/local/lib/python3.7/netlab_template.py
	echo "ser2net not deinstalled. do pkg remove ser2net to delete it"
	echo "Configuration file in /usr/local/etc/netlab not removed" 

reinstall: stop deinstall depends
	install -d /usr/local/etc/netlab/repo
	install -d /usr/local/etc/netlab/templates
	install -m 0750 -o root -g wheel src/classes/netlab_area.py /usr/local/lib/python3.7/
	install -m 0750 -o root -g wheel src/classes/netlab_console.py /usr/local/lib/python3.7/
	install -m 0750 -o root -g wheel src/classes/netlab_host.py /usr/local/lib/python3.7/
	install -m 0750 -o root -g wheel src/classes/netlab_machine.py /usr/local/lib/python3.7/
	install -m 0750 -o root -g wheel src/classes/netlab_port.py /usr/local/lib/python3.7/
	install -m 0750 -o root -g wheel src/classes/netlab_switch.py /usr/local/lib/python3.7/
	install -m 0750 -o root -g wheel src/classes/netlab_template.py /usr/local/lib/python3.7/
	install -d /var/run/netlab
	touch /var/run/netlab/ser2net_session
	install -m 0750 -o root -g wheel src/netlab /usr/local/sbin/

stop:
	netlab unload
