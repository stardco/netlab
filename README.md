**1. Introduction**

Netlab is a system to generate quiclky virtual network environment based on FreeBSD or Debian image.

**2. Installation**

To install tape the following commands :
`make install`

- package dependencies

Warning ! A script launch the installation of the application ser2net if it is not present with pkg
Warning ! A script launch the installation of the application gcc if it is not present with pkg

- Compilation
The small tool int2tap is compiled and copy in /usr/local/sbin/ to convert tap interface name to tap device in /dev

- File copies
The files in the folder "files" are copied to /usr/local/sbin/ 

- Configuration files
The files in the folder "confs" are copied to /usr/local/etc/netlab/
If files already exist, a .old are created

- Startup parameters
in /etc/sysctl.conf
`net.link.tap.up_on_open=1` (if the parameter exists it will be modified)

in /boot/loader.conf
`if_tap_load="YES"`
`if_bridge_load="YES"`
`vmm_load="YES"`
`nmdm_load="YES"`

- Running parameter
The following modules are activated
`kldload if_tap`
`kldload if_bridge`
`kldload vmm`
`kldload ndmd`

The sysctl argument is parametered
`sysctl net.link.tap.up_on_open=1`


**3. How to use**

WARNING : all commands have to be done by root !

*  Add a template

Copy an .img file in /usr/local/etc/netlab/templates (for exemple BSDRP-1.97-full-amd64-serial.img)

Create a type associate in the file /usr/local/etc/netlab/templates.conf

NAME : name of the template
TYPE : only BSD or Linux supported
FILENAME : image filename located on /usr/local/etc/netlab/templates/

`BSDRP_197:BSD:BSDRP-1.97-full-amd64-serial.img:`

If it is a debian, you should add the "yes" to define the use of a map file

`DEBIAN_102:Linux:Debian-10.2.0.img:`

*  Add a machine

To create a machine, add a machine in /usr/local/etc/netlab/machines.conf

`#NAME:TYPE:MEMORY (in M):PORT:INTERFACES:`
for example : `BSDTST:BSDRP_197:256:3000:rnb1p1 igwb1p1:`

NAME : name of the machine
TYPE : Type of the machine (describe in templates.conf)
MEMORY (in M) : RAM allocated to the VM
PORT : Telnet port redirection to the serial. WARNING, port number are not yet controlled !
INTERFACES : List of interfaces. They always have to be on the format <switch_name>p<port_number>

*  Start a machine

To start a machine, use the command netlab-machine :

`netlab-machine -m <machine_name> load`
for example : `netlab-machine -m BSDTST load`

a <MACHINE_NAME>.img file is created in the "repo" directory

*  Check the status

To check the status of a machine, use the command netlab-machine :

`netlab-machine -m <machine_name> status`

for example : `netlab-machine -m Internet_GW status`

*  Connection to the machine

`telnet localhost 3000` or `telnet <Server IP> 3000` 
I advice to use tmux...

*  Stop a machine

To stop a machine, use the command netlab-machine :

`netlab-machine -m <machine_name> unload`

for example: `netlab-machine -m Internet_GW unload`

The <MACHINE_NAME>.img file created in the "repo" directory is untouched

* Use area 

To create an area (list of VM) add the list in the areas.conf file
`#NAME:MACHINES:`
NAME : Name of the area
MACHINES : List of machine names (defined in machines.conf)

You can load, unload or reload all machines in an area with the commands

netlab-area -a -<name of the area> load
netlab-area -a -<name of the area> unload
netlab-area -a -<name of the area> reload

* Gateway

THe gateway is the link between the virtual part and the "real world".
In the file interco.conf create a gateway (Layer 2 only)
`#TYPE:SWITCH NAME:PHYSICAL INTERFACE:`
L2:rnb1:ixl0:

TYPE : L2 (Layer 2) only. if the bridge associate has to be created, It will add a physical link
SWITCH NAME : Name of the bridge consider as the interconnexion switch
PHYSICAL INTERFACE : Name of the physical interface member of the interconnexion bridge

* Reinstallation and deinstallation  

`make reinstall` : stop all VM, copy files again without configuration files
`make deinstall` : stop all VM and remove all file except configuration files, templates and repository
