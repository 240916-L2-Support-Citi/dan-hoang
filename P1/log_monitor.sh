#!/bin/bash

logfile="./app.log"
skip=$(< log_monitor_skip.txt)

tail -n +$skip $logfile | while read line
do
    regex="(.*) \[(.*)\] (.*)"

    if [[ $line =~ $regex ]]
    then
        timestamp="${BASH_REMATCH[1]}"
        level="${BASH_REMATCH[2]}"
        message="${BASH_REMATCH[3]//\'/''}"
        psql -d log_entry -c "INSERT INTO log_entry (log_entry_timestamp, level, log_entry_message) VALUES (timestamp '$timestamp', '$level', '$message')"
    fi

    skip=$((skip + 1))
    echo "$skip" > log_monitor_skip.txt
done
