from netlab_area import *
from netlab_console import *
from netlab_machine import *
from netlab_port import *
from netlab_switch import *
from netlab_template import *

class Host:
    def __init__(self):
        self.path_netlab = "/usr/local/etc/netlab"
        self.path_run = "/var/run/netlab"
        self.path_repo = self.path_netlab + "/repo"
        self.path_templates = self.path_netlab + "/templates"
        self.file_conf_templates = self.path_netlab + "/templates.conf"
        self.file_conf_machines = self.path_netlab + "/machines.conf"
        self.file_conf_switches = self.path_netlab + "/switches.conf"
        self.file_conf_intercos = self.path_netlab + "/intercos.conf"
        self.file_conf_areas = self.path_netlab + "/areas.conf"
        self.template_list = [] 
        self.set_template_list()
        self.sw_list = []
        self.set_sw_list()
        self.set_interco_list()
        self.machine_list = []
        self.set_list_machine()
        self.area_list = []
        self.set_area_list()

    ############################################################
    #### Function needed for the intitialization of the host ###
    ############################################################

    def set_template_list(self):
    # Parse the file define in file_conf_templates and populate template_list
        f = open(self.file_conf_templates,"r")
        template_entries = f.readlines()
        f.close()
        for template_entry in template_entries:
            template_entry = template_entry.replace("\n","")
            template_entry = template_entry.split(":")
            if not template_entry[0][0] == "#" and not template_entry[0][0] == "" and not self.template_exists(template_entry[0]):
                self.template_list.append(Template(template_entry[0], template_entry[1], self.path_templates + "/" + template_entry[2]))
 
    def set_sw_list(self):
    # Parse the file define in file_conf_switches and populate sw_list
        f = open(self.file_conf_switches,"r")
        switch_entries = f.readlines()
        f.close()
        for switch_entry in switch_entries:
            switch_entry = switch_entry.replace("\n","")
            switch_entry = switch_entry.split(":")
            if not switch_entry[0][0] == "#" and not switch_entry[0][0] == "":
                index = self.sw_index(switch_entry[1])
                if index == -1:
                    self.sw_list.append(Switch(switch_entry[1],switch_entry[0]))
                    index = self.sw_index(switch_entry[1])
                switch_entry[2] = switch_entry[2].split(" ")
                for port in switch_entry[2]:
                    self.sw_list[index].add_port(Port(port,"tap"))
                  
    def set_interco_list(self):
    # Parse the file define in file_conf_intercos and populate sw_list
        f = open(self.file_conf_intercos,"r")
        switch_entries = f.readlines()
        f.close()
        for switch_entry in switch_entries:
            switch_entry = switch_entry.replace("\n","")
            switch_entry = switch_entry.split(":")
            if not switch_entry[0][0] == "#" and not switch_entry[0][0] == "":
                index = self.sw_index(switch_entry[1])
                if index == -1:
                    self.sw_list.append(Switch(switch_entry[1],switch_entry[0]))
                    index = self.sw_index(switch_entry[1])
                switch_entry[2] = switch_entry[2].split(" ")
                for port in switch_entry[2]:
                    self.sw_list[index].add_port(Port(port,"physical"))

    def set_area_list(self):
    # Parse the file define in file_conf_areas and populate area_list
        f = open(self.file_conf_areas,"r")
        area_entries = f.readlines()
        f.close()
        for area_entry in area_entries:
            area_entry = area_entry.replace("\n","")
            area_entry = area_entry.split(":")
            if not area_entry[0][0] == "#" and not area_entry[0][0] == "" and not self.area_exists(area_entry[0]):
                area_entry[1] = area_entry[1].split(" ")
                vm_list = []
                for machine in area_entry[1]:
                    index = self.machine_index(machine)
                    if not index == -1:
                        vm_list.append(self.get_machine(machine))
                self.area_list.append(Area(area_entry[0], vm_list)) 
 
    def set_list_machine(self):
    # Parse the file define in file_conf_machines and populate machine_list
        f = open(self.file_conf_machines,"r")
        machine_entries = f.readlines()
        f.close()
        for machine_entry in machine_entries:
            machine_entry = machine_entry.replace("\n","")
            machine_entry = machine_entry.split(":")
            port_list = []
            # If the machine is not comment
            if not machine_entry[0][0] == "#" and not machine_entry[0][0] == "":
                # Name of the machine
                name = machine_entry[0]
                # Type of Machine
                template = self.template_list[self.template_index(machine_entry[1])]
                # Number of CPU
                cpu = machine_entry[2]
                # Amoung of memory
                mem = machine_entry[3]
                # Console
                console = Console(name,machine_entry[4],300,"/var/run/netlab/ser2net_session")
                
                # Ports part for a machine
                machine_entry[-1] = machine_entry[-1].split(" ")
                for port_name in machine_entry[-1]:
                    port_list.append(self.find_port_in_switches(port_name))
                                
                # Add a new machine in list
                self.machine_list.append(Machine(name,cpu,mem,console,template,self.path_repo,port_list))
    
    ##################################################
    #### Function dedicated on action on the lists ###
    ##################################################    
    
    def sw_exists(self, sw_name):
    # Test if a switch exists
        res = False
        for sw in self.sw_list:
            if sw_name == sw.sw_name:
                res = True
                break
        return res
        
    def sw_index(self, sw_name):
    # Find the position of a switch in the list of switches or return -1
        res = 0
        for sw in self.sw_list:
            if sw_name == sw.sw_name:
                break
            else:
                res += 1
        if (res + 1) > len(self.sw_list):
            res = -1
        return res
    
    def find_port_in_switches(self,port_name):
    # Find a port included in the list of switches and return it    
        port_return = ""
        for switch in self.sw_list:
            index = switch.port_index(port_name)
            if not index == -1:
                port_return = switch.sw_port_list[index]
                break
        return port_return

    def print_sw_list(self):
    # Return a string with all the switch in the list 
        sw_names = ""
        for sw in self.sw_list:
            sw_names = sw_names + sw.sw_name + " "
        return sw_names

    def get_switch(self, switch_name):
    # Return the Switch object if it exists
        res = False
        for switch in self.sw_list:
            if switch_name == switch.sw_name:
                res = True
                break
        if res:
           return switch 
           
    def template_exists(self, template_name):
    # Test if a template exists
        res = False
        for template in self.template_list:
            if template_name == template.template_name:
                res = True
                break
        return res

    def template_index(self, template_name):
    # Find the position of a template in the list of templates or return -1    
        res = 0
        for template in self.template_list:
            if template_name == template.template_name:
                break
            else:
                res += 1
        if (res + 1) > len(self.template_list):
            res = -1
        return res
    
    def print_template_list(self):
    # Return a string with all the template in the list    
        template_names = ""
        for template in self.template_list:
            template_names = template_names + template.template_name + " "
        return template_names

    def get_area(self, area_name):
    # Return the Area object if it exists
        res = False
        for area in self.area_list:
            if area_name == area.area_name:
                res = True
                break
        if res:
           return area
           
    def area_exists(self, area_name):
    # Test if a area exists
        res = False
        for area in self.area_list:
            if area_name == area.area_name:
                res = True
                break
        return res

    def area_index(self, area_name):
    # Find the position of a area in the list of areas or return -1    
        res = 0
        for area in self.area_list:
            if area_name == area.area_name:
                break
            else:
                res += 1
        if (res + 1) > len(self.area_list):
            res = -1
        return res

    def print_area_list(self):
    # Return a string with all the area in the list        
        area_names = ""
        for area in self.area_list:
            area_names = area_names + area.area_name + " "
        return area_names    

    def get_machine(self, machine_name):
    # Return the Machine object if it exists
        res = False
        for machine in self.machine_list:
            if machine_name == machine.vm_name:
                res = True
                break
        if res:
           return machine 
        
    def machine_exists(self, machine_name):
    # Test if a machine exists
        res = False
        for machine in self.machine_list:
            if machine_name == machine.vm_name:
                res = True
                break
        return res

    def machine_index(self, machine_name):
    # Find the position of a machine in the list of machines or return -1    
        res = 0
        for machine in self.machine_list:
            if machine_name == machine.vm_name:
                break
            else:
                res += 1
        if (res + 1) > len(self.machine_list):
            res = -1
        return res

    def print_machine_list(self):
    # Return a string with all the machine in the list        
        machine_names = ""
        for machine in self.machine_list:
            machine_names = machine_names + machine.vm_name + " "
        return machine_names