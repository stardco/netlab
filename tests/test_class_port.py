import getopt
from netlab_classes import *

if __name__ == "__main__":
    # Creation of three ports
    myPort1 = Port("port_test1","tap")
    myPort2 = Port("port_test2","tap","myswitch")
    myPort3 = Port("bce2","physical")
    
    # Checks variables and exists_on_host function
    print("Name :",myPort1.port_name,end="\t\t")
    print("Type :",myPort1.port_type,end="\t\t")
    print("Associated Switch Name :",myPort1.port_associated_sw_name,end="\t\t")
    print("Actives ? :",myPort1.port_active,end="\t\t")
    print("Exists on host ? :",myPort1.exists_on_host())
        
    print("Name :",myPort2.port_name,end="\t\t")
    print("Type :" + myPort2.port_type,end="\t\t")
    print("Associated Switch Name :",myPort2.port_associated_sw_name,end="\t\t")
    print("Actives ? :",myPort2.port_active,end="\t\t")
    print("Exists on host ? :",myPort2.exists_on_host())

    print("Name :",myPort3.port_name,end="\t\t")
    print("Type :",myPort3.port_type,end="\t\t")
    print("Associated Switch Name :",myPort3.port_associated_sw_name,end="\t\t")
    print("Actives ? :",myPort3.port_active,end="\t\t")
    print("Exists on host ? :",myPort3.exists_on_host())    
    
    # Activation of the port
    print("=== Port 1 activation ===")
    myPort1.set_port()
    cmd = shlex.split("ifconfig " + myPort1.port_name)
    result = subprocess.run(cmd)
    print("Actives ? :",myPort1.port_active,end="\t\t")
    print("Exists on host ? :",myPort1.exists_on_host())
    
    # Second activation of the port 
    print("=== Second Port 1 activation, it should change nothing ===")
    myPort1.set_port()
    cmd = shlex.split("ifconfig " + myPort1.port_name)
    result = subprocess.run(cmd)
    print("Actives ? :",myPort1.port_active,end="\t\t")
    print("Exists on host ? :",myPort1.exists_on_host())
    
    # Deactivation of the port
    print("=== Port 1 deactivation ===")
    myPort1.unset_port()
    cmd = shlex.split("ifconfig " + myPort1.port_name)
    result = subprocess.run(cmd)
    print("Actives ? :",myPort1.port_active,end="\t\t")
    print("Exists on host ? :",myPort1.exists_on_host())
    
    # Second deactivation of the port
    print("=== Second Port 1 deactivation, it should change nothing ===")
    myPort1.unset_port()
    cmd = shlex.split("ifconfig " + myPort1.port_name)
    result = subprocess.run(cmd)
    print("Actives ? :",str(myPort1.port_active),end="\t\t")
    print("Exists on host ? :",str(myPort1.exists_on_host()))
    