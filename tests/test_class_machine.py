import getopt
from netlab_classes import *


if __name__ == "__main__":
    # Creation of two ports
    myPort1 = Port("port_test1","tap")
    myPort2 = Port("port_test2","tap","myswitch") 
 
    # Creation of a Template
    myTemplate1 = Template('BSDRP','BSD','/usr/local/etc/netlab/templates/BSDRP-1.97-full-amd64-serial.img')
    
    # Creation of a console
    myConsole1 = Console("SuperMachine",3000,300,"/var/run/netlab/ser2net_session")
    
    # Creation of the Machine
    myMachine1 = Machine("SuperMachine",1,256,myConsole1,myTemplate1,"/home",[myPort1,myPort2])
    
    
    # Checks variables and print_vm_port_list
    print("=== Check variables ===")
    print("Name :", myMachine1.vm_name)
    print("CPU :", myMachine1.vm_cpu)
    print("Memory :", myMachine1.vm_mem)
    print("Console port number :",myMachine1.vm_console.console_port)
    print("Template type name :", myMachine1.vm_template.template_name) 
    print("Image path :", myMachine1.vm_datafile) 
    print("Image map path :", myMachine1.vm_datafile_map)    
    print("List of port :", myMachine1.print_vm_port_list())
    print("Running :", myMachine1.vm_running)
    print("Loaded :", myMachine1.vm_loaded)
    print("Int2tap_binary :", myMachine1.vm_int2tap_bin)
    print("=======================")
    
    # Check print_status
    print("\n=== Check print_status ===")
    print("{:<20} | {:<15} | {:<3} | {:<5} | {:<5} | {:<60} | {:<25}".format("NAME","TYPE","CPU","MEM","PORT","INTERFACES","STATUS"))
    print(myMachine1.print_status())
    print("==========================")
    
    # Check load machine
    print("\n=== Check load() ===")
    myMachine1.load()
    time.sleep(5)
    print("{:<20} | {:<15} | {:<3} | {:<5} | {:<5} | {:<60} | {:<25}".format("NAME","TYPE","CPU","MEM","PORT","INTERFACES","STATUS"))
    print(myMachine1.print_status())
    print("Port1 status :",myPort1.exists_on_host())
    print("Port2 status :",myPort2.exists_on_host())
    print("Console is on run file :",myConsole1.is_on_run_file())
    print("==========================")   
    
    input()
    
    # Check unload machine
    print("\n=== Check unload() ===")
    myMachine1.unload()
    print("{:<20} | {:<15} | {:<3} | {:<5} | {:<5} | {:<60} | {:<25}".format("NAME","TYPE","CPU","MEM","PORT","INTERFACES","STATUS"))
    print(myMachine1.print_status())
    print("Port1 status :",myPort1.exists_on_host())
    print("Port2 status :",myPort2.exists_on_host())
    print("Console is on run file :",myConsole1.is_on_run_file())
    print("==========================")  
    
    # Check reload machine
    print("\n=== Check reload() ===")
    myMachine1.reload()
    time.sleep(1)
    print("{:<20} | {:<15} | {:<3} | {:<5} | {:<5} | {:<60} | {:<25}".format("NAME","TYPE","CPU","MEM","PORT","INTERFACES","STATUS"))
    print(myMachine1.print_status())
    print("Port1 status :",myPort1.exists_on_host())
    print("Port2 status :",myPort2.exists_on_host())
    print("Console is on run file :",myConsole1.is_on_run_file())
    print("==========================")  
    
    time.sleep(1)
    
    # Check unload machine
    print("\n=== Check unload() ===")
    myMachine1.unload()
    print("{:<20} | {:<15} | {:<3} | {:<5} | {:<5} | {:<60} | {:<25}".format("NAME","TYPE","CPU","MEM","PORT","INTERFACES","STATUS"))
    print(myMachine1.print_status())
    print("Port1 status :",myPort1.exists_on_host())
    print("Port2 status :",myPort2.exists_on_host())
    print("Console is on run file :",myConsole1.is_on_run_file())
    print("==========================")
    