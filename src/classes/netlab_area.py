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
