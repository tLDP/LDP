#/bin/sh

#compile userspace app
gcc -o ioctl ioctl.c

#create character device
mknod char_dev c 100 0
