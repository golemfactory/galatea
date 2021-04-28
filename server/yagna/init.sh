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

# having key generation a last step allows api service to wait until yagna is ready
/usr/bin/yagna app-key create requestor
/usr/bin/yagna app-key list --json > /root/.local/share/yagna/app_key

# now we bring the primary process back into the foreground
# and leave it there
fg %1
