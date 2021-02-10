import getopt
from netlab_classes import *

if __name__ == "__main__":
    # Creation of the switches 
    mySwitch = Switch("testb1")
    
    # Checks variables
    print("=== Check variables ===")
    print("Name :", mySwitch.sw_name,end="\t\t")
    print("Type :", mySwitch.sw_type,end="\t\t")
    print("Actives ? :", mySwitch.sw_active,end="\t\t")
    print("Exists on host ? :", mySwitch.exists_on_host())
    print("=======================")
    
    print("\n=== Test add_port, port_exist, port_active, port_index, sw_port list and print_sw_port_list ===")
    # Add a list of ports
    mySwitch.add_port(Port("testb1p1","tap"))
    mySwitch.add_port(Port("testb1p2","tap"))
    mySwitch.add_port(Port("bce2","physical"))
    
    # Add an existing port
    print("Port \"testb1p2\" exists so it should be True:",mySwitch.port_exists("testb1p2"))
    mySwitch.add_port(Port("testb1p2","tap"))
    
    # Test an active and an inactive port
    print("Port \"testb1p2\" is not active so it should be False:",mySwitch.port_active("testb1p2"))
    print("Port \"bce2\" is active so it should be True:",mySwitch.port_active("bce2"))
    
    # Check position of switches in list
    print("Port \"testb1p1\" is on the position 0:",mySwitch.port_index("testb1p1"))
    print("Port \"testb1p2\" is on the position 1:",mySwitch.port_index("testb1p2"))
    print("Port \"bce2\" is on the position 2:",mySwitch.port_index("bce2"))
    
    # Test print_sw_port_list function
    print("List of port associated :", mySwitch.print_sw_port_list())
        
    # Validation of add_port added values
    print("First port associated switch :", mySwitch.sw_port_list[0].port_associated_sw_name)
    print("==========================================================")
    
    # Test associated_on_host
    print("\n=== Test associated_on_host ===")
    print("A tap port is not associated on host so it sould be False:",mySwitch.associated_on_host("testb1p1"))
    print("=================================")
    
    # Test set_sw function
    print("\n=== Test set_sw ===")
    mySwitch.set_sw()
    cmd = shlex.split("ifconfig " + mySwitch.sw_name)
    result = subprocess.run(cmd)
    print("Actives ? :", mySwitch.sw_active,end="\t\t")
    print("Exists on host ? :", mySwitch.exists_on_host())
    print("=====================")
    
    # Test unset_sw function
    print("\n=== Test unset_sw ===")
    mySwitch.unset_sw()
    cmd = shlex.split("ifconfig " + mySwitch.sw_name)
    result = subprocess.run(cmd)
    print("Actives ? :", mySwitch.sw_active,end="\t\t")
    print("Exists on host ? :", mySwitch.exists_on_host())
    print("=====================")
    
    # Test sw_update
    print("\n=== Test update_sw ===")
    # no port tap activated
    mySwitch.update_sw()
    print("Exists on host ? No tap ports actives (only physical), should be False:", mySwitch.exists_on_host())
    
    # One port tap activated
    mySwitch.sw_port_list[0].set_port()
    mySwitch.update_sw()
    
    # Test associated_on_host
    print("\n=== Test associated_on_host ===")
    print("A tap port is associated on host so it sould be False:",mySwitch.associated_on_host("testb1p1"))
    print("=================================")
    
    # Check if switch is activated
    print("Exists on host ? One port tap actives (plus physical), should be True:", mySwitch.exists_on_host())
    cmd = shlex.split("ifconfig " + mySwitch.sw_name)
    result = subprocess.run(cmd)
    
    # Test sw_update Two ports tap activated
    mySwitch.sw_port_list[1].set_port()
    mySwitch.update_sw()
    print("Exists on host ? Two ports active (plus physical), should be True:", mySwitch.exists_on_host())
    cmd = shlex.split("ifconfig " + mySwitch.sw_name)
    result = subprocess.run(cmd)
    
    # Test sw_update deactivation of all ports except physical
    mySwitch.sw_port_list[0].unset_port()
    mySwitch.sw_port_list[1].unset_port()
    mySwitch.update_sw()
    print("Exists on host ? Only physical port actives, should be False:", mySwitch.exists_on_host())
    cmd = shlex.split("ifconfig " + mySwitch.sw_name)
    result = subprocess.run(cmd)
    print("======================")
 