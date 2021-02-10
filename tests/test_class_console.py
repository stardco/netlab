import getopt
import time
from netlab_classes import *

if __name__ == "__main__":
    # Creation of a port
    myConsole1 = Console("SuperMachine",3000,300,"/var/run/netlab/ser2net_session")
     
    # Checks variables
    print("=== Check variables ===")
    print("Machine name :", myConsole1.console_vm_name,end="\t\t")
    print("Port :", myConsole1.console_port,end="\t\t")
    print("Timeout :", myConsole1.console_timeout,end="\t\t")
    print("Index :", myConsole1.console_index,end="\t\t")
    print("PID :", myConsole1.console_pid,end="\t\t")
    print("Session file path :", myConsole1.console_run_file)
    print("=======================")
    
    # Check is_on_run_file
    print("=== Check is_on_run_file() ===")
    print("Should be False :", myConsole1.is_on_run_file())
    print("=======================")  

    # Check console_port_is_used_on_host is the port is empty
    print("=== Check console_port_is_used_on_host() ===")
    print("The port",myConsole1.console_port,"is not used so it should be False",myConsole1.console_port_is_used_on_host())
    # Check console_port_is_used_on_host is the port is used
    myConsole1.console_port = 22
    print("The port",myConsole1.console_port,"is used so it should be True",myConsole1.console_port_is_used_on_host())  
    myConsole1.console_port = 3000  
    print("=======================")     
    
    # Check create_console if not loaded
    print("=== Check create_console() ===")
    print("Create the console on host :", myConsole1.create_console())
    print("is_run_on_file should be True :", myConsole1.is_on_run_file())
    cmd = "ps -ax | grep nmdm" + str(myConsole1.console_index) + "B | grep ser2net | grep -v grep"
    print(subprocess.getoutput(cmd))
    cmd = "cat " + str(myConsole1.console_run_file)
    print(subprocess.getoutput(cmd))
    # Checks variables
    print("Machine name :", myConsole1.console_vm_name,end="\t\t")
    print("Port :", myConsole1.console_port,end="\t\t")
    print("Timeout :", myConsole1.console_timeout,end="\t\t")
    print("Index :", myConsole1.console_index,end="\t\t")
    print("PID :", myConsole1.console_pid,end="\t\t")
    print("Session file path :", myConsole1.console_run_file)
    print("=======================")  
    
    # Check create_console if already loaded
    print("=== Check create_console() if console already loaded ===")
    print("Create the console on host :", myConsole1.create_console())
    print("is_run_on_file should be True :", myConsole1.is_on_run_file())
    cmd = "ps -ax | grep nmdm" + str(myConsole1.console_index) + "B | grep ser2net | grep -v grep"
    print(subprocess.getoutput(cmd))
    cmd = "cat " + str(myConsole1.console_run_file)
    print(subprocess.getoutput(cmd))
    print("=======================")  
    
    # Check destroy_console if loaded
    print("=== Check destroy_console() ===")
    print("Should be True :", myConsole1.destroy_console())
    print("is_run_on_file should be False :", myConsole1.is_on_run_file())
    time.sleep(3)
    cmd = "ps -ax | grep nmdm" + str(myConsole1.console_index) + "B | grep ser2net | grep -v grep"
    print(subprocess.getoutput(cmd))
    cmd = "cat " + str(myConsole1.console_run_file)
    print(subprocess.getoutput(cmd))
    # Checks variables
    print("Machine name :", myConsole1.console_vm_name,end="\t\t")
    print("Port :", myConsole1.console_port,end="\t\t")
    print("Timeout :", myConsole1.console_timeout,end="\t\t")
    print("Index :", myConsole1.console_index,end="\t\t")
    print("PID :", myConsole1.console_pid,end="\t\t")
    print("Session file path :", myConsole1.console_run_file)
    print("=======================") 
    
    # Check destroy_console if not loaded
    print("=== Check destroy_console() ===")
    print("Should be True :", myConsole1.destroy_console())
    print("is_run_on_file should be False :", myConsole1.is_on_run_file())
    time.sleep(3)
    cmd = "ps -ax | grep nmdm" + str(myConsole1.console_index) + "B | grep ser2net | grep -v grep"
    print(subprocess.getoutput(cmd))
    cmd = "cat " + str(myConsole1.console_run_file)
    print(subprocess.getoutput(cmd))
    print("=======================") 