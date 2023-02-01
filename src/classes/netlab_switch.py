import shlex
import subprocess

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