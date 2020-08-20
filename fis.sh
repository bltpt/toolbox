#!/bin/sh

# fis.sh: FreeBSD Installation Status
# Purpose: to compare the installed version of FreeBSD with the
#          running version, so you can tell if you need to
#          reboot.

installed=`freebsd-version`
running=`uname -a | cut -f 3 -d " "`

echo Installed: $installed
echo Runnning: $running
