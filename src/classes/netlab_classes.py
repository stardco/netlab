import sys
import re
import shlex
import os.path
import subprocess
import time

#############
## CLASSES ##
#############
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
                self.template_list.append(Template(template_entry[0], template_entry[1], self.path_templates + template_entry[2]))
 
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
     
class Machine:
    def __init__(self, name, cpu, mem, console, template, path, port_list = []):
    # Initialization of the Machine
        self.vm_int2tap_bin = "int2tap"
        self.vm_name = name
        self.vm_cpu = cpu
        self.vm_mem = mem
        self.vm_console = console
        self.vm_template = template
        self.vm_port_list = port_list
        self.vm_datafile = path + "/" + self.vm_name + ".img"
        self.vm_datafile_map = ""
        self.set_status()
        
    def print_status(self):
    # Return a String with the status of the machine with format
        self.set_status()
        if self.vm_loaded:
            status = "loaded"
        else:
            status = "unloaded"
        if self.vm_running:
            status += " running"
        else:
            status += " stopped"
        res = "{:<20} | {:<15} | {:<3} | {:<5} | {:<5} | {:<60} | {:<25}".format(self.vm_name, self.vm_template.template_name, self.vm_cpu, self.vm_mem, self.vm_console.console_port, self.print_vm_port_list(), status)
        return res

    def print_vm_port_list(self):
    # Return a String with the port_name of the Ports in vm_port_list
        res = ""
        for port in self.vm_port_list:
            res = res + port.port_name + " "
        return res
    
    def set_status(self):
    # Check and update the status of the machine in the host
        if os.path.exists("/dev/vmm/" + self.vm_name):
            self.vm_loaded = True
        else:
            self.vm_loaded = False
        if not subprocess.getoutput("ps -ax | grep -v \"grep\" | grep \"bhyve: " + self.vm_name + " \"") == "":
            self.vm_running = True
        else:
            self.vm_running = False
       
    def set_vm_datafile(self):
    # If needed, It checks th datafile (.img) of the vm
        datafiles_good = True
        if not os.path.exists(self.vm_datafile):
            cmd = shlex.split("cp " + self.vm_template.template_image + " " + self.vm_datafile)
            result = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            result.wait()
            if result.returncode == 1:
                datafiles_good = False
        if self.vm_template.template_core == "Linux" and datafiles_good:
            list_param = self.vm_datafile.split(".")
            list_param[-1] = "map"
            self.vm_datafile_map = ".".join(list_param)
            if not os.path.exists(self.vm_datafile):
                cmd = shlex.split("echo \"(hd0) " + self.vm_datafile + "\" > " + self.vm_datafile_map)
                result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if result == 1:
                    datafiles_good = False   
        return datafiles_good
    
    def int2tap(self, port_name): 
    # Return a String with the resule of the int2tap binary
        cmd = self.vm_int2tap_bin + " -i " + port_name
        res = subprocess.getoutput(cmd)
        return res
        
    def load(self):
    # Load the machine on the host
        network = ""
        volume = ""
        console = ""
        go_to_load = True
        # Check if the machine is already loaded
        if self.vm_loaded:
            print("Machine already loaded")
            go_to_load = False
        # Creation of the network part of the command
        if go_to_load:
            cpt = 0
            for port in self.vm_port_list:
                if not port.exists_on_host():
                    port.set_port()
                network = network + "-s 2:" + str(cpt) + ",virtio-net," + self.int2tap(port.port_name) + " "
                cpt = cpt + 1
        # Creation of the hard disk part of the command 
        if go_to_load:
            if self.set_vm_datafile():
                volume = "-s 1:0,virtio-blk," + self.vm_datafile
            else:
                go_to_load = False

        # Creation of the console part of the command
        if go_to_load:
            if self.vm_console.create_console():
                console = "-s 31,lpc -l com1,/dev/nmdm" + str(self.vm_console.console_index) + "A"
            else:
                go_to_load = False         
     
        # Load the vm
        if go_to_load:
            if self.vm_template.template_core == "Linux":
                bhyve_load = "grub-bhyve -c /dev/null -m " + self.vm_datafile_map + " -r hd0,msdos1 -M " + str(self.vm_mem) + " " + self.vm_name
            else:
                bhyve_load = "bhyveload -c /dev/null -m "+ str(self.vm_mem) + " -d " + self.vm_datafile + " " + self.vm_name   
            bhyve_cmd = "bhyve -c " + str(self.vm_cpu) + " -m " + str(self.vm_mem) + " -A -H -P -s 0:0,hostbridge " + volume + " " + network + " " + console + " " + self.vm_name
            p_load = subprocess.Popen(shlex.split(bhyve_load))
            p_load.wait()
            p_cmd = subprocess.Popen(shlex.split(bhyve_cmd),close_fds=True)
            
    def unload(self):
    # Unload the machine on the host
         # Check if the machine is already loaded
        if self.vm_running:
            bhyve_stop = "bhyvectl --force-poweroff --vm=" + self.vm_name
            p_stop = subprocess.Popen(shlex.split(bhyve_stop))
            p_stop.wait()
            
        if self.vm_loaded:
            bhyve_destroy = "bhyvectl --destroy --vm=" + self.vm_name
            p_destroy = subprocess.Popen(shlex.split(bhyve_destroy))

        # Shut the network part
        for port in self.vm_port_list:
            port.unset_port() 
                
        # Shut of the console part
        self.vm_console.destroy_console()
        
    def reload(self):
    # Unload and load the machine on the host
        self.unload()
        time.sleep(2)
        self.load()

class Switch:
    def __init__(self, switch_name, switch_type = "L2"):
    # Initialization of the Switch
        self.sw_name = switch_name
        self.sw_type = switch_type
        self.sw_port_list = []
        self.sw_active = self.exists_on_host()

    def update_sw(self):
    # Update the switch on the host, remove itself if no more tap interface is linked on it, create itself on host if needed
    # The procedure also add tap member on itself 
        active = False
        lst_physical_port = []
        for port in self.sw_port_list:
            if port.port_type == "physical":
                lst_physical_port.append(port)
                continue
            if port.exists_on_host():
                active = True
                self.set_sw()
                if not self.associated_on_host(port.port_name):
                    cmd = shlex.split("ifconfig " + self.sw_name + " addm " + port.port_name)
                    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
        if active:
            for port in lst_physical_port:
                if not self.associated_on_host(port.port_name):
                    cmd = shlex.split("ifconfig " + self.sw_name + " addm " + port.port_name)
                    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            for port in lst_physical_port:
                if self.associated_on_host(port.port_name):
                    cmd = shlex.split("ifconfig " + self.sw_name + " deletem " + port.port_name)
                    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.unset_sw()

    def associated_on_host(self,port_name):
    # Check if a tap interface is already associated to itself on the host
        res = False
        if self.exists_on_host():
            if not subprocess.getoutput("ifconfig " + self.sw_name + " | grep member: \"" + port_name + "\"") == "":
                res = True
    
    def set_sw(self):
    # Create the switch on the host
        if not self.exists_on_host():
            cmd = shlex.split("ifconfig bridge create name " + self.sw_name + " up")
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                res = True
            else:
                res = False
        else:
            res = False
        self.sw_active = self.exists_on_host()
        return res
    
    def unset_sw(self):
    # Destroy the switch on the host (without question)
        if self.exists_on_host():
            cmd = shlex.split("ifconfig " + self.sw_name + " destroy")
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                res = True
            else:
                res = False
        else:
            res = False
        self.sw_active = self.exists_on_host()
        return res

    def add_port(self, port):
    # Add a Port in the port list and check if the port already exist in the sw_port_list
        if not self.port_exists(port.port_name):
            port.port_associated_sw_name = self.sw_name
            self.sw_port_list.append(port)
        else:
            print("Error ! The name",port.port_name,"of the port already exist")
        
    def exists_on_host(self):
    # Check if the switch already exists on the host
        cmd = shlex.split("ifconfig " + self.sw_name)
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            res = True
        else:
            res = False
        return res
    
    def port_exists(self, port_name):
    # Check if a port exists ont th sw_port_list
        exists = False
        for port in self.sw_port_list:
            if port.port_name == port_name:
                exists = True
                break
        return exists
 
    def port_active(self, port_name):
    # Check if a port is active on the host
        res = False
        for port in self.sw_port_list:
            if port.port_name == port_name:
                res = port.port_active
                break
        return res
 
    def port_index(self, port_name):
    # Return the index where the port_name is located in sw_port_list or return -1
        res = 0
        for port in self.sw_port_list:
            if port.port_name == port_name:
                break
            else:
                res += 1
        if (res + 1) > len(self.sw_port_list):
            res = -1
        return res
    
    def print_sw_port_list(self):
    # return a String with the port_name of the port in the sw_port_list
        res = ""
        for port in self.sw_port_list:
            res = res + port.port_name + " "
        return res
     
class Port: 
    def __init__(self, port_name, port_type = "tap", sw_name = ""):
    # Initialization of the Port
        self.port_name = port_name
        self.port_type = port_type
        self.port_active = self.exists_on_host()
        self.port_associated_sw_name = sw_name
        
    def set_port(self):
    # Create the port on the host
        if not self.exists_on_host():
            cmd = shlex.split("ifconfig tap create name " + self.port_name)
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                res = True
            else:
                res = False
        else:
            res = False
        self.port_active = self.exists_on_host()
        return res
    
    def unset_port(self):
    # Destroy the port on the host
        if self.exists_on_host():
            res = True
            cmd = shlex.split("ifconfig " + self.port_name + " destroy")
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                res = True
            else:
                res = False
        else:
            res = False
        
        self.port_active = self.exists_on_host()
        return res
        
    def exists_on_host(self):
    # Check if the port already exists on the host
        cmd = shlex.split("ifconfig " + self.port_name)
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            res = True
        else:
            res = False
        return res    
  
class Console:
    def __init__(self, vm_name, port, timeout, run_file):
    # Initialization of the Console
        self.console_vm_name = vm_name
        self.console_port = port
        self.console_timeout = timeout
        self.console_index = -1
        self.console_pid = -1
        self.console_run_file = run_file
        self.is_on_run_file()
    
    def console_port_is_used_on_host(self):
    # Check if the port (TCP) is used on the host
        res = ""
        cmd = "netstat -46an | grep \"." + str(self.console_port) + " \""
        res = subprocess.getoutput(cmd)
        if res == "":
            result = False
        else:
            result = True
        return result
            
    def is_on_run_file(self):
    # Check if the console is already loaded on host
        res = False
        f = open(self.console_run_file,"r")
        ser2net_entries = f.readlines()
        f.close()
        for entry in ser2net_entries:
            entry = entry.replace("\n","")
            entry = entry.split(":")
            if entry[0] == self.console_vm_name:
                self.console_index = entry[1]
                self.console_pid = entry[2]
                res = True
                break
        return res
    
    def destroy_console(self):
    # Unconfigure the console on the host
        result = True
        if self.is_on_run_file():
            f = open(self.console_run_file,"r")
            file_entry = f.readlines()
            f.close()
            f = open(self.console_run_file,"w")
            for entry in file_entry:
                if not entry.split(":")[0] == self.console_vm_name:
                    f.writelines([entry])
            f.close()
            cmd = shlex.split("kill " + str(self.console_pid))
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if not res.returncode == 0:
                result = False
            else:
                self.console_index = -1
                self.console_pid = -1
        return result
    
    def create_console(self):
    # Configure the console on the host
        result = True
        if not self.is_on_run_file() and not self.console_port_is_used_on_host():
            f = open(self.console_run_file,"r")
            file_entries = f.readlines()
            f.close()            
            num_console = 0
            if file_entries:
                restart = True
            else:
                restart = False
                
            while restart:
                restart = False
                for entry in file_entries:
                    if int(entry.split(":")[1]) == num_console:
                        num_console = num_console + 1 
                        restart = True
                        break

            self.console_index = num_console
            cmd = shlex.split("ser2net -C " + str(self.console_port) + ":telnet:" + str(self.console_timeout) + ":/dev/nmdm" + str(self.console_index) + "B")
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode == 0:
                cmd = "ps -ax | grep nmdm" + str(self.console_index) + "B | grep ser2net | grep -v grep"
                self.console_pid = subprocess.getoutput(cmd).lstrip().split(" ")[0]
                f = open(self.console_run_file,"a")
                f.writelines([self.console_vm_name + ":" + str(self.console_index) + ":" + str(self.console_pid) + "\n"])
                f.close()
            else:
                print("Error in the creation of console link")
                result = False
        return result
    
    def connect_console(self):
    # Make a telnet conection on the console port
        if self.is_on_run_file():
            print("The port is active. Tape CTRL + $ and quit to exit telnet")
            telnet_cmd = "telnet localhost " + str(self.console_port)
            p_cmd = subprocess.Popen(shlex.split(telnet_cmd),close_fds=True)
        else:
            print("The port of",self.console_vm_name,"is not active")
           
            
class Area:
    def __init__(self, name, vm_list):
    # Initialization of the Area
        self.area_name = name
        self.area_vm_list = vm_list

    def print_area_vm_list(self):
    # Print the name of the machine listed in area_vm_list
        vm_names = ""
        for vm in self.area_vm_list:
            vm_names = vm_names + vm.vm_name + " "
        return vm_names

class Template:
    def __init__(self, name, core, image, files = ["none"]):
    # Initialization of the Template
        self.template_name = name
        self.template_core = core
        self.template_image = image
        self.template_files = files
