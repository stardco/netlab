# netlab
Virtual network lab on FreeBSD

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

`BSDRP_196:BSDRP-1.96-full-amd64-serial.img::`

If it is a debian, you should add the "yes" to define the use of a map file

`DEBIAN_102:Debian-10.2.0.img:yes:`

*  Add a machine

To create a machine, add a machine in /usr/local/etc/netlab/machines.conf

`#NAME:TYPE:MEMORY (in M):PORT:INTERFACES:`

for example : `Internet_GW:BSDRP_196:256:3000:rnb1p1 igwb1p1:`

NAME : name of the machine
TYPE : Type of the machine (describe in templates.conf)
MEMORY (in M) : RAM allocated to the VM
PORT : Telnet port redirection to the serial. WARNING, port number are not yet controlled !
INTERFACES : List of interfaces. They always have to be on the format <switch_name>p<port_number>

*  Start a machine

To start a machine, use the command netlab-machine :

`netlab-machine -m <machine_name> load`

for example : `netlab-machine -m Internet_GW load`

a <MACHINE_NAME>.img file is created in the "repo" directory

*  Check the status

To check the status of a machine, use the command netlab-machine :

`netlab-machine -m <machine_name> load`

for example : `netlab-machine -m Internet_GW load`

*  Connection to the machine


*  Stop a machine

To stop a machine, use the command netlab-machine :

`netlab-machine -m <machine_name> unload`

for example: `netlab-machine -m Internet_GW unload`

The <MACHINE_NAME>.img file created in the "repo" directory is untouched


* Use area 

TODO (just decribe)


* Reinstallation and deinstallation  

TODO (just decribe)
