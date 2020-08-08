#!/bin/bash
for file in home/pi/Documents/pi-automation/scripts/*.js;
do
 nohup node $file &
done
wait
