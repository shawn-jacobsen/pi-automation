#!/bin/bash
for file in ~/Documents/pi-automation/scripts/*.js;
do
 nohup node $file &
done
wait
