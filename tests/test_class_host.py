import getopt
from netlab_classes import *

if __name__ == "__main__":
    # Creation of the host
    myHost = Host()
    
    
    # Checks variables
    print("=== Check variables ===")
    print("Path netlab :", myHost.path_netlab)
    print("Path repo :", myHost.path_run)
    print("Path repo :", myHost.path_repo)
    print("Path templates :", myHost.path_templates)
    print("Configuration file templates :", myHost.file_conf_templates)
    print("Configuration file machines :", myHost.file_conf_machines)
    print("Configuration file switches :", myHost.file_conf_switches)
    print("Configuration file intercos :", myHost.file_conf_intercos)
    print("Configuration file area :", myHost.file_conf_areas)
    print("List of template :", myHost.print_template_list())
    print("List of machine :", myHost.print_machine_list())
    print("List of switches :", myHost.print_sw_list())
    print("List of area :", myHost.print_area_list())
    print("=======================")
    print("=== Print list of port for each switch ===")
    for sw in myHost.sw_list:
        print("Switch :",sw.sw_name)
        print(sw.print_sw_port_list())
    print("=== Print list of machine for each area ===")
    for area in myHost.area_list:
        print("Area :",area.area_name)
        print(area.print_area_vm_list())     
    
