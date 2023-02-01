import shlex
import subprocess

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