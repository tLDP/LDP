#! /bin/sh

# A script to create file systems on logical volumes. Created at bare
# metal backup time by the Perl script make.fdisk.

# Copyright 2006 through the last date of modification Charles Curley.

# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA

# You can also contact the Free Software Foundation at http://www.fsf.org/

# For more information contact the author, Charles Curley, at
# http://www.charlescurley.com/.


export blockcheck=$1;

if [ "$blockcheck" != "-c" ] && [ -n "$blockcheck" ]
then
    echo "${0}: Build file systems on logical volumes."
    echo "${0}: -c: block check during file system making."
    exit 1;
fi

export LVM_SYSTEM_DIR=$(pwd)/lvm.cfg

echo "y\n" | pvcreate -ff --uuid "CCmw0N-0We2-HzRS-jRZa-FkC7-NxTc-oAfvpX"\
     --restorefile lvm.cfg/archive/VolGroup00_*.vg   /dev/hda3
vgcfgrestore --file LVM.backs VolGroup00

# Hideously disty dependent!
if [ -e /etc/init.d/lvm ] ; then
     /etc/init.d/lvm start
fi

echo
echo making LV /dev/VolGroup00/LogVol00 an ext3 partition.
mke2fs -j $blockcheck /dev/VolGroup00/LogVol00

echo
echo making LV /dev/VolGroup00/LogVol02 an ext3 partition.
mke2fs -j $blockcheck /dev/VolGroup00/LogVol02

echo
echo making LV /dev/VolGroup00/LogVol01 a swap partition.
mkswap $blockcheck /dev/VolGroup00/LogVol01

