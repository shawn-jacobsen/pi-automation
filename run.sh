#!/bin/bash
for file in ./scripts/*.js;
do
  node $file &
done
wait
