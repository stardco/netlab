#!/usr/local/bin/python3.7

import getopt
from netlab_classes import *

##################
## TOOLS
##################

def usage():
    print("netlab load | unload | reload | status | connect -h --help")
    print("load, unload, reload options")
    print("load : loading operations")
    print("unload : unloading operations")
    print("reload : unloading and loading operations")
    print("status : status of one machine, one area or all machines")
    print ("-m <machine> | -a <area>")
    print("-h : print this message")

def main(argv):
    global myVm
    global myArea
    
    try:
        opts, args = getopt.getopt(argv, "hm:a:", ["help", "machine=", "area="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-v", "--verbose"):
            global verbose
            verbose = 1
        elif opt in ("-l", "--light"):
            global status_light
            status_light = 1
        elif opt in ("-m", "--machine"):
            global myVm
            myVm = arg
        elif opt in ("-a", "--area"):
            global myArea
            myVm = arg
         
if __name__ == "__main__":
    main(sys.argv[2:])
    command_netlab = sys.args[1]
    myHost = Host()     
    if command_netlab == "status":
        print("Status")
        netlab_status()
    elif command_netlab == "load":
        print("Load")
    elif command_netlab == "unload":
        print("Unload")
    elif command_netlab == "reload":
        print("Reload")
    elif command_netlab == "connect":
        print("Connect")

  
  
  
def netlab_status(host,vm="", area=""):
    print("{:<20} | {:<15} | {:<3} | {:<5} | {:<5} | {:<60} | {:<25}".format("NAME","TYPE","CPU","MEM","PORT","INTERFACES","STATUS"))
    if vm:
        # print VM
    elif area:
        # print Area
    else:
        print("all")       

