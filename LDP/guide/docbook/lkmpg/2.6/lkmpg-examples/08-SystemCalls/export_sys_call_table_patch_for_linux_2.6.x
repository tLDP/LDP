--- kernel/kallsyms.c.orig	2003-12-30 07:07:17.000000000 +0000
+++ kernel/kallsyms.c	2003-12-30 07:43:43.000000000 +0000
@@ -184,7 +184,7 @@
 		iter->pos = pos;
 		return get_ksymbol_mod(iter);
 	}
-	
+
 	/* If we're past the desired position, reset to start. */
 	if (pos < iter->pos)
 		reset_iter(iter);
@@ -291,3 +291,11 @@
 
 EXPORT_SYMBOL(kallsyms_lookup);
 EXPORT_SYMBOL(__print_symbol);
+/* START OF DIRTY HACK:
+ * Purpose: enable interception of syscalls as shown in the
+ * Linux Kernel Module Programming Guide. */
+extern void *sys_call_table;
+EXPORT_SYMBOL(sys_call_table);
+ /* see http://marc.free.net.ph/message/20030505.081945.fa640369.html
+  * for discussion why this is a BAD THING(tm) and no longer supported by 2.6.0
+  * END OF DIRTY HACK: USE AT YOUR OWN RISK */
