**1. Introduction**

Netlab is a system to generate quiclky virtual network environment based on FreeBSD or Debian image.

**2. Installation**

To install tape the following commands :
`make install`
Warning ! a script launch the installation of the application ser2net.
Warning ! You need to activate the following configuration lines :
- in /etc/sysctl.conf

`net.link.tap.up_on_open=1`
- in /boot/loader.conf

`if_tap_load="YES"`

`if_bridge_load="YES"`

`vmm_load="YES"`

`nmdm_load="YES"`


And to activate them :

`sysctl net.link.tap.up_on_open=1`

`kldload if_tap`

`kldload if_bridge`

`kldload vmm`

`kldload ndmd`

**3. How to use**

WARNING : all commands have to be done by root !

*  Add a template

Copy an .img file in /usr/local/etc/netlab/templates (for exemple BSDRP-1.96-full-amd64-serial.img)

Create a type associate in the file /usr/local/etc/netlab/templates.conf

`BSDRP_196:BSD:BSDRP-1.96-full-amd64-serial.img:`

If it is a debian, you should add the "Linux" the type to define the use of a map file

`DEBIAN_102:Linux:Debian-10.2.0.img:`

*  Add a switch

The switches are used to link ports each other. To create one, add it on  /usr/local/etc/netlab/switches.conf

`#TYPE:NAME:List of ports`
for example:`L2:bbb1:bbb1p1`

Be carefull, each port name has to be unique

TYPE: Reserved for future use L2 by default
NAME: Name of the switch (the bridge in the system)
List of port: List of ports associated to the switch

*  Add an external interconnexion

If you want to include a physical interface in a bridge, you have to declare it on  /usr/local/etc/netlab/intercos.conf

`#TYPE:NAME:PHYSICAL INTERFACE`
for example:`L2:bbb1:ixl0`

Be carefull, each port name has to be unique

TYPE: Reserved for future use L2 by default
NAME: Name of the switch (the bridge in the system)
List of port: List of ports associated to the switch

*  Add a machine

To create a machine, add a machine in /usr/local/etc/netlab/machines.conf

`#NAME:TYPE:CPU:MEMORY (in M):PORT:INTERFACES:`
for example : `ESRV_DNS1:BSDRP_197:1:256:3616:eiib4p2`

NAME : name of the machine
TYPE : Type of the machine (describe in templates.conf)
CPU : Number of vcpu allowed
MEMORY (in M) : RAM allocated to the VM
PORT : Telnet port redirection to the serial.
INTERFACES : List of interfaces. They always have to be on the format <switch_name>p<port_number>

* Add an area

An area is a list of machine. To create one, add an area in /usr/local/etc/netlab/areas.conf

`#NAME:MACHINES:`
for example : `LAB_EINE:LAB_EINE_GW EINE_GW1 EINE_GW2:` 

* Status commands

The following command give you the different status :

To have the status of all machines :
`netlab status`

To have the status of a machine
`netlab status -m <name of the machine>`

To have the list of the areas
`netlab status -a all`

To have the status of all machines in a area
`netlab status -a <name of the area>`

* Load commands

To start all machines 
`netlab load`

To start a machine
`netlab load -m <name of the machine>`

To start an area
`netlab load -a <name of the area>`

* Unload commands

To stop all machines 
`netlab unload`

To stop a machine
`netlab unload -m <name of the machine>`

To stop an area
`netlab unload -a <name of the area>`

* Reload commands

To reload all machines 
`netlab reload`

To reload a machine
`netlab reload -m <name of the machine>`

To reload an area
`netlab reload -a <name of the area>`

(What a surprise !)

*  Connection to the machine

The connection command allowed you to make a "telnet localhost <port_number>" but based on a machine name.
To have the list of available machine 
`netlab connect`

To connect to a specific machine
`netlab connect -m <name of the machine>

* Reinstallation and deinstallation  

TODO (just decribe)
