The Problem with this example is, you will get unresolved symbols
if you try to insmod it into a stock 2.6.x kernel.

This is because the interception of system calls via sys_call_table 
is considered harmful and thus no longer supported. (since 2.5.41)

See the thread: (pick just one)  

  http://www.ussg.iu.edu/hypermail/linux/kernel/0305.0/0711.html
  http://marc.free.net.ph/message/20030505.081945.fa640369.html
  http://marc.theaimsgroup.com/?l=linux-kernel&m=105212296015799&w=2

for why.

To be able to get this example running with post 2.5.41 (read 2.6.x) 
kernels you must patch your kernel to export sys_call_table.

WARNING: 
	DONT TRY THIS ON PRODUCTION SYSTEMS, OR ANY OTHER SYSTEMS
	WITH VALUEABLE DATA ON IT.


If I had to write a Configure.help entry for this patch it would
be tagged <dangerous> and probably look like this:

#######################################################################

This option exports the sys_call_table, which makes it possible to 
intercept system calls. Intercepting system calls is dangerous,
and might cause data loss or worse.

Say Y if you want to try the included example and don't care about 
data loss and other scary stuff.

Virtually anybody else should say N here.

#######################################################################

Using an old PC you don't need for anything else as a sandbox
might be a good idea either.

Assuming your current 2.6.x kernel tree lies under /usr/src/linux/
(where it should not! [1] ;) the script below shows how to apply,
compile and boot a sys_call_table exporting kernel in one go.

This patch has been tested with 2.6.[0123], and may / may not apply
clean / at all to other versions.

[1] http://www.linuxmafia.com/faq/Kernel/usr-src-linux-symlink.html


#!/bin/sh
cp export_sys_call_table_patch_for_linux_2.6.x /usr/src/linux/
cd /usr/src/linux/
patch -p0 < export_sys_call_table_patch_for_linux_2.6.x


