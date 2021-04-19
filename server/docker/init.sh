#!/bin/bash

# turn on bash's job control
set -m

# Start the primary process and put it in the background
/usr/bin/yagna service run &

# Wait for the service to boot
sleep 5

# Start the helper process
/usr/bin/yagna payment fund --driver zksync
/usr/bin/yagna payment init --sender --driver zksync

# now we bring the primary process back into the foreground
# and leave it there
fg %1
