/* 
 *  kbleds.c - Blink keyboard leds until the module is unloaded.
 */

#include <linux/module.h>
#include <linux/config.h>
#include <linux/init.h>
#include <linux/tty.h>		/* For fg_console, MAX_NR_CONSOLES */
#include <linux/kd.h>		/* For KDSETLED */
#include <linux/console_struct.h>	/* For vc_cons */

MODULE_DESCRIPTION("Example module illustrating the use of Keyboard LEDs.");
MODULE_AUTHOR("Daniele Paolo Scarpazza");
MODULE_LICENSE("GPL");

struct timer_list my_timer;
struct tty_driver *my_driver;
char kbledstatus = 0;

#define BLINK_DELAY   HZ/5
#define ALL_LEDS_ON   0x07
#define RESTORE_LEDS  0xFF

/*
 * Function my_timer_func blinks the keyboard LEDs periodically by invoking
 * command KDSETLED of ioctl() on the keyboard driver. To learn more on virtual 
 * terminal ioctl operations, please see file:
 *     /usr/src/linux/drivers/char/vt_ioctl.c, function vt_ioctl().
 *
 * The argument to KDSETLED is alternatively set to 7 (thus causing the led 
 * mode to be set to LED_SHOW_IOCTL, and all the leds are lit) and to 0xFF
 * (any value above 7 switches back the led mode to LED_SHOW_FLAGS, thus
 * the LEDs reflect the actual keyboard status).  To learn more on this, 
 * please see file:
 *     /usr/src/linux/drivers/char/keyboard.c, function setledstate().
 * 
 */

static void my_timer_func(unsigned long ptr)
{
	int *pstatus = (int *)ptr;

	if (*pstatus == ALL_LEDS_ON)
		*pstatus = RESTORE_LEDS;
	else
		*pstatus = ALL_LEDS_ON;

	(my_driver->ioctl) (vc_cons[fg_console].d->vc_tty, NULL, KDSETLED,
			    *pstatus);

	my_timer.expires = jiffies + BLINK_DELAY;
	add_timer(&my_timer);
}

static int __init kbleds_init(void)
{
	int i;

	printk(KERN_INFO "kbleds: loading\n");
	printk(KERN_INFO "kbleds: fgconsole is %x\n", fg_console);
	for (i = 0; i < MAX_NR_CONSOLES; i++) {
		if (!vc_cons[i].d)
			break;
		printk(KERN_INFO "poet_atkm: console[%i/%i] #%i, tty %lx\n", i,
		       MAX_NR_CONSOLES, vc_cons[i].d->vc_num,
		       (unsigned long)vc_cons[i].d->vc_tty);
	}
	printk(KERN_INFO "kbleds: finished scanning consoles\n");

	my_driver = vc_cons[fg_console].d->vc_tty->driver;
	printk(KERN_INFO "kbleds: tty driver magic %x\n", my_driver->magic);

	/*
	 * Set up the LED blink timer the first time
	 */
	init_timer(&my_timer);
	my_timer.function = my_timer_func;
	my_timer.data = (unsigned long)&kbledstatus;
	my_timer.expires = jiffies + BLINK_DELAY;
	add_timer(&my_timer);

	return 0;
}

static void __exit kbleds_cleanup(void)
{
	printk(KERN_INFO "kbleds: unloading...\n");
	del_timer(&my_timer);
	(my_driver->ioctl) (vc_cons[fg_console].d->vc_tty, NULL, KDSETLED,
			    RESTORE_LEDS);
}

module_init(kbleds_init);
module_exit(kbleds_cleanup);
