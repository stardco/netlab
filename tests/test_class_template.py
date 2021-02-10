import getopt
from netlab_classes import *

if __name__ == "__main__":
    # Creation of a port
    myTemplate1 = Template('BSDRP','BSD','/usr/local/etc/netlab/templates/BSDRP-1.97-full-amd64-serial.img')
    myTemplate2 = Template('Debian','Linux','/usr/local/etc/netlab/templates/Debian-10.2.0.img',["/usr/local/etc/netlab/templates/Debian-10.2.0.map","FILE"])
    
    # Checks variables
    print("=== Check variables ===")
    print("Name :", myTemplate1.template_name,end="\t\t")
    print("Type :", myTemplate1.template_core,end="\t\t")
    print("Image path :", myTemplate1.template_image,end="\t\t")
    print("Files path :", myTemplate1.template_files)
    print("Name :", myTemplate2.template_name,end="\t\t")
    print("Type :", myTemplate2.template_core,end="\t\t")
    print("Image path :", myTemplate2.template_image,end="\t\t")
    print("Files path :", myTemplate2.template_files)
    print("=======================")