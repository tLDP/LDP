/*
 *  stop.c - Illustration of multi filed modules
 */

#include <linux/kernel.h>	/* We're doing kernel work */
#include <linux/module.h>	/* Specifically, a module  */

void cleanup_module()
{
	printk("<1>Short is the life of a kernel module\n");
}
