#!/bin/bash
# soundcard-on.sh

#  Script author: Mkarcher
#  http://www.thinkwiki.org/wiki  ...
#  /Script_for_configuring_the_CS4239_sound_chip_in_PnP_mode
#  ABS Guide author made minor changes and added comments.
#  Couldn't contact script author to ask for permission to use, but ...
#+ the script was released under the FDL,
#+ so its use here should be both legal and ethical.

#  Sound-via-pnp-script for Thinkpad 600E
#+ and possibly other computers with onboard CS4239/CS4610
#+ that do not work with the PCI driver
#+ and are not recognized by the PnP code of snd-cs4236.
#  Also for some 770-series Thinkpads, such as the 770x.
#  Run as root user, of course.
#
#  These are old and very obsolete laptop computers,
#+ but this particular script is very instructive,
#+ as it shows how to set up and hack device files.



#  Search for sound card pnp device:

for dev in /sys/bus/pnp/devices/*
do
  grep CSC0100 $dev/id > /dev/null &amp;&amp; WSSDEV=$dev
  grep CSC0110 $dev/id > /dev/null &amp;&amp; CTLDEV=$dev
done
# On 770x:
# WSSDEV = /sys/bus/pnp/devices/00:07
# CTLDEV = /sys/bus/pnp/devices/00:06
# These are symbolic links to /sys/devices/pnp0/ ...


#  Activate devices:
#  Thinkpad boots with devices disabled unless "fast boot" is turned off
#+ (in BIOS).

echo activate > $WSSDEV/resources
echo activate > $CTLDEV/resources


# Parse resource settings.

{ read # Discard "state = active" (see below).
  read bla port1
  read bla port2
  read bla port3
  read bla irq
  read bla dma1
  read bla dma2
 # The "bla's" are labels in the first field: "io," "state," etc.
 # These are discarded.

 #  Hack: with PnPBIOS: ports are: port1: WSS, port2:
 #+ OPL, port3: sb (unneeded)
 #       with ACPI-PnP:ports are: port1: OPL, port2: sb, port3: WSS
 #  (ACPI bios seems to be wrong here, the PnP-card-code in snd-cs4236.c
 #+  uses the PnPBIOS port order)
 #  Detect port order using the fixed OPL port as reference.
  if [ ${port2%%-*} = 0x388 ]
 #            ^^^^  Strip out everything following hyphen in port address.
 #                  So, if port1 is 0x530-0x537
 #+                 we're left with 0x530 -- the start address of the port.
 then
   # PnPBIOS: usual order
   port=${port1%%-*}
   oplport=${port2%%-*}
 else
   # ACPI: mixed-up order
   port=${port3%%-*}
   oplport=${port1%%-*}
 fi
 } &lt; $WSSDEV/resources
# To see what's going on here:
# ---------------------------
#   cat /sys/devices/pnp0/00:07/resources
#
#   state = active
#   io 0x530-0x537
#   io 0x388-0x38b
#   io 0x220-0x233
#   irq 5
#   dma 1
#   dma 0
#   ^^^   "bla" labels in first field (discarded). 


{ read # Discard first line, as above.
  read bla port1
  cport=${port1%%-*}
  #            ^^^^
  # Just want _start_ address of port.
} &lt; $CTLDEV/resources


# Load the module:

modprobe --ignore-install snd-cs4236 port=$port cport=$cport\
fm_port=$oplport irq=$irq dma1=$dma1 dma2=$dma2 isapnp=0 index=0
# See the modprobe manpage.

exit $?
