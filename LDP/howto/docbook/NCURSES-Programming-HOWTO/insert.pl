#!/usr/local/bin/perl
# Converts the inline programlistings into filerefs
# The original source should contain some thing like
# <programlisting>
# /* File Path: adir/filename */
# ..
# ..
# ..
# </programlisting>
#
# this gets converted to
# 
# <programlisting><inlinemediaobject><imageobject>
#   <imagedata format="linespecific" fileref="adir/filename">
# </imageobject></inlinemediaobject></programlisting>
#

if(@ARGV != 1) {
    print "Usage: $0 <sgml source with programs inline>\n";
    exit(1);
}

open(ORIG, "<$ARGV[0]") || die("Cannot open input file");
open(TMP, ">tmp.out");

$ready = 0;

while(<ORIG>) {
    chomp;

    if(/^\<programlisting\>/) {
        $ready = 1;
    }
    elsif ($ready == 1) {
        if(/^\/\*.*:\s([\w\/\.]+)\s/) {
            print TMP "<programlisting><inlinemediaobject><imageobject>\n";
            print TMP "    <imagedata format=\"linespecific\" \ 
    fileref=\"ncurses_programs/$1\">\n";
            $ready = 2;
        }
        else {
            print TMP "<programlisting>\n";
            print TMP "$_\n";
            $ready = 0;
        }
    }
    elsif($ready == 2 && /\<\/programlisting\>/) {
        print TMP "</imageobject></inlinemediaobject></programlisting>\n";
        $ready = 0;
    }
    elsif($ready != 2) {
        print TMP $_, "\n";
        next;
    }
}
close(TMP);
close(ORIG);

#system("mv tmp.out $ARGV[0]");
