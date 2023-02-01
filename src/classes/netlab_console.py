import shlex
import os.path
import subprocess

class Console:
    def __init__(self, vm_name, port, timeout, run_file):
    # Initialization of the Console
        self.console_vm_name = vm_name
        self.console_port = port
        self.console_timeout = timeout
        self.console_index = -1
        self.console_pid = -1
        self.console_run_file = run_file
        if not os.path.exists(self.console_run_file):
            open(self.console_run_file, 'w').close()
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
            p_cmd = subprocess.Popen(shlex.split(telnet_cmd))
            p_cmd.wait()
        else:
            print("The port of",self.console_vm_name,"is not active")