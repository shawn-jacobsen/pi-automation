#!/bin/bash
for file in ./scripts/*.js;
do
 nohup node $file &
done
wait
