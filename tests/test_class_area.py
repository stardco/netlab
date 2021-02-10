import getopt
from netlab_classes import *

if __name__ == "__main__":
    # Creation of two ports
    myPort1 = Port("port_test1","tap")
    myPort2 = Port("port_test2","tap","myswitch") 
    myPort3 = Port("port_test3","tap")
    myPort4 = Port("port_test4","tap","myswitch") 
 
    # Creation of a Template
    myTemplate1 = Template('BSDRP','BSD','/usr/local/etc/netlab/templates/BSDRP-1.97-full-amd64-serial.img')
    
    # Creation of a console
    myConsole1 = Console("SuperMachine1",3000,300,"/var/run/netlab/ser2net_session")
    myConsole2 = Console("SuperMachine2",3001,300,"/var/run/netlab/ser2net_session")
    
    # Creation of the Machine
    myMachine1 = Machine("SuperMachine1",1,256,myConsole1,myTemplate1,"/home",[myPort1,myPort2])
    myMachine2 = Machine("SuperMachine2",1,256,myConsole2,myTemplate1,"/home",[myPort3,myPort4])

    # Creation of a port
    myArea1 = Area('SuperArea',[myMachine1, myMachine2])
    
    # Checks variables
    print("=== Check variables ===")
    print("Name :", myArea1.area_name,end="\t\t")
    print("Type :", myArea1.print_area_vm_list())
    print("=======================")