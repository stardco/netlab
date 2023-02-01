import shlex
import os
import subprocess

class Machine:
    # Initialization of the Machine
    def __init__(self, name, cpu, mem, console, template, path, port_list = []):
        self.vm_name = name
        self.vm_cpu = cpu
        self.vm_mem = mem
        self.vm_console = console
        self.vm_template = template
        self.vm_port_list = port_list
        self.vm_datafile = path + "/" + self.vm_name + ".img"
        self.vm_datafile_map = ""
        self.set_status()

    # Return a String with the status of the machine with format   
    def print_status(self):
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

    # Return a String with the port_name of the Ports in vm_port_list
    def print_vm_port_list(self):
        res = ""
        for port in self.vm_port_list:
            res = res + port.port_name + " "
        return res

    # Check and update the status of the machine in the host   
    def set_status(self):
        if os.path.exists("/dev/vmm/" + self.vm_name):
            self.vm_loaded = True
        else:
            self.vm_loaded = False
        if not subprocess.getoutput("ps -ax | grep -v \"grep\" | grep \"bhyve: " + self.vm_name + " \"") == "":
            self.vm_running = True
        else:
            self.vm_running = False

    # If needed, It checks th datafile (.img) of the vm   
    def set_vm_datafile(self):
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
            print(self.vm_datafile_map)
            if not os.path.exists(self.vm_datafile_map):
                f = open(self.vm_datafile_map,"w")
                f.write("(hd0) " + self.vm_datafile + "\n")
        return datafiles_good
    
    # Load the machine on the host
    def load(self,verbose=True):
        if verbose:
            print("Loading",self.vm_name,"...",end=' ',flush=True)
        network = ""
        volume = ""
        console = ""
        go_to_load = True
        # Check if the machine is already loaded
        if self.vm_loaded:
            if verbose:
                print("Machine already loaded")
            go_to_load = False
        # Creation of the network part of the command
        if go_to_load:
            cpt = 0
            for port in self.vm_port_list:
                if not port.exists_on_host():
                    port.set_port()
                network = network + "-s 2:" + str(cpt) + ",virtio-net," + os.readlink("/dev/" + port.port_name) + " "
                cpt = cpt + 1
        # Creation of the hard disk part of the command 
        if go_to_load:
            if self.set_vm_datafile():
                volume = "-s 1:0,virtio-blk," + self.vm_datafile
            else:
                if verbose:
                    print("KO, error in data file definition")
                go_to_load = False

        # Creation of the console part of the command
        if go_to_load:
            if self.vm_console.create_console():
                console = "-s 31,lpc -l com1,/dev/nmdm" + str(self.vm_console.console_index) + "A"
            else:
                if verbose:
                    print("KO, error console definition")
                go_to_load = False         
     
        # Load the vm
        if go_to_load:
            # Boot loader definition
            if self.vm_template.template_core == "Linux":
                bhyve_load = "grub-bhyve -c /dev/null -m " + self.vm_datafile_map + " -r hd0,msdos1 -M " + str(self.vm_mem) + " " + self.vm_name
            else:
                bhyve_load = "bhyveload -c /dev/null -m "+ str(self.vm_mem) + " -d " + self.vm_datafile + " " + self.vm_name  
            
            # VM boot definition
            bhyve_cmd = "bhyve -c " + str(self.vm_cpu) + " -m " + str(self.vm_mem) + " -A -H -P -s 0:0,hostbridge " + volume + " " + network + " " + console + " " + self.vm_name
            
            # Bootloader execution
            p_load = subprocess.Popen(shlex.split(bhyve_load))
            p_load.wait()

            # VM boot execution
            p_cmd = subprocess.Popen(shlex.split(bhyve_cmd),close_fds=True)
            if verbose:
                print("OK")

    # Unload the machine on the host
    def unload(self,verbose=True):
        if verbose:
            print("Unloading",self.vm_name,"...",end=' ',flush=True)
        # Check if the machine is already loaded
        if self.vm_running:
            bhyve_stop = "bhyvectl --force-poweroff --vm=" + self.vm_name
            p_stop = subprocess.Popen(shlex.split(bhyve_stop))
            p_stop.wait()
            
        if self.vm_loaded:
            bhyve_destroy = "bhyvectl --destroy --vm=" + self.vm_name
            p_destroy = subprocess.Popen(shlex.split(bhyve_destroy))
            p_destroy.wait()

        # Shut the network part
        for port in self.vm_port_list:
            port.unset_port() 
                
        # Shut of the console part
        self.vm_console.destroy_console()
        
        # Update the machine status
        self.set_status()
        if verbose:
            print("OK")

    # Unload and load the machine on the host if it is already loaded        
    def reload(self,verbose=True):
        if verbose:
            print("Reloading",self.vm_name,"...",end=' ',flush=True)      
        if self.vm_running or self.vm_loaded:
            self.unload(verbose=False)
            self.load(verbose=False)
            if verbose:
                print("OK")
        else:
            if verbose:
                print("Machine not loaded")

    # Create a new Machine entry
    def create(pathfile):
        name = input("Enter the name of the machine: ")
        # check_name
        template = input("Enter the name of the template: ")
        # check_template
        cpu = input("Enter the number of cpu: ")
        # check_cpu
        mem = input("Enter the amoung of memory (in M): ")
        # check_mem
        console = input("Enter the number of the console port: ")
        # check_console
        portlist = input("Enter the list of the ports: ")
        # check_portlist
        f = open(pathfile,"a")
        f.write(name + ":" + template + ":" + cpu + ":" + mem + ":" + console + ":" + portlist + "\n")
        f.close()

    # Modify a existing machine entry
    def modify(pathfile,theVm):
        name = input("Enter the name of the machine (" + theVm.vm_name + "): ")
        # check_name
        template = input("Enter the name of the template (" + theVm.vm_template + "): ")
        # check_template
        cpu = input("Enter the number of cpu (" + theVm.vm_cpu + "): ")
        # check_cpu
        mem = input("Enter the amoung of memory (in M) (" + theVm.vm_mem + "): ")
        # check_mem
        console = input("Enter the number of the console port (" + theVm.vm_console.console_port + "): ")
        # check_console
        portlist = input("Enter the list of the ports (" + theVm.print_vm_port_list() + "): ")
        # check_portlist
        change_cmd = "sed -i \"\" -e 's/^" + theVm.vm_name + ":.*/" + name + ":" + template + ":" + cpu + ":" + mem + ":" + console + ":" + portlist + "/g' " + pathfile
        p_load = subprocess.Popen(shlex.split(change_cmd))

    # Modify a existing machine entry
    def delete(pathfile,theVm):
        change_cmd = "sed -i \"\" -e 's/^" + theVm.vm_name + ":/d' " + pathfile
        p_load = subprocess.Popen(shlex.split(change_cmd))
