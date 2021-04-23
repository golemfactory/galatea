#!/bin/bash

# turn on bash's job control
set -m

# Wait for the yagna service to finish init
echo "Waiting for yagna service full init..."
sleep 5

path=./yagna/app_key
max_iterations=10
wait_seconds=2

iterations=0

while true
do
	((iterations++))
	echo "Attempt [$iterations / $max_iterations]"
	sleep $wait_seconds

	if [ -f "$path" ]; then
		echo "Yagna is ready!"
		break
	fi

	if [ "$iterations" -ge "$max_iterations" ]; then
		echo "Timeout: Yagna did not started in a timeframe"
		exit 1
	fi
done

# Starting the api server
QUART_ENV=development \
QUART_APP="app:create_app()" \
quart run --host=0.0.0.0
