/*
 *  sched.c - scheduale a function to be called on every timer interrupt.
 *
 *  Copyright (C) 2001 by Peter Jay Salzman
 */

/* 
 * The necessary header files 
 */

/* 
 * Standard in kernel modules 
 */
#include <linux/kernel.h>	/* We're doing kernel work */
#include <linux/module.h>	/* Specifically, a module */
#include <linux/proc_fs.h>	/* Necessary because we use the proc fs */
#include <linux/workqueue.h>	/* We scheduale tasks here */
#include <linux/sched.h>	/* We need to put ourselves to sleep 
				   and wake up later */
#include <linux/init.h>		/* For __init and __exit */
#include <linux/interrupt.h>	/* For irqreturn_t */

struct proc_dir_entry *Our_Proc_File;
#define PROC_ENTRY_FILENAME "sched"
#define MY_WORK_QUEUE_NAME "WQsched.c"

/* 
 * The number of times the timer interrupt has been called so far 
 */
static int TimerIntrpt = 0;

static void intrpt_routine(void *);

static int die = 0;		/* set this to 1 for shutdown */

/* 
 * The work queue structure for this task, from workqueue.h 
 */
static struct workqueue_struct *my_workqueue;

static struct work_struct Task;
static DECLARE_WORK(Task, intrpt_routine, NULL);

/* 
 * This function will be called on every timer interrupt. Notice the void*
 * pointer - task functions can be used for more than one purpose, each time
 * getting a different parameter.
 */
static void intrpt_routine(void *irrelevant)
{
	/* 
	 * Increment the counter 
	 */
	TimerIntrpt++;

	/* 
	 * If cleanup wants us to die
	 */
	if (die == 0)
		queue_delayed_work(my_workqueue, &Task, 100);
}

/* 
 * Put data into the proc fs file. 
 */
ssize_t
procfile_read(char *buffer,
	      char **buffer_location,
	      off_t offset, int buffer_length, int *eof, void *data)
{
	int len;		/* The number of bytes actually used */

	/* 
	 * It's static so it will still be in memory 
	 * when we leave this function
	 */
	static char my_buffer[80];

	/* 
	 * We give all of our information in one go, so if anybody asks us
	 * if we have more information the answer should always be no.
	 */
	if (offset > 0)
		return 0;

	/* 
	 * Fill the buffer and get its length 
	 */
	len = sprintf(my_buffer, "Timer called %d times so far\n", TimerIntrpt);

	/* 
	 * Tell the function which called us where the buffer is 
	 */
	*buffer_location = my_buffer;

	/* 
	 * Return the length 
	 */
	return len;
}

/* 
 * Initialize the module - register the proc file 
 */
int __init init_module()
{
	/*
	 * Create our /proc file
	 */
	Our_Proc_File = create_proc_entry(PROC_ENTRY_FILENAME, 0644, NULL);
	
	if (Our_Proc_File == NULL) {
		remove_proc_entry(PROC_ENTRY_FILENAME, &proc_root);
		printk(KERN_ALERT "Error: Could not initialize /proc/%s\n",
		       PROC_ENTRY_FILENAME);
		return -ENOMEM;
	}

	Our_Proc_File->read_proc = procfile_read;
	Our_Proc_File->owner = THIS_MODULE;
	Our_Proc_File->mode = S_IFREG | S_IRUGO;
	Our_Proc_File->uid = 0;
	Our_Proc_File->gid = 0;
	Our_Proc_File->size = 80;

	/* 
	 * Put the task in the work_timer task queue, so it will be executed at
	 * next timer interrupt
	 */
	my_workqueue = create_workqueue(MY_WORK_QUEUE_NAME);
	queue_delayed_work(my_workqueue, &Task, 100);
	
	
	printk(KERN_INFO "/proc/%s created\n", PROC_ENTRY_FILENAME);
	
	return 0;
}

/* 
 * Cleanup
 */
void __exit cleanup_module()
{
	/* 
	 * Unregister our /proc file 
	 */
	remove_proc_entry(PROC_ENTRY_FILENAME, &proc_root);
	printk(KERN_INFO "/proc/%s removed\n", PROC_ENTRY_FILENAME);

	die = 1;		/* keep intrp_routine from queueing itself */
	cancel_delayed_work(&Task);	/* no "new ones" */
	flush_workqueue(my_workqueue);	/* wait till all "old ones" finished */
	destroy_workqueue(my_workqueue);

	/* 
	 * Sleep until intrpt_routine is called one last time. This is 
	 * necessary, because otherwise we'll deallocate the memory holding 
	 * intrpt_routine and Task while work_timer still references them.
	 * Notice that here we don't allow signals to interrupt us.
	 *
	 * Since WaitQ is now not NULL, this automatically tells the interrupt
	 * routine it's time to die.
	 */

}

/* 
 * some work_queue related functions
 * are just available to GPL licensed Modules 
 */
MODULE_LICENSE("GPL");
