#!/bin/bash

set -e

if [ "z$TBAKEY" == "z" ]
then
	echo "TBAKEY env variable not set"
	echo "Get API key from https://www.thebluealliance.com/apidocs"
	echo "then run"
	echo "export TBAKEY=abcd...."
	exit 1
fi

mkdir -p data/

for event in 2025cur 2025new 2025dal 2025joh 2025arc 2025gal 2025hop 2025mil
do
	curl -H "X-TBA-Auth-Key: $TBAKEY" https://www.thebluealliance.com/api/v3/event/$event > data/$event.event.json
	sleep 1
	curl -H "X-TBA-Auth-Key: $TBAKEY" https://www.thebluealliance.com/api/v3/event/$event/matches > data/$event.matches.json
	sleep 1
done
