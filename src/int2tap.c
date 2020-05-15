#include <sys/ioctl.h>
#include <sys/stat.h>
#include <net/if.h>
#include <net/if_tap.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <dirent.h>
#include <unistd.h>
#include <ctype.h>

char * findDevName(char * intName); 

/*void main() {
	char * myIntName;
	char * myDevName;
	printf("Saisissez un nom d'interface tap :\n");
	scanf("%s",myIntName);
	printf("The dev name of %s is %s\n",myIntName,findDevName(myIntName));	
}*/

int main (int argc, char **argv) {
	char * myIntName = NULL;
	char * myDevName;
	int index;
	int c;

	opterr = 0;


	while ((c = getopt (argc, argv, "i:")) != -1)
		switch (c) {
			case 'i':
				myIntName = optarg;
				break;
			case '?':
				if (optopt == 'c')
					fprintf (stderr, "Option -%c requires an argument.\n", optopt);
				else if (isprint (optopt))
					fprintf (stderr, "Unknown option `-%c'.\n", optopt);
				else
					fprintf (stderr, "Unknown option character `\\x%x'.\n", optopt);
				return 1;
			default:
				abort ();
		}
	
	printf("%s\n",findDevName(myIntName));	

	for (index = optind; index < argc; index++)
		printf ("Non-option argument %s\n", argv[index]);
	return 0;
}



/* this function returns the name of the device according to the name in input
input : * char is the interface name (or alias)
output : * char is the name present in /dev 
if interface does not exist the function return the input by default */
char * findDevName(char * intName) {
	
	/* variable implementation */
	int fd;
	char * path = "/dev/";
	char *tbuf, *tbuf2, *devName;
	struct ifreq myTapInfo; //use to find the tap name 
        DIR *d;
        struct dirent *dir;
	
	/* variable initialisation */
	devName = (char*) malloc(sizeof(char*));
	devName = strdup(intName);

	/* Openning directory */
	d = opendir("/dev/");
	/* readding file in directory if not empty */
	if (d) {
		while ((dir = readdir(d)) != NULL) {
		/* looking for tap file and implement it on the table tbl */
			tbuf = (char *) malloc((strlen(dir->d_name) + 1) * sizeof(char) );
			strcpy(tbuf,dir->d_name);
			if(strncmp("tap", tbuf, 3) == 0) {
				tbuf2 = (char *) malloc(sizeof(char) * (strlen(path) + strlen(tbuf) + 1 ));
				tbuf2 = strdup(path);
				strcat(tbuf2, tbuf);
				fd = open(tbuf2, O_RDONLY); // opening the device
				ioctl(fd, TAPGIFNAME, &myTapInfo); // looking for the tap device name
				/* If finded we break the loop */
				if(strcmp(myTapInfo.ifr_name,intName) == 0 || strcmp(tbuf,intName) == 0) {
					devName = strdup(tbuf);
					close(fd);
					free(tbuf2);
					free(tbuf);
					break;
				}
				close(fd);
				free(tbuf2);		
			}
			free(tbuf);
		}
		/* closing directory */
		closedir(d);
	}
	free(tbuf);
	return devName;	
}
