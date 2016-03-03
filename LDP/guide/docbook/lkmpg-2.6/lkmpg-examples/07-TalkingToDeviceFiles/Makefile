obj-m += chardev.o

all: ioctl module

module:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

install:
	mknod /proc/char_dev c 100 0

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
	rm -f ioctl
