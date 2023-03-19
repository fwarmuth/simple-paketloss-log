#!/bin/bash
OUTPUT=./ping.log
LOCK=.pingcheck_running.tmp

# check lock
if test -f "$LOCK"; then
    echo "Trying to start a new check, but check already running" >> $OUTPUT
    exit
fi
# create lock
touch $LOCK

# Do check
packet=$(ping -i.2 -c 100 google.de | tail -3 | ts '[%Y-%m-%d %H:%M:%S]')
echo "$packet"  >> $OUTPUT
echo "---------------------" >> $OUTPUT

# remove lock
rm $LOCK


